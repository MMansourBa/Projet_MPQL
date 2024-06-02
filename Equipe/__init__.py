from typing import List
from Membre import Membre


class Equipe:
    def __init__(self):
        self.membres: List[Membre] = []

    def ajouter_membre(self, membre: Membre):
        self.membres.append(membre)

    def obtenir_membres(self) -> List[Membre]:
        return self.membres