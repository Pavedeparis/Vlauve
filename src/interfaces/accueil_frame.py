from tkinter import ttk
from entites.personne import Abonne
class AccueilFrame(ttk.Frame):
    def __init__(self, container, controller, utilisateur):
        super().__init__(container)
        self.controller = controller
        self.utilisateur = utilisateur  # On stocke l'utilisateur complet, pas seulement le nom

        # Initialisation de l'affichage de l'accueil en fonction de l'utilisateur
        self.afficher_accueil()

    def afficher_accueil(self):
        # Message de bienvenue
        message = f"Bienvenue {self.utilisateur.get_nom()} !" 
        ttk.Label(self, text=message, font=("Helvetica", 16)).pack(pady=30)

        # Affichage en fonction de l'utilisateur
        if isinstance(self.utilisateur, Abonne):
            self.afficher_accueil_abonne()
        else:
            self.afficher_accueil_admin()
    
    def afficher_accueil_abonne(self):
        # Menu pour les options possibles
        ttk.Button(self, text="Afficher stations", command=lambda: self.controller.afficher_stations(self.utilisateur)).pack()
        ttk.Button(self, text="Affichage historique trajets", command=lambda:self.controller.afficher_trajets(self.utilisateur)).pack()
        #ttk.Button(self, text="Gestion des factures", command=self.controller.afficher_factures).pack()
        #ttk.Button(self, text="Gestion de mon compte et mon abonnement", command=self.controller.afficher_).pack()
        ttk.Button(self, text="Déconnexion", command=self.controller.afficher_connexion).pack()

    def afficher_accueil_admin(self):
        # Menu pour les options possibles
        ttk.Button(self, text="Gestion des abonnements", command=self.controller.gestion_abonnements).pack()
        ttk.Button(self, text="Afficher stations", command=lambda: self.controller.afficher_stations(self.utilisateur)).pack()
        #ttk.Button(self, text="Gestion des vélos", command=self.controller.afficher_).pack()
        #ttk.Button(self, text="Afficher les statistiques", command=self.controller.afficher_).pack()
        ttk.Button(self, text="Déconnexion", command=self.controller.afficher_connexion).pack()
