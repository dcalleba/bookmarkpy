import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import logging
from typing import List, Optional

class GmailSender:
    def __init__(self):
        """Initialise la connexion Gmail en chargeant les credentials depuis .env"""
        # Configuration du logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        # Chargement des variables d'environnement
        load_dotenv()
        self.email = os.getenv("GMAIL_USER")
        self.password = os.getenv("GMAIL_PASSWORD")
        print (self.email)
        print (self.password)
        if not self.email or not self.password:
            raise ValueError("Les credentials Gmail ne sont pas configurés dans le fichier .env")

    def send_email(self, 
                   recipients: List[str],
                   subject: str,
                   body: str,
                   attachments: Optional[List[str]] = None,
                   is_html: bool = False) -> bool:
        """Envoie un email via Gmail"""
        try:
            message = MIMEMultipart()
            message["From"] = self.email
            message["To"] = ", ".join(recipients)
            message["Subject"] = subject

            # Ajout du corps du message
            content_type = "html" if is_html else "plain"
            message.attach(MIMEText(body, content_type, 'utf-8'))

            # Gestion des pièces jointes
            if attachments:
                for file_path in attachments:
                    if os.path.exists(file_path):
                        with open(file_path, "rb") as attachment:
                            part = MIMEBase("application", "octet-stream")
                            part.set_payload(attachment.read())
                            encoders.encode_base64(part)
                            filename = os.path.basename(file_path)
                            part.add_header(
                                "Content-Disposition",
                                f"attachment; filename= {filename}"
                            )
                            message.attach(part)
                            self.logger.info(f"Pièce jointe ajoutée: {filename}")

            # Connexion et envoi
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(message)
                self.logger.info("Email envoyé avec succès")
                return True

        except Exception as e:
            self.logger.error(f"Erreur lors de l'envoi de l'email: {str(e)}")
            return False

if __name__ == "__main__":
    # Exemple d'utilisation
    sender = GmailSender()
    
    success = sender.send_email(
        recipients=["daniel@callebaut.org"],
        subject="Test d'envoi",
        body="Ceci est un test",
        attachments=["document.pdf"]
    )
    
    print(f"Statut de l'envoi: {'Succès' if success else 'Échec'}")