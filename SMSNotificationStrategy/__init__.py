from Membre import Membre
from NotificationStrategy.__init__ import NotificationStrategy


class SMSNotificationStrategy(NotificationStrategy):
    # Envoyer des notifications par SMS
    def envoyer(self, message: str, destinataire: Membre):
        print(f"Notification envoyée à {destinataire.nom} par SMS: {message}")