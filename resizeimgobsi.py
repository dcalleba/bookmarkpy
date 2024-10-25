import os
from PIL import Image

def compress_image(input_file_path, output_file_path, quality=85):
    """
    Compresse une image pour réduire sa taille.
    
    :param input_file_path: Chemin du fichier image d'entrée.
    :param output_file_path: Chemin du fichier image de sortie.
    :param quality: Qualité de l'image de sortie (de 0 à 100).
    """
    try:
        with Image.open(input_file_path) as img:
            # Convertir l'image en mode RGB (si ce n'est pas déjà le cas)
            img = img.convert("RGB")
            img.save(output_file_path, "JPEG", optimize=True, quality=quality)
    except Exception as e:
        print(f"Erreur lors de la compression de {input_file_path}: {e}")

def load_compressed_images_log(log_file_path):
    """
    Charge la liste des images déjà compressées à partir d'un fichier de log.
    
    :param log_file_path: Chemin du fichier de log.
    :return: Un set contenant les chemins des images déjà compressées.
    """
    if not os.path.exists(log_file_path):
        return set()
    
    with open(log_file_path, 'r') as f:
        compressed_images = set(line.strip() for line in f)
    
    return compressed_images

def save_compressed_image_log(log_file_path, image_path):
    """
    Enregistre le chemin d'une image compressée dans le fichier de log.
    
    :param log_file_path: Chemin du fichier de log.
    :param image_path: Chemin de l'image compressée.
    """
    with open(log_file_path, 'a') as f:
        f.write(image_path + '\n')

def compress_images_in_folder(folder_path, output_folder=None, quality=85):
    """
    Parcours tous les sous-dossiers et compresse toutes les images dans le répertoire donné.
    
    :param folder_path: Chemin du répertoire contenant les images à compresser.
    :param output_folder: Chemin du répertoire de sortie pour les images compressées.
    :param quality: Qualité de l'image de sortie (de 0 à 100).
    """
    log_file_path = os.path.join(folder_path, 'compressed_images.log')
    compressed_images = load_compressed_images_log(log_file_path)
    
    for root, _, files in os.walk(folder_path):
        # Vérifie si le dossier courant ou l'un de ses parents a le suffixe "_ori"
        if any(part.endswith('_photo') for part in root.split(os.sep)):
            print(f"Dossier ignoré (suffixe '_photo' détecté) : {root}")
            continue
        
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                input_file_path = os.path.join(root, file)
                
                # Vérifie si l'image a déjà été compressée
                if input_file_path in compressed_images:
                    print(f"Image déjà compressée, ignorée : {input_file_path}")
                    continue
                
                # Déterminer le chemin de sortie
                if output_folder:
                    relative_path = os.path.relpath(root, folder_path)
                    output_file_dir = os.path.join(output_folder, relative_path)
                    os.makedirs(output_file_dir, exist_ok=True)
                    output_file_path = os.path.join(output_file_dir, file)
                else:
                    output_file_path = input_file_path
                
                # Compresser l'image
                compress_image(input_file_path, output_file_path, quality=quality)
                print(f"Image compressée : {output_file_path}")
                
                # Enregistrer le fichier dans le log
                save_compressed_image_log(log_file_path, input_file_path)

# Utilisation du script
vault_path = "/Users/danielcallebaut/Desktop/Md_clipper_ori"  # Remplacez par le chemin de votre vault Obsidian
output_folder = None  # Mettez à None pour écraser les fichiers originaux ou spécifiez un chemin pour enregistrer les fichiers compressés
compress_images_in_folder(vault_path, output_folder, quality=50)
