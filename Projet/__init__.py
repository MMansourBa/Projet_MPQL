from datetime import timedelta, datetime
from typing import List, Optional

from Changement.__init__ import Changement
from Equipe.__init__ import Equipe
from Jalon.__init__ import Jalon
from Membre import Membre
from NotificationContext import NotificationContext
from NotificationStrategy.__init__ import NotificationStrategy
from Risque.__init__ import Risque
from Tache.__init__ import Tache


class Projet:
    def __init__(self, nom: str, description: str, date_debut: datetime, date_fin: datetime, budget: float):
        self.nom = nom
        self.description = description
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.budget = budget
        self.taches: List[Tache] = []
        self.equipe = Equipe()
        self.risques: List[Risque] = []
        self.jalons: List[Jalon] = []
        self.version: int = 1
        self.changements: List[Changement] = []
        self.chemin_critique: List[Tache] = []
        self.notification_context: Optional[NotificationContext] = None

    def set_notification_strategy(self, strategy: NotificationStrategy):
        self.notification_context = NotificationContext(strategy)

    def ajouter_tache(self, tache: Tache):
        self.taches.append(tache)
        self.notifier(f"Nouvelle tâche ajoutée: {tache.nom}")

    def ajouter_membre_equipe(self, membre: Membre):
        self.equipe.ajouter_membre(membre)
        self.notifier(f"{membre.nom} a été ajouté à l'équipe")

    def definir_budget(self, budget: float):
        self.budget = budget
        self.notifier(f"Le budget du projet a été défini: {self.budget} Unité Monetaire")

    def ajouter_risque(self, risque: Risque):
        self.risques.append(risque)
        self.notifier(f"Nouveau risque ajouté: {risque.description}")

    def ajouter_jalon(self, jalon: Jalon):
        self.jalons.append(jalon)
        self.notifier(f"Nouveau jalon ajouté: {jalon.nom}")

    def enregistrer_changement(self, description: str):
        changement = Changement(description, self.version, datetime.now())
        self.changements.append(changement)
        self.version += 1
        self.notifier(f"Changement enregistré: {description} (version {changement.version})")

    def generer_rapport_performance(self) -> str:
        rapport = f"Rapport d'activités du Projet '{self.nom}'\n"
        rapport += f"Version: {self.version}\n"
        rapport += f"Dates: {self.date_debut} à {self.date_fin}\n"
        rapport += f"Budget : {self.budget} Unité Monetaire\n"
        rapport += "Équipe:\n"
        for membre in self.equipe.obtenir_membres():
            rapport += f"{membre.nom} ({membre.role})\n"
        rapport += "Tâches:\n"
        for tache in self.taches:
            rapport += f"{tache.nom} ({tache.date_debut} à {tache.date_fin}), Responsable: {tache.responsable.nom}, Statut: {tache.statut}\n"
        rapport += "Jalons:\n"
        for jalon in self.jalons:
            rapport += f"{jalon.nom} ({jalon.date})\n"
        rapport += "Risques:\n"
        for risque in self.risques:
            rapport += f"{risque.description} (Probabilité: {risque.probabilite}, Impact: {risque.impact})\n"
        rapport += "Chemin Critique:\n"
        for tache in self.chemin_critique:
            rapport += f"{tache.nom} ({tache.date_debut} à {tache.date_fin})\n"
        return rapport

    def notifier(self, message: str):
        if self.notification_context:
            self.notification_context.notifier(message, self.equipe.obtenir_membres())

    def calculer_chemin_critique(self):
        # Calculer les temps au plus tôt
        for tache in self.taches:
            if not tache.dependances:
                tache.ES = self.date_debut
                tache.EF = tache.ES + timedelta(days=tache.duree())
            else:
                tache.ES = max(dep.EF for dep in tache.dependances)
                tache.EF = tache.ES + timedelta(days=tache.duree())
            print(f"Tâche {tache.nom} : ES = {tache.ES}, EF = {tache.EF}")  # Débogage

        # Initialiser LF pour la dernière tâche
        fin_projet = max(tache.EF for tache in self.taches)
        for tache in self.taches:
            if tache.EF == fin_projet:
                tache.LF = tache.EF
                tache.LS = tache.LF - timedelta(days=tache.duree())
            print(f"Tâche {tache.nom} initialisée pour LF/LS: LS = {tache.LS}, LF = {tache.LF}")  # Débogage

        # Calculer les temps au plus tard pour toutes les tâches
        for tache in reversed(self.taches):
            if tache.LF is None:
                tache.LF = min(dep.LS for dep in self.taches if tache in dep.dependances)
                tache.LS = tache.LF - timedelta(days=tache.duree())
            print(f"Tâche {tache.nom} : LS = {tache.LS}, LF = {tache.LF}")  # Débogage

        # Déterminer le chemin critique
        self.chemin_critique = [tache for tache in self.taches if (tache.LF - tache.EF).days == 0]
        print(f"Chemin critique: {[tache.nom for tache in self.chemin_critique]}")  # Débogage