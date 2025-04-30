# Classe principale de l'interface de connexion
from tkinter import messagebox
from tkinter import ttk
from entites.personne import Abonne, Administrateur

class ConnexionFrame(ttk.Frame):
    def __init__(self, container, controller, utilisateurs):
        super().__init__(container)
        self.controller = controller
        self.utilisateurs = utilisateurs  # Liste des utilisateurs

        # Titre de la fenêtre
        ttk.Label(self, text="Bienvenue sur l'application", font=("Helvetica", 18)).pack(pady=20)
        
        ttk.Label(self, text="Email").pack(pady=5)
        self.email_entry = ttk.Entry(self)
        self.email_entry.pack()

        ttk.Label(self, text="Mot de passe").pack(pady=5)
        self.mdp_entry = ttk.Entry(self, show="*")
        self.mdp_entry.pack()

        ttk.Button(self, text="Se connecter", command=self.connexion).pack(pady=10)
        ttk.Button(self, text="Créer un compte", command=self.controller.afficher_inscription).pack(pady=10)

    def connexion(self):
        email = self.email_entry.get()
        mdp = self.mdp_entry.get()

        # Vérification si self.utilisateurs est une liste valide et non vide
        if not isinstance(self.utilisateurs, list) or len(self.utilisateurs) == 0:
            messagebox.showerror("Erreur", "Aucun utilisateur trouvé.")
            return

        # Recherche de l'utilisateur avec l'email fourni
        utilisateur = next((u for u in self.utilisateurs if u and u.get_email() == email), None)

        # Debugging: vérifier quel utilisateur a été trouvé
        if utilisateur:
            print("Utilisateur trouvé :", utilisateur.get_email())
        else:
            print("Aucun utilisateur trouvé avec l'email :", email)

        if utilisateur is None:
            messagebox.showerror("Erreur de connexion", "Email introuvable.")
            return

        # Vérification des identifiants
        if utilisateur.verifier_identifiants(email, mdp):
            messagebox.showinfo("Connexion réussie", f"Bienvenue, {utilisateur.get_nom()}!")
        self.controller.afficher_accueil(utilisateur)