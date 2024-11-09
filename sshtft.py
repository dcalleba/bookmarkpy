import paramiko
import os
import stat

def mkdir_p(sftp, remote_directory):
    """Crée un répertoire distant et tous les répertoires parents nécessaires"""
    if remote_directory.startswith('/'):
        path_parts = remote_directory.split('/')[1:]  # Ignore le premier élément vide
        current_dir = "/"
    else:
        path_parts = remote_directory.split('/')
        current_dir = ""

    for dir_part in path_parts:
        if dir_part:
            current_dir = f"{current_dir}/{dir_part}" if current_dir else dir_part
            try:
                sftp.stat(current_dir)
            except IOError:
                print(f"Tentative de création du répertoire distant : {current_dir}")
                sftp.mkdir(current_dir)

def ssh_transfer_folders(host, username, password, local_path, remote_path, mode='upload'):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sftp = None

    try:
        ssh.connect(host, username=username, password=password)
        sftp = ssh.open_sftp()

        if mode == 'upload':
            try:
                mkdir_p(sftp, remote_path)
            except IOError as e:
                print(f"Erreur lors de la création du répertoire {remote_path}: {str(e)}")
                return

            def upload_folder(local_folder, remote_folder):
                for item in os.listdir(local_folder):
                    local_item_path = os.path.join(local_folder, item)
                    remote_item_path = f"{remote_folder}/{item}"
                    if os.path.isfile(local_item_path):
                        sftp.put(local_item_path, remote_item_path)
                        print(f"Fichier uploadé : {local_item_path} -> {remote_item_path}")
                    elif os.path.isdir(local_item_path):
                        try:
                            mkdir_p(sftp, remote_item_path)
                            upload_folder(local_item_path, remote_item_path)
                        except IOError as e:
                            print(f"Erreur lors de l'upload de {local_item_path}: {str(e)}")

            upload_folder(local_path, remote_path)
            print("Upload terminé.")

        elif mode == 'download':
            def download_folder(remote_folder, local_folder):
                if not os.path.exists(local_folder):
                    os.makedirs(local_folder)
                try:
                    for item in sftp.listdir(remote_folder):
                        remote_item_path = f"{remote_folder}/{item}"
                        local_item_path = os.path.join(local_folder, item)
                        if stat.S_ISDIR(sftp.stat(remote_item_path).st_mode):
                            download_folder(remote_item_path, local_item_path)
                        else:
                            sftp.get(remote_item_path, local_item_path)
                            print(f"Fichier téléchargé : {remote_item_path} -> {local_item_path}")
                except IOError as e:
                    print(f"Erreur lors de l'accès au dossier distant {remote_folder}: {str(e)}")

            download_folder(remote_path, local_path)
            print("Téléchargement terminé.")

    except paramiko.AuthenticationException:
        print("Erreur d'authentification. Vérifiez vos identifiants.")
    except paramiko.SSHException as ssh_exception:
        print(f"Erreur SSH: {str(ssh_exception)}")
    except Exception as e:
        print(f"Une erreur inattendue est survenue : {str(e)}")

    finally:
        if sftp:
            sftp.close()
        if ssh:
            ssh.close()
# Exemple d'utilisation
host = 'opal6.opalstack.com'
username = 'dcallebaut'
password = 'Rueduciel,1'
local_path = '/users/danielcallebaut/bdj'
remote_path = 'bdj_original'

# Pour uploader un dossier
ssh_transfer_folders(host, username, password, local_path, remote_path, mode='upload')

# Pour télécharger un dossier
#ssh_transfer_folders(host, username, password, local_path, remote_path, mode='download')