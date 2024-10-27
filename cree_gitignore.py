import os
#daniel

def create_gitignore():
    # Spécifier le chemin du répertoire courant
    current_directory = os.getcwd()

    # Lister tous les fichiers et dossiers dans le répertoire courant
    all_files = os.listdir(current_directory)

    # Demander à l'utilisateur quels fichiers ne pas ignorer
    print("Entrez les noms des fichiers à ne PAS ignorer (séparés par des espaces):
          ")
    files_to_track = input().split()

    # Créer un fichier .gitignore
    with open('.gitignore', 'w') as gitignore_file:
        for filename in all_files:
            # Ignorer le fichier .gitignore lui-même et les fichiers que l'utilisateur veut suivre
            if filename != '.gitignore' and filename not in files_to_track:
                gitignore_file.write(f'{filename}\n')

    print("Le fichier .gitignore a été créé avec tous les fichiers du répertoire courant, sauf ceux spécifiés.")
    print("Fichiers non ignorés:", ', '.join(files_to_track))

# Exécuter la fonction
create_gitignore()