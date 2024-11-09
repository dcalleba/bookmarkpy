import os
import fnmatch
import logging
from datetime import datetime
import unittest
from typing import List

class DirectoryComparer:
    """Classe pour comparer les fichiers .md entre deux répertoires."""
    
    def __init__(self, dir1: str, dir2: str, enable_logging: bool = True):
        """
        Initialise le comparateur de répertoires.
        
        Args:
            dir1: Chemin du premier répertoire
            dir2: Chemin du second répertoire
            enable_logging: Active ou désactive les logs
        """
        self.dir1 = dir1
        self.dir2 = dir2
        
        if enable_logging:
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                filename=f"directory_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            )
        else:
            logging.disable(logging.CRITICAL)

    def compare_directories(self) -> List[str]:
        """
        Compare les fichiers .md dans les deux répertoires.
        
        Returns:
            Liste des différences trouvées
        """
        differences = []
        self._compare(self.dir1, self.dir2, differences)
        logging.info(f"Comparaison terminée : {len(differences)} différences trouvées")
        return differences

    def _compare(self, dir1: str, dir2: str, differences: List[str]) -> None:
        """
        Méthode privée pour comparer récursivement les répertoires.
        """
        items_dir1 = self._get_md_files(dir1)
        items_dir2 = self._get_md_files(dir2)

        # Vérification des fichiers de dir1 vers dir2
        for item in items_dir1:
            relative_path = os.path.relpath(item, dir1)
            corresponding_file = os.path.join(dir2, relative_path)
            
            if not os.path.exists(corresponding_file):
                message = f'Présent dans dir1, absent dans dir2: {relative_path}'
                differences.append(message)
                logging.warning(message)
            else:
                size1 = os.path.getsize(item)
                size2 = os.path.getsize(corresponding_file)
                if size1 != size2:
                    message = f'Différence de taille: {relative_path} ({size1} octets dans {dir1}, {size2} octets dans {dir2})'
                    differences.append(message)
                    logging.info(message)

        # Vérification des fichiers de dir2 vers dir1
        for item in items_dir2:
            relative_path = os.path.relpath(item, dir2)
            corresponding_file = os.path.join(dir1, relative_path)
            if not os.path.exists(corresponding_file):
                message = f'Présent dans dir2, absent dans dir1: {relative_path}'
                differences.append(message)
                logging.warning(message)

    def _get_md_files(self, directory: str) -> List[str]:
        """
        Récupère tous les fichiers .md dans un répertoire et ses sous-répertoires.
        
        Args:
            directory: Chemin du répertoire à analyser
            
        Returns:
            Liste des chemins des fichiers .md
        """
        md_files = []
        for root, _, files in os.walk(directory):
            for filename in fnmatch.filter(files, '*.md'):
                md_files.append(os.path.join(root, filename))
        return md_files


class TestDirectoryComparer(unittest.TestCase):
    """Classe de tests unitaires pour DirectoryComparer."""
    
    def setUp(self):
        # Création des répertoires de test
        self.test_dir1 = "test_dir1"
        self.test_dir2 = "test_dir2"
        os.makedirs(self.test_dir1, exist_ok=True)
        os.makedirs(self.test_dir2, exist_ok=True)

    def tearDown(self):
        # Nettoyage des répertoires de test
        import shutil
        shutil.rmtree(self.test_dir1)
        shutil.rmtree(self.test_dir2)

    def test_compare_directories(self):
        # Création de fichiers de test
        with open(os.path.join(self.test_dir1, "test1.md"), "w") as f:
            f.write("Test content 1")
        with open(os.path.join(self.test_dir2, "test1.md"), "w") as f:
            f.write("Test content 2")
        
        comparer = DirectoryComparer(self.test_dir1, self.test_dir2, enable_logging=False)
        differences = comparer.compare_directories()
        
        self.assertTrue(len(differences) > 0)


if __name__ == "__main__":
    # Exemple d'utilisation
    import sys
    
    if len(sys.argv) == 3:
        dir1 = sys.argv[1]
        dir2 = sys.argv[2]
    else:
        dir1 = "/users/danielcallebaut/desktop/obsimind"
        dir2 = "/users/danielcallebaut/desktop/obsimind_imgcomp"
    
    if not os.path.exists(dir1) or not os.path.exists(dir2):
        print("Erreur : Un des répertoires spécifiés n'existe pas.")
        sys.exit(1)
        
    comparer = DirectoryComparer(dir1, dir2)
    differences = comparer.compare_directories()
    
    if differences:
        print("Différences trouvées :")
        for diff in differences:
            print(f"- {diff}")
    else:
        print("Aucune différence trouvée.")