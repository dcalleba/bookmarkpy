import os
import logging
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class Statistics:
    total_md_files_dir1: int = 0
    total_md_files_dir2: int = 0
    total_size_dir1: int = 0
    total_size_dir2: int = 0
    missing_in_dir2: int = 0
    missing_in_dir1: int = 0
    different_sizes: int = 0
    empty_files_dir1: int = 0
    empty_files_dir2: int = 0
    empty_in_dir1_not_dir2: int = 0
    empty_in_dir2_not_dir1: int = 0

class DirectoryComparer:
    def __init__(self, dir1: str, dir2: str):
        self.dir1 = dir1
        self.dir2 = dir2
        self.stats = Statistics()
        self._setup_logging()

    def _setup_logging(self):
        log_filename = f"directory_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def compare(self) -> List[Tuple[str, str]]:
        self.logger.info(f"Début de la comparaison entre:\nDossier 1: {self.dir1}\nDossier 2: {self.dir2}")
        
        differences = []
        files1 = self._get_md_files(self.dir1)
        files2 = self._get_md_files(self.dir2)

        # Calcul des statistiques de base
        self.stats.total_md_files_dir1 = len(files1)
        self.stats.total_md_files_dir2 = len(files2)
        self.stats.total_size_dir1 = sum(files1.values())
        self.stats.total_size_dir2 = sum(files2.values())
        
        # Comptage des fichiers vides
        self.stats.empty_files_dir1 = sum(1 for size in files1.values() if size == 0)
        self.stats.empty_files_dir2 = sum(1 for size in files2.values() if size == 0)

        # Comparaison des fichiers
        for f in files1:
            rel_path = os.path.relpath(f, self.dir1)
            f2 = os.path.join(self.dir2, rel_path)
            
            if f2 not in files2:
                self.stats.missing_in_dir2 += 1
                status = " (fichier vide)" if files1[f] == 0 else ""
                differences.append((rel_path, f'Présent dans dir1, absent dans dir2{status}'))
            elif files1[f] != files2[f2]:
                self.stats.different_sizes += 1
                if files1[f] == 0 and files2[f2] != 0:
                    self.stats.empty_in_dir1_not_dir2 += 1
                    differences.append((rel_path, f'Vide dans dir1 ({files1[f]} Ko), non vide dans dir2 ({files2[f2]} Ko)'))
                elif files1[f] != 0 and files2[f2] == 0:
                    self.stats.empty_in_dir2_not_dir1 += 1
                    differences.append((rel_path, f'Non vide dans dir1 ({files1[f]} Ko), vide dans dir2 ({files2[f2]} Ko)'))
                else:
                    differences.append((rel_path, f'Taille différente: dir1 = {files1[f]} Ko, dir2 = {files2[f2]} Ko'))

        # Vérification des fichiers uniquement dans dir2
        for f in files2:
            rel_path = os.path.relpath(f, self.dir2)
            f1 = os.path.join(self.dir1, rel_path)
            if f1 not in files1:
                self.stats.missing_in_dir1 += 1
                status = " (fichier vide)" if files2[f] == 0 else ""
                differences.append((rel_path, f'Absent dans dir1, présent dans dir2{status}'))

        self._log_statistics()
        return differences

    def _get_md_files(self, directory: str) -> Dict[str, int]:
        md_files = {}
        for root, _, files in os.walk(directory):
            for file in files:
                # if file.endswith('.jpg'):
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    # Conversion en Ko
                    md_files[file_path] = os.path.getsize(file_path) // 1024
        return md_files

    def _log_statistics(self):
        self.logger.info("\n=== Statistiques de la comparaison ===")
        self.logger.info(f"Nombre total de fichiers .md dans le dossier 1: {self.stats.total_md_files_dir1}")
        self.logger.info(f"Nombre total de fichiers .md dans le dossier 2: {self.stats.total_md_files_dir2}")
        self.logger.info(f"Taille totale des fichiers .md dans le dossier 1: {self.stats.total_size_dir1:,} Ko")
        self.logger.info(f"Taille totale des fichiers .md dans le dossier 2: {self.stats.total_size_dir2:,} Ko")
        self.logger.info(f"Fichiers manquants dans le dossier 2: {self.stats.missing_in_dir2}")
        self.logger.info(f"Fichiers manquants dans le dossier 1: {self.stats.missing_in_dir1}")
        self.logger.info(f"Fichiers avec des tailles différentes: {self.stats.different_sizes}")
        self.logger.info("\n=== Statistiques des fichiers vides ===")
        self.logger.info(f"Fichiers vides dans le dossier 1: {self.stats.empty_files_dir1}")
        self.logger.info(f"Fichiers vides dans le dossier 2: {self.stats.empty_files_dir2}")
        self.logger.info(f"Fichiers vides uniquement dans dir1: {self.stats.empty_in_dir1_not_dir2}")
        self.logger.info(f"Fichiers vides uniquement dans dir2: {self.stats.empty_in_dir2_not_dir1}")

if __name__ == "__main__":
    try:
        #dir1 = input("Entrez le chemin du premier dossier: ")
        #dir2 = input("Entrez le chemin du deuxième dossier: ")
        dir1 = "/users/danielcallebaut/desktop/obsimind"
        dir2 = "/users/danielcallebaut/desktop/obsimind_imgcomp"
        comparer = DirectoryComparer(dir1, dir2)
        differences = comparer.compare()
        
        if differences:
            print("\nDifférences trouvées:")
            for file, diff in differences:
                print(f"Fichier: {file} - {diff}")
        else:
            print("\nAucune différence trouvée.")
            
    except Exception as e:
        logging.error(f"Une erreur est survenue: {str(e)}", exc_info=True)