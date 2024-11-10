import subprocess
import logging
from datetime import datetime
from typing import Optional

class GitAutomation:
    """Classe pour automatiser les opérations Git courantes"""
    
    def __init__(self, enable_logging: bool = True):
        """Initialisation de la classe avec configuration des logs"""
        self.logger = self._setup_logging() if enable_logging else None

    def _setup_logging(self) -> logging.Logger:
        """Configuration du système de logging"""
        logger = logging.getLogger('GitAutomation')
        logger.setLevel(logging.INFO)
        
        # Création du handler pour fichier
        fh = logging.FileHandler(f'git_automation_{datetime.now().strftime("%Y%m%d")}.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
        return logger

    def _execute_command(self, command: list) -> tuple[int, str, str]:
        """Exécute une commande Git et retourne le résultat"""
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = process.communicate()
            
            if self.logger:
                self.logger.info(f"Commande exécutée: {' '.join(command)}")
                if stdout: self.logger.info(f"Sortie: {stdout}")
                if stderr: self.logger.warning(f"Erreur: {stderr}")
                
            return process.returncode, stdout, stderr
        except Exception as e:
            if self.logger:
                self.logger.error(f"Erreur lors de l'exécution de la commande: {str(e)}")
            return 1, "", str(e)

    def git_status(self) -> Optional[str]:
        """Vérifie le status du repository"""
        code, stdout, stderr = self._execute_command(['git', 'status'])
        return stdout if code == 0 else None

    def git_add_all(self) -> bool:
        """Ajoute tous les fichiers modifiés"""
        code, _, _ = self._execute_command(['git', 'add', '.'])
        return code == 0

    def git_commit(self, message: str) -> bool:
        """Effectue un commit avec le message fourni"""
        code, _, _ = self._execute_command(['git', 'commit', '-m', message])
        return code == 0

    def git_push(self) -> bool:
        """Push les modifications vers le repository distant"""
        code, _, _ = self._execute_command(['git', 'push'])
        return code == 0

    def execute_workflow(self) -> None:
        """Exécute le workflow Git complet"""
        print("\n=== Status actuel du repository ===")
        status = self.git_status()
        if status:
            print(status)
        
        confirmation = input("\nVoulez-vous continuer avec le commit ? (o/n): ")
        if confirmation.lower() != 'o':
            print("Opération annulée")
            return

        if self.git_add_all():
            print("\nFichiers ajoutés avec succès")
            
            commit_message = input("\nEntrez votre message de commit: ")
            if self.git_commit(commit_message):
                print("\nCommit effectué avec succès")
                
                push_confirm = input("\nVoulez-vous pusher les modifications ? (o/n): ")
                if push_confirm.lower() == 'o':
                    if self.git_push():
                        print("\nPush effectué avec succès")
                    else:
                        print("\nErreur lors du push")
            else:
                print("\nErreur lors du commit")
        else:
            print("\nErreur lors de l'ajout des fichiers")

if __name__ == "__main__":
    # Exemple d'utilisation
    git_automation = GitAutomation(enable_logging=True)
    git_automation.execute_workflow()