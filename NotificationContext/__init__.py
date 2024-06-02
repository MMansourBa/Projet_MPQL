from typing import List

from Membre import Membre
from NotificationStrategy.__init__ import NotificationStrategy


class NotificationContext:
    def __init__(self, strategy: NotificationStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: NotificationStrategy):
        self._strategy = strategy

    def notifier(self, message: str, destinataires: List[Membre]):
        for destinataire in destinataires:
            self._strategy.envoyer(message, destinataire)