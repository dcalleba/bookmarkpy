from PIL import Image
import os
import logging
from datetime import datetime

def setup_logging():
    if not os.path.exists('logs'):
        os.makedirs('logs')
    log_file = f'logs/compression_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def is_hidden(path):
    # Vérifie si un chemin est caché
    basename = os.path.basename(path)
    return basename.startswith('.') or basename.startswith('_')

def compress_image(filepath):
    try:
        initial_size = os.path.getsize(filepath) / 1024
        
        with Image.open(filepath) as img:
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            max_size = 1600
            if max(img.size) > max_size:
                ratio = max_size / max(img.size)
                new_size = tuple(int(dim * ratio) for dim in img.size)
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            img.save(filepath, 'JPEG', quality=75, optimize=True)
        
        final_size = os.path.getsize(filepath) / 1024
        reduction = ((initial_size - final_size) / initial_size) * 100
        
        logging.info(f"Compressé : {filepath}")
        logging.info(f"Taille initiale : {initial_size:.2f}KB")
        logging.info(f"Taille finale : {final_size:.2f}KB")
        logging.info(f"Réduction : {reduction:.2f}%\n")
        
    except Exception as e:
        logging.error(f"Erreur lors de la compression de {filepath}: {str(e)}")

def compress_images_recursive(directory):
    valid_extensions = {'.jpg', '.jpeg', '.png'}
    total_files = 0
    processed_files = 0
    
    logging.info(f"Début du traitement du dossier : {directory}")
    
    # Parcours récursif en ignorant les dossiers cachés
    for root, dirs, files in os.walk(directory):
        # Modifier la liste dirs en place pour ignorer les dossiers cachés
        dirs[:] = [d for d in dirs if not is_hidden(os.path.join(root, d))]
        
        for filename in files:
            if is_hidden(filename):
                continue
                
            total_files += 1
            if any(filename.lower().endswith(ext) for ext in valid_extensions):
                filepath = os.path.join(root, filename)
                compress_image(filepath)
                processed_files += 1
    
    logging.info(f"\nStatistiques finales:")
    logging.info(f"Nombre total de fichiers trouvés : {total_files}")
    logging.info(f"Nombre d'images traitées : {processed_files}")

if __name__ == "__main__":
    setup_logging()
    # directory = "chemin/vers/votre/dossier/obsidian"
    directory = "/users/danielcallebaut/desktop/obsimind"
    
    try:
        compress_images_recursive(directory)
        logging.info("Compression terminée avec succès!")
    except Exception as e:
        logging.error(f"Erreur générale : {str(e)}")