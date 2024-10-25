import json
import os

# Fonction pour trouver un dossier spécifique par son nom
def find_folder(bookmark_folder, folder_name):
    if bookmark_folder['type'] == 'folder' and bookmark_folder['name'] == folder_name:
        return bookmark_folder
    for item in bookmark_folder.get('children', []):
        if item['type'] == 'folder':
            found_folder = find_folder(item, folder_name)
            if found_folder:
                return found_folder
    return None

# Fonction pour extraire les liens de favoris avec leur chemin complet
def extract_bookmarks_with_path(bookmark_folder):
    bookmarks = []
    for item in bookmark_folder['children']:
        if item['type'] == 'url':
            bookmarks.append(f"[{item['name']}]({item['url']})")
    return bookmarks

# Fonction pour charger les liens existants dans le fichier Markdown
def load_existing_links(markdown_file_path):
    if not os.path.exists(markdown_file_path):
        return set()  # Retourne un ensemble vide si le fichier n'existe pas

    with open(markdown_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        # Extraction des URLs existantes dans le fichier Markdown
        existing_links = {line.split("](")[1].strip(")") for line in content.splitlines() if line.startswith("[")}
    return existing_links

# Fonction principale pour traiter une liste de sous-dossiers
def process_folders(folder_list):
    # Chemin vers le fichier des favoris de Chrome
    chrome_bookmarks_path = os.path.expanduser(
        "~/Library/Application Support/Google/Chrome/Default/Bookmarks"  # macOS
        # "C:\\Users\\VotreNomDUtilisateur\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Bookmarks"  # Windows
        # "~/.config/google-chrome/Default/Bookmarks"  # Linux
    )

    # Charger le fichier JSON des favoris
    with open(chrome_bookmarks_path, 'r', encoding='utf-8') as file:
        bookmarks_data = json.load(file)

    # Traiter chaque sous-dossier dans la liste
    for folder_to_extract in folder_list:
        # Nom du fichier Markdown basé sur le nom du sous-dossier
        filename = f"Fav_{folder_to_extract}.md"
        
        # Chemin complet du fichier Markdown dans votre vault Obsidian
        obsidian_vault_path = os.path.expanduser(f"~/Desktop/obsimind/new/{filename}")

        # Vérification si le fichier existe déjà et charger les liens existants
        existing_links = load_existing_links(obsidian_vault_path)

        # Trouver le sous-dossier
        target_folder = find_folder(bookmarks_data['roots']['bookmark_bar'], folder_to_extract)

        # Vérifier si le sous-dossier a été trouvé et extraire les favoris
        if target_folder:
            new_links = []
            for link in extract_bookmarks_with_path(target_folder):
                # Ajouter le lien s'il n'existe pas déjà dans le fichier Markdown
                url = link.split("](")[1].strip(")")
                if url not in existing_links:
                    new_links.append(link)
            
            # Trier les nouveaux liens par ordre alphabétique
            new_links.sort()

            # Si des nouveaux liens sont trouvés, les ajouter au fichier Markdown
            if new_links:
                with open(obsidian_vault_path, 'a', encoding='utf-8') as markdown_file:
                    markdown_file.write("\n".join(new_links))
                    markdown_file.write("\n")
                print(f"{len(new_links)} nouveaux liens ont été ajoutés au fichier {obsidian_vault_path} et triés alphabétiquement.")
            else:
                print(f"Aucun nouveau lien à ajouter pour '{folder_to_extract}'.")
        else:
            print(f"Le dossier '{folder_to_extract}' n'a pas été trouvé.")

# Liste des sous-dossiers à traiter
folders_to_process = ["AAA", "Bois", "Resto"]  # Ajoutez ici tous les sous-dossiers que vous souhaitez traiter

# Exécuter le traitement pour la liste de sous-dossiers
process_folders(folders_to_process)
