"""
Ce module contient les fonctionnalités principales de l'application.
"""

from datetime import datetime, timedelta
from typing import List, Optional


# 1. CLASSES PRINCIPALES
class Membre:
    """
    Classe représentant un membre d'un projet.

    Attributes:
        nom (str): Le nom du membre.
        role (str): Le rôle du membre dans le projet.
    """

    def __init__(self, nom: str, role: str):
        """
        Initialise un nouveau membre avec un nom et un rôle.

        Args:
            nom (str): Le nom du membre.
            role (str): Le rôle du membre.
        """
        self.nom = nom
        self.role = role


class Equipe:
    """
    Les methodes dela classe Equipe
    """

    def __init__(self):
        self.membres: List[Membre] = []

    def ajouter_membre(self, membre: Membre):
        """
        Ajout d'un membre
        """
        self.membres.append(membre)

    def obtenir_membres(self) -> List[Membre]:
        """
        Liste membre
        """
        return self.membres


class Tache:
    """
    Classe représentant une tache.
    """

    def __init__(
        self,
        nom: str,
        description: str,
        date_debut: datetime,
        date_fin: datetime,
        responsable: Membre,
        statut: str,
    ):
        self.nom = nom
        self.description = description
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.responsable = responsable
        self.statut = statut
        self.dependances: List["Tache"] = []
        self.es: Optional[datetime] = None
        self.ef: Optional[datetime] = None
        self.ls: Optional[datetime] = None
        self.lf: Optional[datetime] = None

    def ajouter_dependance(self, tache: "Tache"):
        """
        Ajout dependance
        """
        self.dependances.append(tache)

    def mettre_a_jour_statut(self, statut: str):
        """
        Mettre a jour un dependance
        """
        self.statut = statut

    def duree(self) -> int:
        """
        Duree
        """
        return (self.date_fin - self.date_debut).days


class Jalon:
    """
    Classe Jalon
    """

    def __init__(self, nom: str, date: datetime):
        self.nom = nom
        self.date = date


class Risque:
    """
    Classe Risque
    """

    def __init__(self, description: str, probabilite: float, impact: str):
        self.description = description
        self.probabilite = probabilite
        self.impact = impact


class Changement:
    """
    Classe Changement
    """

    def __init__(self, description: str, version: int, date: datetime):
        self.description = description
        self.version = version
        self.date = date


# 2. GESTION DES NOTIFICATIONS
class NotificationStrategy:
    """
    Classe de base pour les stratégies de notification.
    """

    def envoyer(self, message: str, destinataire: Membre):
        """
        Envoie une notification à un membre..
        """
        raise NotImplementedError(
            "Cette méthode doit être implémentée par les sous-classes"
        )


class EmailNotificationStrategy(NotificationStrategy):
    """
    Stratégie de notification par email.
    """

    def envoyer(self, message: str, destinataire: Membre):
        """
        Envoie une notification par email.
        """
        print(f"Notification envoyée à {destinataire.nom}"
              f" par email: {message}")


class SMSNotificationStrategy(NotificationStrategy):
    """
    Envoie une notification par SMS.
    """

    def envoyer(self, message: str, destinataire: Membre):
        print(f"Notification envoyée à {destinataire.nom}"
              f" par SMS: {message}")


class PushNotificationStrategy(NotificationStrategy):
    """
    Envoie une notification par Push.
    """

    def envoyer(self, message: str, destinataire: Membre):
        print(
            f"Notification envoyée à {destinataire.nom}"
            f" par notification push: {message}"
        )


class NotificationContext:
    """
    Classe NotificationContext qui utilise
    une instance de NotificationStrategy
    """

    def __init__(self, strategy: NotificationStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: NotificationStrategy):
        """
        Définir la stratégie de notification
        à utiliser pour un projet.
        """
        self._strategy = strategy

    def notifier(self, message: str, destinataires: List[Membre]):
        """
        Définir la stratégie de notification à utiliser pour un projet.
        """
        for destinataire in destinataires:
            self._strategy.envoyer(message, destinataire)


