def check_permissions(sftp, path):
    try:
        sftp.stat(path)
        return True
    except IOError as e:
        if "Permission denied" in str(e):
            print(f"Erreur de permission pour accéder à {path}")
            return False
        return True  # Le chemin n'existe pas, mais on peut probablement le créer

# Dans la fonction principale, avant mkdir_p :
if not check_permissions(sftp, os.path.dirname(remote_path)):
    print("Vous n'avez pas les permissions nécessaires pour créer ce dossier.")
    return