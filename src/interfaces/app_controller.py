from tkinter import messagebox
from interfaces.connexion_frame import ConnexionFrame
from interfaces.inscription_frame import InscriptionFrame
from interfaces.accueil_frame import AccueilFrame
from interfaces.trajet_frame import TrajetFrame
from interfaces.stations_frame import StationsFrame
from interfaces.velos_frame import VelosFrame
from interfaces.abonnements_frame import AbonnementsFrame

class AppController:
    def __init__(self, container, utilisateurs):
        self.container = container
        self.frame_courant = None
        self.utilisateurs = utilisateurs 
        
        # Vérifier si utilisateurs trouvés pour débugger
        print("Utilisateurs chargés :", self.utilisateurs)
        if not self.utilisateurs:  
            print("Erreur : Aucun utilisateur trouvé.")
            messagebox.showerror("Erreur", "Aucun utilisateur trouvé.")
            return 

        # Lancer la page de connexion
        self.afficher_connexion()

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

    # Méthode d'administration (uniquement pour l'administrateur)
    def gestion_abonnements(self, utilisateur):
        self.changer_frame(AbonnementsFrame(self.container, self, utilisateur))