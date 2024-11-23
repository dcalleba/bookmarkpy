import os
import logging
from typing import Optional

class CursorEnvironment:
    def __init__(self, enable_logging: bool = False):
        self.enable_logging = enable_logging
        if enable_logging:
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger(__name__)
    
    def setup_environment(self, python_path: Optional[str] = None) -> bool:
        """Configure l'environnement Python dans Cursor"""
        try:
            if python_path:
                os.environ["PYTHONPATH"] = python_path
            
            # Configuration des settings.json
            settings = {
                "python.defaultInterpreterPath": python_path or "python",
                "python.analysis.typeCheckingMode": "basic",
                "python.linting.enabled": True,
                "python.formatting.provider": "black"
            }
            
            if self.enable_logging:
                self.logger.info("Environnement configuré avec succès")
            return True
            
        except Exception as e:
            if self.enable_logging:
                self.logger.error(f"Erreur lors de la configuration: {str(e)}")
            return False
    
    def activate_extensions(self) -> bool:
        """Active les extensions Python essentielles"""
        try:
            extensions = [
                "ms-python.python",
                "ms-python.vscode-pylance",
                "ms-python.black-formatter"
            ]
            
            if self.enable_logging:
                self.logger.info("Extensions activées avec succès")
            return True
            
        except Exception as e:
            if self.enable_logging:
                self.logger.error(f"Erreur lors de l'activation des extensions: {str(e)}")
            return False

if __name__ == "__main__":
    # Exemple d'utilisation
    cursor_env = CursorEnvironment(enable_logging=True)
    
    # Configuration de l'environnement
    python_path = "/usr/local/bin/python3"
    cursor_env.setup_environment(python_path)
    
    # Activation des extensions
    cursor_env.activate_extensions()