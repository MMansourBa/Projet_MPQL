import unittest
from datetime import datetime, timedelta
import logging

from main import Membre, EmailNotificationStrategy, PushNotificationStrategy, Projet, Equipe, Tache, Jalon, Risque, \
    Changement, NotificationContext, SMSNotificationStrategy


class TestProjetModule(unittest.TestCase):

    def setUp(self):
        """
        Initialiser les objets nécessaires pour les tests
        """
        self.modou = Membre("Modou", "Chef de projet")
        self.christian = Membre("Christian", "Développeur")
        self.email_strategy = EmailNotificationStrategy()
        self.sms_strategy = SMSNotificationStrategy()
        self.push_strategy = PushNotificationStrategy()
        self.projet = Projet(
            "Nouveau Produit",
            "Développement d'un nouveau produit",
            datetime(2024, 1, 1),
            datetime(2024, 12, 31),
            50000,
        )
        self.projet.set_notification_strategy(self.email_strategy)

        # Configurer le logger pour capturer les logs de niveau INFO
        self.logger = logging.getLogger()
        if not self.logger.hasHandlers():
            self.logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def test_membre(self):
        """
        Test de la classe Membre
        """
        self.assertEqual(self.modou.nom, "Modou")
        self.assertEqual(self.modou.role, "Chef de projet")

    def test_equipe(self):
        """
        Test de la classe Equipe
        """
        equipe = Equipe()
        equipe.ajouter_membre(self.modou)
        self.assertIn(self.modou, equipe.obtenir_membres())

    def test_tache(self):
        """
        Test de la classe Tache
        """
        tache = Tache(
            "Analyse des besoins",
            "Analyse complète des besoins",
            datetime(2024, 1, 1),
            datetime(2024, 1, 31),
            self.modou,
            "Terminée",
        )
        self.assertEqual(tache.nom, "Analyse des besoins")
        self.assertEqual(tache.description, "Analyse complète des besoins")
        self.assertEqual(tache.date_debut, datetime(2024, 1, 1))
        self.assertEqual(tache.date_fin, datetime(2024, 1, 31))
        self.assertEqual(tache.responsable, self.modou)
        self.assertEqual(tache.statut, "Terminée")
        self.assertEqual(tache.duree(), 30)

        tache2 = Tache(
            "Développement",
            "Développement du produit",
            datetime(2024, 2, 1),
            datetime(2024, 6, 30),
            self.christian,
            "Non démarrée",
        )
        tache2.ajouter_dependance(tache)
        self.assertIn(tache, tache2.dependances)

        tache2.mettre_a_jour_statut("En cours")
        self.assertEqual(tache2.statut, "En cours")

    def test_jalon(self):
        """
        Test de la classe Jalon
        """
        jalon = Jalon("Phase 1 terminée", datetime(2024, 1, 31))
        self.assertEqual(jalon.nom, "Phase 1 terminée")
        self.assertEqual(jalon.date, datetime(2024, 1, 31))

    def test_risque(self):
        """
        Test de la classe Risque
        """
        risque = Risque("Retard de livraison", 0.3, "Élevé")
        self.assertEqual(risque.description, "Retard de livraison")
        self.assertEqual(risque.probabilite, 0.3)
        self.assertEqual(risque.impact, "Élevé")

    def test_changement(self):
        """
        Test de la classe Changement
        """
        changement = Changement("Changement de la portée", 1, datetime.now())
        self.assertEqual(changement.description, "Changement de la portée")
        self.assertEqual(changement.version, 1)

    def test_notification_strategy(self):
        """
        Test des stratégies de notification
        """
        with self.assertLogs(level='INFO') as cm:
            self.email_strategy.envoyer("Message de test", self.modou)
            self.assertIn("Notification envoyée à Modou par email: Message de test", cm.output[0])

        with self.assertLogs(level='INFO') as cm:
            self.sms_strategy.envoyer("Message de test", self.modou)
            self.assertIn("Notification envoyée à Modou par SMS: Message de test", cm.output[0])

        with self.assertLogs(level='INFO') as cm:
            self.push_strategy.envoyer("Message de test", self.modou)
            self.assertIn("Notification envoyée à Modou par notification push: Message de test", cm.output[0])

    def test_notification_context(self):
        """
        Test de la classe NotificationContext
        """
        context = NotificationContext(self.email_strategy)

        with self.assertLogs(level='INFO') as cm:
            context.notifier("Message de test", [self.modou])
            self.assertIn("Notification envoyée à Modou par email: Message de test", cm.output[0])

        context.set_strategy(self.sms_strategy)
        with self.assertLogs(level='INFO') as cm:
            context.notifier("Message de test", [self.modou])
            self.assertIn("Notification envoyée à Modou par SMS: Message de test", cm.output[0])

    def test_projet_methods(self):
        """
        Test des méthodes de la classe Projet
        """
        self.projet.ajouter_membre_equipe(self.modou)
        self.assertIn(self.modou, self.projet.equipe.obtenir_membres())

        tache1 = Tache(
            "Analyse des besoins",
            "Analyse complète des besoins",
            datetime(2024, 1, 1),
            datetime(2024, 1, 31),
            self.modou,
            "Terminée",
        )
        self.projet.ajouter_tache(tache1)
        self.assertIn(tache1, self.projet.taches)

        nouveau_budget = 75000
        self.projet.definir_budget(nouveau_budget)
        self.assertEqual(self.projet.budget, nouveau_budget)

        risque = Risque("Retard de livraison", 0.3, "Élevé")
        self.projet.ajouter_risque(risque)
        self.assertIn(risque, self.projet.risques)

        jalon = Jalon("Phase 1 terminée", datetime(2024, 1, 31))
        self.projet.ajouter_jalon(jalon)
        self.assertIn(jalon, self.projet.jalons)

        description = "Changement de la portée du projet"
        self.projet.enregistrer_changement(description)
        dernier_changement = self.projet.changements[-1]
        self.assertEqual(dernier_changement.description, description)
        self.assertEqual(dernier_changement.version, 1)
        self.assertEqual(self.projet.version, 2)

        tache2 = Tache(
            "Développement",
            "Développement du produit",
            datetime(2024, 2, 1),
            datetime(2024, 6, 30),
            self.christian,
            "Non démarrée",
        )
        tache2.ajouter_dependance(tache1)
        self.projet.ajouter_tache(tache2)
        self.projet.calculer_chemin_critique()
        self.assertIn(tache2, self.projet.chemin_critique)

        rapport = self.projet.generer_rapport_performance()
        self.assertIn("Nouveau Produit", rapport)
        self.assertIn("75000", rapport)  # Mettre à jour cette assertion pour le nouveau budget

        with self.assertLogs(level='INFO') as cm:
            self.projet.notifier("Test de notification")
            self.assertIn("Notification envoyée à Modou par email: Test de notification", cm.output[-1])


if __name__ == '__main__':
    unittest.main()