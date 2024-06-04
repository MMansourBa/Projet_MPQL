from datetime import datetime, timedelta
from typing import Optional, List

from Membre import Membre


class Tache:
    def __init__(self, nom: str, description: str, date_debut: datetime, date_fin: datetime, responsable: Membre,
                 statut: str):
        self.nom = nom
        self.description = description
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.responsable = responsable
        self.statut = statut
        self.dependances: List['Tache'] = []
        #Ajout des attributs supplementaires pour pouvoir
        # calculer le chemin critique apres dans la classe Projet
        self.ES: Optional[datetime] = None #Date de début au plus tôt
        self.EF: Optional[datetime] = None #Date de fin au plus tôt
        self.LS: Optional[datetime] = None #Date de début au plus tard
        self.LF: Optional[datetime] = None #Date de fin au plus tard

    def ajouter_dependance(self, tache: 'Tache'):
        self.dependances.append(tache)

    def mettre_a_jour_statut(self, statut: str):
        self.statut = statut

    def duree(self) -> int:
        return (self.date_fin - self.date_debut).days