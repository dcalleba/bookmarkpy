import json
import os

# Fonction pour trouver un dossier spécifique par son nom et vider son contenu
def find_and_clear_folder(bookmark_folder, folder_name):
    if bookmark_folder['type'] == 'folder' and bookmark_folder['name'] == folder_name:
        bookmark_folder['children'] = []  # Vide le contenu du dossier
        return bookmark_folder
    for item in bookmark_folder.get('children', []):
        if item['type'] == 'folder':
            found_folder = find_and_clear_folder(item, folder_name)
            if found_folder:
                return found_folder
    return None

# Fonction pour lire le contenu du fichier .md et extraire les liens
def extract_links_from_md(md_file_path):
    if not os.path.exists(md_file_path):
        print(f"Le fichier {md_file_path} n'existe pas.")
        return []

    with open(md_file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()
    
    links = []
    for line in content:
        if line.startswith('[') and '](' in line:
            # Extrait le texte du lien et l'URL
            text = line.split('](')[0].strip('[')
            url = line.split('](')[1].strip(')\n')
            links.append({'name': text, 'type': 'url', 'url': url})
    return links

# Fonction principale pour mettre à jour les favoris dans Chrome
def update_chrome_bookmarks(folder_list):
    # Chemin vers le fichier des favoris de Chrome
    chrome_bookmarks_path = os.path.expanduser(
        "~/Library/Application Support/Google/Chrome/Default/Bookmarks"  # macOS
        # "C:\\Users\\VotreNomDUtilisateur\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Bookmarks"  # Windows
        # "~/.config/google-chrome/Default/Bookmarks"  # Linux
    )

    if not os.path.exists(chrome_bookmarks_path):
        print(f"Le fichier de favoris {chrome_bookmarks_path} n'existe pas.")
        return

    # Charger le fichier JSON des favoris
    with open(chrome_bookmarks_path, 'r', encoding='utf-8') as file:
        bookmarks_data = json.load(file)

    # Traiter chaque sous-dossier dans la liste
    for folder_to_update in folder_list:
        # Chemin complet du fichier Markdown correspondant
        md_file_path = os.path.expanduser(f"~/Desktop/obsimind/new/Fav_{folder_to_update}.md")

        # Trouver et vider le sous-dossier
        target_folder = find_and_clear_folder(bookmarks_data['roots']['bookmark_bar'], folder_to_update)

        if target_folder:
            # Extraire les liens du fichier Markdown
            new_links = extract_links_from_md(md_file_path)

            if new_links:
                # Ajouter les nouveaux liens au sous-dossier
                target_folder['children'].extend(new_links)
                print(f"Le dossier '{folder_to_update}' a été vidé et mis à jour avec {len(new_links)} nouveaux liens de {md_file_path}.")
            else:
                print(f"Aucun lien trouvé dans {md_file_path}.")
        else:
            print(f"Le dossier '{folder_to_update}' n'a pas été trouvé.")

    # Sauvegarder les modifications dans le fichier des favoris de Chrome
    with open(chrome_bookmarks_path, 'w', encoding='utf-8') as file:
        json.dump(bookmarks_data, file, ensure_ascii=False, indent=4)

    print(f"Les favoris de Chrome ont été mis à jour avec les nouveaux liens.")

# Liste des sous-dossiers à traiter
folders_to_update = ["AAA"]  # Ajoutez ici tous les sous-dossiers que vous souhaitez mettre à jour

# Exécuter la mise à jour des favoris pour la liste de sous-dossiers
update_chrome_bookmarks(folders_to_update)
