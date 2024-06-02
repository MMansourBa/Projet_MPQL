from Membre import Membre
from NotificationStrategy.__init__ import NotificationStrategy


class PushNotificationStrategy(NotificationStrategy):
    def envoyer(self, message: str, destinataire: Membre):
        print(f"Notification envoyée à {destinataire.nom} par notification push: {message}")