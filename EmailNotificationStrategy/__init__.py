from Membre import Membre
from NotificationStrategy.__init__ import NotificationStrategy


class EmailNotificationStrategy(NotificationStrategy):
    # Envoyer des notifications par email
    def envoyer(self, message: str, destinataire: Membre):
        print(f"Notification envoyée à {destinataire.nom} par email: {message}")