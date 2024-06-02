import unittest
from datetime import datetime

from EmailNotificationStrategy import EmailNotificationStrategy
from Jalon import Jalon
from Membre import Membre
from Projet import Projet
from Risque import Risque
from Tache import Tache


class TestProjetMethods(unittest.TestCase):
    """
    Test cases for the Projet class.
    """

    def setUp(self):
        # Créer des membres
        self.modou = Membre("Modou", "Chef de projet")
        self.christian = Membre("Christian", "Développeur")

        # Créer un projet
        self.projet = Projet(
            "Nouveau Produit",
            "Développement d'un nouveau produit",
            datetime(2024, 1, 1),
            datetime(2024, 12, 31),
            50000,
        )

        # Définir la stratégie de notification
        self.email_strategy = EmailNotificationStrategy()
        self.projet.set_notification_strategy(self.email_strategy)
        # Ajouter des membres
        self.projet.ajouter_membre_equipe(self.modou)
        self.projet.ajouter_membre_equipe(self.christian)
        # Ajouter des tâches
        self.tache1 = Tache(
            "Analyse des besoins",
            "Analyse complète des besoins",
            datetime(2024, 1, 1),
            datetime(2024, 1, 31),
            self.modou,
            "Terminée",
        )
        self.tache2 = Tache(
            "Développement",
            "Développement du produit",
            datetime(2024, 2, 1),
            datetime(2024, 6, 30),
            self.christian,
            "Non démarrée",
        )
        self.tache2.ajouter_dependance(self.tache1)
        self.projet.ajouter_tache(self.tache1)
        self.projet.ajouter_tache(self.tache2)

        # Ajouter un risque
        self.risque = Risque("Retard de livraison", 0.3, "Élevé")
        self.projet.ajouter_risque(self.risque)

        # Ajouter un jalon
        self.jalon = Jalon("Phase 1 terminée", datetime(2024, 1, 31))
        self.projet.ajouter_jalon(self.jalon)

        # Enregistrer un changement
        self.projet.enregistrer_changement("Changement de la portée du projet")

    def test_ajouter_membre_equipe(self):
        """
        Ajouter un membre dans l'equipe de projet
        """
        self.assertIn(self.modou, self.projet.equipe.obtenir_membres())
        self.assertIn(self.christian, self.projet.equipe.obtenir_membres())

    def test_ajouter_tache(self):
        """
        Ajouter une tache a un projet
        """
        self.assertIn(self.tache1, self.projet.taches)
        self.assertIn(self.tache2, self.projet.taches)

    def test_ajouter_risque(self):
        """
        Ajouter risque
        """
        self.assertIn(self.risque, self.projet.risques)

    def test_ajouter_jalon(self):
        """
        Ajout d'un jalon a un projet
        """
        self.assertIn(self.jalon, self.projet.jalons)

    def test_enregistrer_changement(self):
        """
        Changement dans le projet
        """
        self.assertEqual(len(self.projet.changements), 1)
        self.assertEqual(
            self.projet.changements[0].description, "Changement de la portée du projet"
        )
        self.assertEqual(self.projet.version, 2)

    def test_calculer_chemin_critique(self):
        """
        Chemin critique des taches du projet
        """
        self.projet.calculer_chemin_critique()
        self.assertIn(self.tache2, self.projet.chemin_critique)

    def test_generer_rapport_performance(self):
        """
        Test générant le rapport de performance.
        """
        rapport = self.projet.generer_rapport_performance()
        self.assertIn("Rapport d'activités du Projet 'Nouveau Produit'", rapport)
        self.assertIn("Modou (Chef de projet)", rapport)
        self.assertIn("Christian (Développeur)", rapport)
        self.assertIn("Analyse des besoins", rapport)
        self.assertIn("Développement", rapport)
        self.assertIn("Phase 1 terminée", rapport)
        self.assertIn("Retard de livraison", rapport)
        self.assertIn("Chemin Critique:", rapport)


if __name__ == "__main__":
    unittest.main()