class Projet:
    """
    Classe representant un projet.
    """

    def __init__(
        self,
        nom: str,
        description: str,
        date_debut: datetime,
        date_fin: datetime,
        budget: float,
    ):
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
        """
        Methode set_notification_strategy
        """
        self.notification_context = NotificationContext(strategy)

    def ajouter_tache(self, tache: Tache):
        """
        Ajouter une nouvelle tâche à la liste des tâches du projet
        """
        self.taches.append(tache)
        self.notifier(f"Nouvelle tâche ajoutée: {tache.nom}")

    def ajouter_membre_equipe(self, membre: Membre):
        """
        Ajouter membre dans l'equipe
        """
        self.equipe.ajouter_membre(membre)
        self.notifier(f"{membre.nom} a été ajouté à l'équipe")

    def definir_budget(self, budget: float):
        """
        Definir le budget du projet
        """
        self.budget = budget
        self.notifier(
            f"Le budget du projet a été défini: {self.budget} Unité Monetaire"
        )

    def ajouter_risque(self, risque1: Risque):
        """
        Ajouter risque
        """
        self.risques.append(risque1)
        self.notifier(f"Nouveau risque ajouté: {risque1.description}")

    def ajouter_jalon(self, jalon1: Jalon):
        """
        Ajouter jalon
        """
        self.jalons.append(jalon1)
        self.notifier(f"Nouveau jalon ajouté: {jalon1.nom}")

    def enregistrer_changement(self, description: str):
        """
        Enregistrer un changement
        """
        changement = Changement(description, self.version, datetime.now())
        self.changements.append(changement)
        self.version += 1
        self.notifier(
            f"Changement enregistré: "
            f"{description}"
            f" (version {changement.version})"
        )

    def generer_rapport_performance(self) -> str:
        """
        Generer un rapport des activites du projet
        """
        rapport1 = f"Rapport d'activités du Projet '{self.nom}'\n"
        rapport1 += f"Version: {self.version}\n"
        rapport1 += f"Dates: {self.date_debut} à {self.date_fin}\n"
        rapport1 += f"Budget : {self.budget} Unité Monetaire\n"
        rapport1 += "Équipe:\n"
        for membre in self.equipe.obtenir_membres():
            rapport1 += f"{membre.nom} ({membre.role})\n"
        rapport1 += "Tâches:\n"
        for tache in self.taches:
            rapport1 += (
                f"{tache.nom} ({tache.date_debut} "
                f"à {tache.date_fin}), "
                f"Responsable: {tache.responsable.nom}, "
                f"Statut: {tache.statut}\n"
            )
        rapport1 += "Jalons:\n"
        for jalon1 in self.jalons:
            rapport1 += f"{jalon1.nom} ({jalon1.date})\n"
        rapport1 += "Risques:\n"
        for risque1 in self.risques:
            rapport1 += (
                f"{risque1.description} "
                f"(Probabilité: {risque1.probabilite}, "
                f"Impact: {risque1.impact})\n"
            )
        rapport1 += "Chemin Critique:\n"
        for tache in self.chemin_critique:
            rapport1 += (f"{tache.nom} ({tache.date_debut}"
                         f" à {tache.date_fin})\n")
        return rapport1

    def notifier(self, message: str):
        """
        Envoyer un message de notification
        à tous les membres de l'équipe du projet
        """
        if self.notification_context:
            self.notification_context.notifier(message,
                                               self.equipe.obtenir_membres())

    def calculer_chemin_critique(self):
        """
        Calculer le chemin critique
        """
        for tache in self.taches:
            if not tache.dependances:
                tache.es = self.date_debut
                tache.ef = tache.es + timedelta(days=tache.duree())
            else:
                tache.es = max(dep.ef for dep in tache.dependances)
                tache.ef = tache.es + timedelta(days=tache.duree())

        # Initialiser LF pour la dernière tâche
        fin_projet = max(tache.ef for tache in self.taches)
        for tache in self.taches:
            if tache.ef == fin_projet:
                tache.lf = tache.ef
                tache.ls = tache.lf - timedelta(days=tache.duree())

        # Calculer les temps au plus tard pour toutes les tâches
        for tache in reversed(self.taches):
            if tache.lf is None:
                tache.lf = min(
                    dep.ls for dep in self.taches if tache in dep.dependances
                )
                tache.ls = tache.lf - timedelta(days=tache.duree())

        # Déterminer le chemin critique
        self.chemin_critique = [
            tache for tache in self.taches if (tache.lf - tache.ef).days == 0
        ]


if __name__ == "__main__":
    # Créer des membres
    modou = Membre("Modou", "Chef de projet")
    christian = Membre("Christian", "Développeur")

    # Créer une stratégie de notification par email
    email_strategy = EmailNotificationStrategy()

    # Créer un projet
    projet = Projet(
        "Nouveau Produit",
        "Développement d'un nouveau produit",
        datetime(2024, 1, 1),
        datetime(2024, 12, 31),
        50000,
    )

    # Définir la stratégie de notification
    projet.set_notification_strategy(email_strategy)

    # Ajouter des membres
    projet.ajouter_membre_equipe(modou)
    projet.ajouter_membre_equipe(christian)

    # Ajouter des tâches
    tache1 = Tache(
        "Analyse des besoins",
        "Analyse complète des besoins",
        datetime(2024, 1, 1),
        datetime(2024, 1, 31),
        modou,
        "Terminée",
    )
    tache2 = Tache(
        "Développement",
        "Développement du produit",
        datetime(2024, 2, 1),
        datetime(2024, 6, 30),
        christian,
        "Non démarrée",
    )
    tache2.ajouter_dependance(tache1)
    projet.ajouter_tache(tache1)
    projet.ajouter_tache(tache2)

    # Ajouter un risque
    risque = Risque("Retard de livraison", 0.3, "Élevé")
    projet.ajouter_risque(risque)

    # Ajouter un jalon
    jalon = Jalon("Phase 1 terminée", datetime(2024, 1, 31))
    projet.ajouter_jalon(jalon)

    # Enregistrer un changement
    projet.enregistrer_changement("Changement de la portée du projet")

    # Calculer le chemin critique
    projet.calculer_chemin_critique()

    print("#######################################")
    # Générer et afficher le rapport
    rapport = projet.generer_rapport_performance()
    print(rapport)
