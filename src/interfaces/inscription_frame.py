from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from entites.personne import Abonne
from DAO.DAOAbonne import DAOAbonne
from entites.abonnement import Abonnement
from entites.contrat import Contrat
from DAO.DAOContrat import DAOContrat
from DAO.DAOAbonnement import DAOAbonnement

class InscriptionFrame(ttk.Frame):
    def __init__(self, container, controller, utilisateurs):
        super().__init__(container)
        self.controller = controller
        self.utilisateurs = utilisateurs

        # Titre de la fenêtre
        ttk.Label(self, text="Créer un compte", font=("Helvetica", 18)).grid(row=0, column=0, columnspan=2, pady=20, sticky="n")
        self.columnconfigure(0, weight=1)

        # Frame princarte_identitepale pour regrouper les 3 blocs côte à côte
        blocs_frame = ttk.Frame(self)
        blocs_frame.grid(row=1, column=0, pady=10, padx=10)

        # Frame pour l'utilisateur
        utilisateur_frame = ttk.LabelFrame(blocs_frame, text="Utilisateur", padding=(10, 10))
        utilisateur_frame.grid(row=0, column=0, padx=10, sticky="n")
        
        # Email
        ttk.Label(utilisateur_frame, text="Email").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.mail_entry = ttk.Entry(utilisateur_frame, width=25)
        self.mail_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # MDP
        ttk.Label(utilisateur_frame, text="Mot de passe").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.mdp_entry = ttk.Entry(utilisateur_frame, width=25, show="*")
        self.mdp_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Nom
        ttk.Label(utilisateur_frame, text="Nom de famille").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.nom_entry = ttk.Entry(utilisateur_frame, width=25)
        self.nom_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Prénom
        ttk.Label(utilisateur_frame, text="Prénom").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.prenom_entry = ttk.Entry(utilisateur_frame, width=25)
        self.prenom_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Numtel
        ttk.Label(utilisateur_frame, text="Numéro de téléphone").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.numtel_entry = ttk.Entry(utilisateur_frame, width=25)
        self.numtel_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")

        # Carte Bancaire
        ttk.Label(utilisateur_frame, text="Numéro Carte Bancaire").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.numcb_entry = ttk.Entry(utilisateur_frame, width=25)
        self.numcb_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        # Frame pour l'adresse de facturation
        adresse_frame = ttk.LabelFrame(blocs_frame, text="Adresse de facturation", padding=(10, 10))
        adresse_frame.grid(row=1, column=0, padx=10, sticky="n")
        
        # Numéro de rue
        ttk.Label(adresse_frame, text="Numéro de rue").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.numrue_entry = ttk.Entry(adresse_frame, width=25)
        self.numrue_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Rue
        ttk.Label(adresse_frame, text="Nom de rue").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.nomrue_entry = ttk.Entry(adresse_frame, width=25)
        self.nomrue_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Code postal
        ttk.Label(adresse_frame, text="Code Postal").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.code_postal_entry = ttk.Entry(adresse_frame, width=25)
        self.code_postal_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        # Frame pour l'abonnement
        abo_frame = ttk.LabelFrame(blocs_frame, text="Abonnement", padding=(10, 10))
        abo_frame.grid(row=0, column=1, rowspan=2, padx=10, sticky="n")

        # Type d'abonnement
        self.type_abo_var = tk.StringVar(value="Annuel")
        ttk.Label(abo_frame, text="Type d'abonnement").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Radiobutton(abo_frame, text="Annuel", variable=self.type_abo_var, value="Annuel").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        ttk.Radiobutton(abo_frame, text="Occasionnel", variable=self.type_abo_var, value="Occasionnel").grid(row=1, column=2, sticky="w", padx=5, pady=5)

        # Sous-type (si Annuel)
        self.sous_type_var = tk.StringVar(value="Classique")
        ttk.Label(abo_frame, text="Sous-type").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        ttk.Radiobutton(abo_frame, text="Classique", variable=self.sous_type_var, value="Classique").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        ttk.Radiobutton(abo_frame, text="Réduit", variable=self.sous_type_var, value="Réduit").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        ttk.Radiobutton(abo_frame, text="Rien", variable=self.sous_type_var, value="").grid(row=7, column=0, sticky="w", padx=5, pady=5)

        # Durée (si Occasionnel)
        self.duree_var = tk.StringVar(value="")
        ttk.Label(abo_frame, text="Durée").grid(row=2, column=2, sticky="w", padx=5, pady=5)

        # Boutons 1 à 7 jours, un par ligne
        ttk.Radiobutton(abo_frame, text="1 jour", variable=self.duree_var, value="1").grid(row=3, column=2, sticky="w", padx=5)
        ttk.Radiobutton(abo_frame, text="2 jours", variable=self.duree_var, value="2").grid(row=4, column=2, sticky="w", padx=5)
        ttk.Radiobutton(abo_frame, text="3 jours", variable=self.duree_var, value="3").grid(row=5, column=2, sticky="w", padx=5)
        ttk.Radiobutton(abo_frame, text="4 jours", variable=self.duree_var, value="4").grid(row=6, column=2, sticky="w", padx=5)
        ttk.Radiobutton(abo_frame, text="5 jours", variable=self.duree_var, value="5").grid(row=7, column=2, sticky="w", padx=5)
        ttk.Radiobutton(abo_frame, text="6 jours", variable=self.duree_var, value="6").grid(row=8, column=2, sticky="w", padx=5)
        ttk.Radiobutton(abo_frame, text="7 jours", variable=self.duree_var, value="7").grid(row=9, column=2, sticky="w", padx=5)

        # Bouton "Rien"
        ttk.Radiobutton(abo_frame, text="Rien", variable=self.duree_var, value="").grid(row=10, column=2, sticky="w", padx=5)
                
        # Garantie
        ttk.Label(abo_frame, text="Garantie").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.garantie_entry = ttk.Entry(abo_frame, width=10)
        self.garantie_entry.grid(row=4, column=1, sticky="w", padx=5, pady=5)

        # Carte d'identité
        ttk.Label(abo_frame, text="Carte d'identité").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.carte_identite_entry = ttk.Entry(abo_frame, width=10)
        self.carte_identite_entry.grid(row=6, column=1, sticky="w", padx=5, pady=5)

        # Montant
        ttk.Label(abo_frame, text="Montant (€)").grid(row=9, column=0, sticky="w", padx=5, pady=5)
        self.montant_entry = ttk.Entry(abo_frame, width=10)
        self.montant_entry.grid(row=9, column=1, sticky="w", padx=5, pady=5)

        # Explication
        text_explications_abo = (
            "Annuel:\n- Classique → Garantie\n- Réduit → Carte d'identité\n"
            "Occasionnel:\n- Durée entre 1 et 7 jours"
        )
        ttk.Label(abo_frame, text=text_explications_abo, justify="left", foreground="gray").grid(
            row=10, column=0, columnspan=3, sticky="w", padx=5, pady=10
        )


        # Boutons
        ttk.Button(blocs_frame, text="Retour", command=self.controller.afficher_connexion).grid(row=5, column=0, pady=10, padx=10)
        ttk.Button(blocs_frame, text="Créer", command=self.create_account).grid(row=5, column=1, pady=10, padx=10)

    def create_account(self):
        # 1. Créer l'abonné et l'enregistrer
        # Récupérer les infos utilisateur depuis les champs
        email = self.mail_entry.get()
        mdp = self.mdp_entry.get()
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()
        num_tel = self.numtel_entry.get()
        num_cb = self.numcb_entry.get()
        num_rue = self.numrue_entry.get()
        nom_rue = self.nomrue_entry.get()

        abonne = Abonne(None, email, mdp, nom, prenom, num_tel, num_rue, nom_rue, num_cb)
        dao_abonne = DAOAbonne.get_instance()
        carteAbo = dao_abonne.insert_abonne(abonne)
        
        # Vérifier l'abonné
        if carteAbo == -1:
            messagebox.showerror("Erreur", "Échec de création de l'abonné.")
            return

        # Vérifier si tous les champs sont remplis
        if not all([email, mdp, nom, prenom, num_tel, num_cb, num_rue, nom_rue]):
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return

        # 2. Trouver l'ID de l'abonnement sélectionné
        type_abo = self.type_abo_var.get()
        sous_type = self.sous_type_var.get() if type_abo == "Annuel" else None
        duree = self.duree_var.get() if type_abo == "Occasionnel" else None

        # Validation selon le type d'abonnement
        if type_abo == "Annuel":
            if not sous_type:
                messagebox.showerror("Erreur", "Veuillez sélectionner un sous-type d'abonnement (Classique ou Réduit).")
                return
            if duree and duree.strip() != "":
                messagebox.showerror("Erreur", "La durée ne doit pas être sélectionnée pour un abonnement Annuel.")
                return
            if sous_type == "Classique" and not self.garantie_entry.get():
                messagebox.showerror("Erreur", "La garantie est requise pour le sous-type Classique.")
                return
            if sous_type == "Réduit" and not self.carte_identite_entry.get():
                messagebox.showerror("Erreur", "La carte d'identité est requise pour le sous-type Réduit.")
                return
        elif type_abo == "Occasionnel":
            if not duree or not duree.isdigit():
                messagebox.showerror("Erreur", "Veuillez sélectionner une durée (1 à 7 jours) pour un abonnement Occasionnel.")
                return
            if sous_type:
                messagebox.showerror("Erreur", "Le sous-type doit être 'Rien' pour un abonnement Occasionnel.")
                return
            jours_label = " jour" if duree == "1" else " jours"
            sous_type_final = duree + jours_label


        # Recherche de l'abonnement en fonction du type et sous-type/durée
        dao_abo = DAOAbonnement.get_instance()
        sous_type_final = sous_type if type_abo == "Annuel" else (duree + (" jour" if duree == "1" else " jours"))
        abo = dao_abo.select_abonnement_criteres(type_abo=type_abo, sous_type=sous_type_final)

        if not abo:
            messagebox.showerror("Erreur", "Abonnement introuvable.")
            return

        idAbo = abo.get_idAbo()

        if not idAbo:
            messagebox.showerror("Erreur", "Abonnement introuvable.")
            return

        # 3. Créer le contrat entre l'abonné et l'abonnement
        date_debut = datetime.today().date()
        if type_abo == "Annuel":
            date_fin = date_debut + timedelta(days=365)
        else:
            date_fin = date_debut + timedelta(days=int(duree))

        try:
            montant = float(self.montant_entry.get())
        except ValueError:
            messagebox.showerror("Erreur", "Le montant doit être un nombre valide.")
            return

        garantie = self.garantie_entry.get()
        carte_identite = self.carte_identite_entry.get()

        contrat = Contrat(None, idAbo, carteAbo, date_debut, date_fin, montant, garantie, carte_identite)
        dao_contrat = DAOContrat.get_instance()
        id_contrat = dao_contrat.insert_contrat(contrat)

        if id_contrat == -1:
            messagebox.showerror("Erreur", "Échec de création du contrat.")
        else:
            messagebox.showinfo("Succès", "Compte et contrat créés avec succès !")
