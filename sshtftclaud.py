import paramiko
import os
from pathlib import Path

class SSHTransfert:
    def __init__(self, hostname, username, password=None, key_filename=None):
        """Initialisation de la connexion SSH"""
        self.hostname = hostname
        self.username = username
        self.password = password
        self.key_filename = key_filename
        self.client = None
        self.sftp = None

    def connecter(self):
        """Établir la connexion SSH et SFTP"""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            if self.key_filename:
                self.client.connect(
                    hostname=self.hostname,
                    username=self.username,
                    key_filename=self.key_filename
                )
            else:
                self.client.connect(
                    hostname=self.hostname,
                    username=self.username,
                    password=self.password
                )
            
            self.sftp = self.client.open_sftp()
            print("Connexion établie avec succès")
            
        except Exception as e:
            print(f"Erreur de connexion : {str(e)}")
            raise

    def envoyer_fichier(self, chemin_local, chemin_distant):
        """Envoyer un fichier vers le serveur distant"""
        try:
            self.sftp.put(chemin_local, chemin_distant)
            print(f"Fichier envoyé avec succès : {chemin_local} → {chemin_distant}")
        except Exception as e:
            print(f"Erreur lors de l'envoi du fichier : {str(e)}")

    def recevoir_fichier(self, chemin_distant, chemin_local):
        """Télécharger un fichier depuis le serveur distant"""
        try:
            self.sftp.get(chemin_distant, chemin_local)
            print(f"Fichier reçu avec succès : {chemin_distant} → {chemin_local}")
        except Exception as e:
            print(f"Erreur lors de la réception du fichier : {str(e)}")

    def envoyer_dossier(self, dossier_local, dossier_distant):
        """Envoyer un dossier complet vers le serveur distant"""
        try:
            # Créer le dossier distant s'il n'existe pas
            try:
                self.sftp.mkdir(dossier_distant)
            except:
                pass

            # Parcourir tous les fichiers du dossier local
            for root, dirs, files in os.walk(dossier_local):
                for name in files:
                    chemin_local = os.path.join(root, name)
                    chemin_relatif = os.path.relpath(chemin_local, dossier_local)
                    chemin_distant_complet = os.path.join(dossier_distant, chemin_relatif)
                    
                    # Créer les sous-dossiers distants si nécessaire
                    dossier_distant_parent = os.path.dirname(chemin_distant_complet)
                    try:
                        self.sftp.mkdir(dossier_distant_parent)
                    except:
                        pass
                    
                    self.envoyer_fichier(chemin_local, chemin_distant_complet)
                    
        except Exception as e:
            print(f"Erreur lors de l'envoi du dossier : {str(e)}")

    def fermer(self):
        """Fermer les connexions SFTP et SSH"""
        if self.sftp:
            self.sftp.close()
        if self.client:
            self.client.close()
        print("Connexions fermées")
        
# Exemple d'utilisation
if __name__ == "__main__":
    # Paramètres de connexion
    hostname = "opal6.opalstack.com"
    username = "dcallebaut"
    password = "Rueduciel,1"  # Ou utilisez key_filename pour l'authentification par clé
    
    # Création de l'instance
    ssh = SSHTransfert(hostname, username, password)
    
    try:
        # Connexion
        ssh.connecter()
        
        # Envoi d'un fichier
        #ssh.envoyer_fichier("/chemin/local/fichier.txt", "/chemin/distant/fichier.txt")
        
        # Réception d'un fichier
        #ssh.recevoir_fichier("/chemin/distant/fichier.txt", "/chemin/local/fichier_recu.txt")
        
        # Envoi d'un dossier complet
        ssh.envoyer_dossier("/users/danielcallebaut/bdj", "distant")
        
    finally:
        # Fermeture des connexions
        ssh.fermer()


