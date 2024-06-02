from Membre import Membre


class NotificationStrategy:
    # Envoyer des notifications
    def envoyer(self, message: str, destinataire: Membre):
        raise NotImplementedError("Cette méthode doit être implémentée par les sous-classes")