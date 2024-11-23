import os
import shutil
import logging
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass
class FileAction:
    source_path: str
    dest_path: str
    action_type: str  # 'copy' ou 'delete'
    file_size: int
    relative_path: str
    target_dir: str  # 'dir1' ou 'dir2'


class FileManager:
    def __init__(self, dir1: str, dir2: str, enable_logging: bool = True):
        self.dir1 = dir1
        self.dir2 = dir2
        self.actions_proposees: List[FileAction] = []
        if enable_logging:
            self._setup_logging()
        else:
            logging.disable(logging.CRITICAL)

    def _setup_logging(self):
        # Configuration avec plusieurs handlers pour fichier et console
        log_filename = f"file_manager_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        # Création du logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        
        # Handler pour fichier
        file_handler = logging.FileHandler(log_filename, mode='w')
        file_handler.setLevel(logging.DEBUG)
        
        # Handler pour console 
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formateur
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Ajout des handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # Désactivation de la propagation pour éviter la duplication
        self.logger.propagate = False

    def get_action_indices(self, action_type: str = None) -> List[int]:
        """Retourne les indices des actions selon leur type."""
        return [i for i, action in enumerate(self.actions_proposees)
                if action_type is None or action.action_type == action_type]

    def analyser_differences(self) -> List[FileAction]:
        self.logger.info("Début de l'analyse des différences")
        self.actions_proposees.clear()
        
        from compare2_md import DirectoryComparer
        comparer = DirectoryComparer(self.dir1, self.dir2)
        differences = comparer.compare_directories()
        
        self.logger.info(f"Nombre de différences trouvées: {len(differences)}")
        
        for diff in differences:
            self.logger.debug(f"Traitement de la différence: {diff}")
            if "absent dans dir2" in diff:
                rel_path = diff.split(": ")[1]
                source = os.path.join(self.dir1, rel_path)
                dest = os.path.join(self.dir2, rel_path)
                self.actions_proposees.append(
                    FileAction(source, dest, 'copy', 
                             os.path.getsize(source), rel_path, 'dir2')
                )
                self.logger.debug(f"Action de copie ajoutée pour: {rel_path}")
            elif "absent dans dir1" in diff:
                rel_path = diff.split(": ")[1]
                source = os.path.join(self.dir2, rel_path)
                self.actions_proposees.append(
                    FileAction(source, "", 'delete',
                             os.path.getsize(source), rel_path, 'dir2')
                )
                self.logger.debug(f"Action de suppression ajoutée pour: {rel_path}")

        self.logger.info(f"Nombre total d'actions proposées: {len(self.actions_proposees)}")
        return self.actions_proposees

    def afficher_propositions(self):
        if not self.actions_proposees:
            print("Aucune action proposée.")
            return

        print("\n=== Actions proposées ===")
        print(f"\nDossier 1: {self.dir1}")
        print(f"Dossier 2: {self.dir2}\n")
        
        for i, action in enumerate(self.actions_proposees, 1):
            if action.action_type == 'copy':
                print(f"{i}. COPIER vers {action.target_dir}:")
                print(f"   Fichier: {action.relative_path}")
                print(f"   De: {action.source_path}")
                print(f"   Vers: {action.dest_path}")
            else:
                print(f"{i}. SUPPRIMER de {action.target_dir}:")
                print(f"   Fichier: {action.relative_path}")
                print(f"   Chemin: {action.source_path}")
            print(f"   Taille: {action.file_size // 1024} Ko\n")

    def executer_actions(self, indices_selectionnes: List[int]) -> bool:
        self.logger.info(f"Début de l'exécution des actions. Nombre d'actions: {len(indices_selectionnes)}")
        try:
            for idx in indices_selectionnes:
                if 0 <= idx < len(self.actions_proposees):
                    action = self.actions_proposees[idx]
                    self.logger.debug(f"Exécution de l'action {idx + 1}/{len(indices_selectionnes)}")
                    
                    if action.action_type == 'copy':
                        self.logger.info(f"Copie de {action.relative_path}")
                        os.makedirs(os.path.dirname(action.dest_path), exist_ok=True)
                        shutil.copy2(action.source_path, action.dest_path)
                        self.logger.info(f"Copié avec succès: {action.relative_path}")
                    else:
                        self.logger.info(f"Suppression de {action.relative_path}")
                        os.remove(action.source_path)
                        self.logger.info(f"Supprimé avec succès: {action.relative_path}")
                    
                    # Forcer l'écriture du buffer
                    for handler in self.logger.handlers:
                        handler.flush()
            
            self.logger.info("Toutes les actions ont été exécutées avec succès")
            return True
        except Exception as e:
            self.logger.error(f"Erreur lors de l'exécution des actions: {str(e)}", exc_info=True)
            return False

if __name__ == "__main__":
    try:
        # dir1 = input("Entrez le chemin du premier dossier: ")
        # dir2 = input("Entrez le chemin du deuxième dossier: ")
        dir1 = "/users/danielcallebaut/desktop/obsimind"
        dir2 = "/users/danielcallebaut/desktop/obsimind_imgcomp"
    
        manager = FileManager(dir1, dir2)
        actions = manager.analyser_differences()
        
        if not actions:
            print("Aucune différence trouvée.")
            exit(0)

        manager.afficher_propositions()
        
        print("\nEntrez les numéros des actions à exécuter (séparés par des espaces)")
        print("Options disponibles:")
        print("- 'all' : tout sélectionner")
        print("- 'all_copy' : sélectionner toutes les copies")
        print("- 'all_supprime' : sélectionner toutes les suppressions")
        print("- 'q' : quitter")
        
        choix = input("> ").strip().lower()
        if choix == 'q':
            exit(0)
        
        indices = []
        if choix == 'all':
            indices = list(range(len(actions)))
        elif choix == 'all_copy':
            indices = manager.get_action_indices('copy')
        elif choix == 'all_supprime':
            indices = manager.get_action_indices('delete')
        else:
            try:
                indices = [int(x) - 1 for x in choix.split()]
            except ValueError:
                print("Entrée invalide")
                exit(1)

        print("\nActions sélectionnées:")
        for idx in indices:
            action = actions[idx]
            if action.action_type == 'copy':
                print(f"- Copier vers {action.target_dir}: {action.relative_path}")
            else:
                print(f"- Supprimer de {action.target_dir}: {action.relative_path}")
        
        confirmation = input("\nConfirmez-vous l'exécution de ces actions? (o/n): ")
        if confirmation.lower() == 'o':
            if manager.executer_actions(indices):
                print("Actions exécutées avec succès")
            else:
                print("Des erreurs sont survenues lors de l'exécution")
        else:
            print("Opération annulée")
            
    except Exception as e:
        logging.error(f"Une erreur est survenue: {str(e)}", exc_info=True)