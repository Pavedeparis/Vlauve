import tkinter as tk
from tkinter import messagebox
from interfaces.connexion_frame import ConnexionFrame
from interfaces.inscription_frame import InscriptionFrame
from interfaces.accueil_frame import AccueilFrame
from interfaces.trajet_frame import TrajetFrame
from interfaces.stations_frame import StationsFrame
from interfaces.velos_frame import VelosFrame
from interfaces.abonnements_frame import AbonnementsFrame
from DAO.DAOAbonne import DAOAbonne
from DAO.DAOAdministrateur import DAOAdministrateur

class AppController:
    def __init__(self, container, utilisateurs):
        self.container = container
        self.frame_courant = None
        self.utilisateurs = self.charger_utilisateurs() 
        
        # Debugging: vérifier si utilisateurs est bien peuplée
        print("Utilisateurs chargés :", self.utilisateurs)

        if not self.utilisateurs:  # Si la liste est vide ou None
            print("Erreur : Aucun utilisateur trouvé.")
            messagebox.showerror("Erreur", "Aucun utilisateur trouvé.")
            return 

        self.afficher_connexion()

    
    def charger_utilisateurs(self):
        # Récupérer les utilisateurs
        abonnés = DAOAbonne.get_instance().select_abonnes()
        administrateurs = DAOAdministrateur.get_instance().select_administrateurs()

        # Debugging: vérifier les données récupérées
        print("Abonnés:", abonnés)
        print("Administrateurs:", administrateurs)
        
        # Vérification si les listes sont valides
        if abonnés is None or administrateurs is None:
            print("Erreur : La récupération des utilisateurs a échoué.")
            return []  # Retourner une liste vide pour éviter l'erreur plus tard
        
        return abonnés + administrateurs

    # Méthodes générales
    def changer_frame(self, nouvelle_frame):
        if self.frame_courant:
            self.frame_courant.destroy()
        self.frame_courant = nouvelle_frame
        self.frame_courant.pack(fill="both", expand=True)

    def afficher_connexion(self):
        self.changer_frame(ConnexionFrame(self.container, self, self.utilisateurs))

    def afficher_inscription(self):
        self.changer_frame(InscriptionFrame(self.container, self, self.utilisateurs))

    def afficher_accueil(self, utilisateur):
        self.changer_frame(AccueilFrame(self.container, self, utilisateur)) 

    def afficher_trajets(self, utilisateur):
        self.changer_frame(TrajetFrame(self.container, self, utilisateur))

    def afficher_stations(self, utilisateur):
        self.changer_frame(StationsFrame(self.container, self, utilisateur))

    def afficher_velos(self, utilisateur, id_station):
        self.changer_frame(VelosFrame(self.container, self, utilisateur, id_station))

    # Méthodes d'administration (uniquement pour les administrateurs)
    def gestion_abonnements(self, utilisateur):
        self.changer_frame(AbonnementsFrame(self.container, self, utilisateur))

    def gestion_reseau(self):
        self.changer_frame()