import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from entites.personne import Abonne
from DAO.DAOAbonne import DAOAbonne
from entites.abonnement import Abonnement

class InscriptionFrame(ttk.Frame):
    def __init__(self, container, controller, utilisateurs):
        super().__init__(container)
        self.controller = controller
        self.utilisateurs = utilisateurs

        # Titre de la fenêtre
        ttk.Label(self, text="Créer un compte", font=("Helvetica", 18)).grid(row=0, column=1, columnspan=2, pady=20)

        # Frame pour l'utilisateur
        utilisateur_frame = ttk.LabelFrame(self, text="Utilisateur")
        utilisateur_frame.grid(row=1, column=1, columnspan=2, pady=10)
        
        # Email
        ttk.Label(utilisateur_frame, text="Email").grid(row=1, column=0, padx=5, pady=5)
        self.mail_entry = ttk.Entry(utilisateur_frame, width=20)
        self.mail_entry.grid(row=1, column=1, padx=5, pady=5)     
        
        # MDP
        ttk.Label(utilisateur_frame, text="Mot de passe").grid(row=2, column=0, padx=5, pady=5)
        self.mdp_entry = ttk.Entry(utilisateur_frame, width=20, show="*")
        self.mdp_entry.grid(row=2, column=1, padx=5, pady=5)

        # Nom
        ttk.Label(utilisateur_frame, text="Nom de famille").grid(row=3, column=0, padx=5, pady=5)
        self.nom_entry = ttk.Entry(utilisateur_frame, width=20)
        self.nom_entry.grid(row=3, column=1, padx=5, pady=5)

        # Prénom
        ttk.Label(utilisateur_frame, text="Prénom").grid(row=4, column=0, padx=5, pady=5)
        self.prenom_entry = ttk.Entry(utilisateur_frame, width=20)
        self.prenom_entry.grid(row=4, column=1, padx=5, pady=5)

        # Numtel
        ttk.Label(utilisateur_frame, text="Numéro de téléphone").grid(row=5, column=0, padx=5, pady=5)
        self.numtel_entry = ttk.Entry(utilisateur_frame, width=20)
        self.numtel_entry.grid(row=5, column=1, padx=5, pady=5)

        # Carte Bancaire
        ttk.Label(utilisateur_frame, text="Numéro Carte Bancaire").grid(row=6, column=0, padx=5, pady=5)
        self.numcb_entry = ttk.Entry(utilisateur_frame, width=20)
        self.numcb_entry.grid(row=6, column=1, padx=5, pady=5)

        # Frame pour l'adresse de facturation
        adresse_frame = ttk.LabelFrame(self, text="Adresse de facturation")
        adresse_frame.grid(row=2, column=1, columnspan=2, pady=10)

        # Numéro de rue
        ttk.Label(adresse_frame, text="Numéro de rue").grid(row=0, column=0, padx=5, pady=5)
        self.numrue_entry = ttk.Entry(adresse_frame, width=10)
        self.numrue_entry.grid(row=0, column=1, padx=5, pady=5)

        # Rue
        ttk.Label(adresse_frame, text="Nom de rue").grid(row=0, column=2, padx=5, pady=5)
        self.nomrue_entry = ttk.Entry(adresse_frame, width=30)
        self.nomrue_entry.grid(row=0, column=3, padx=5, pady=5)

        # Code postal
        ttk.Label(adresse_frame, text="Code Postal").grid(row=1, column=0, padx=5, pady=5)
        self.code_postal_entry = ttk.Entry(adresse_frame, width=10)
        self.code_postal_entry.grid(row=1, column=1, padx=5, pady=5)

        # Ville
        ttk.Label(adresse_frame, text="Ville").grid(row=1, column=2, padx=5, pady=5)
        self.ville_entry = ttk.Entry(adresse_frame, width=30)
        self.ville_entry.grid(row=1, column=3, padx=5, pady=5)
        
        # Frame pour l'abonnement
        abo_frame = ttk.LabelFrame(self, text="Abonnement")
        abo_frame.grid(row=7, column=1, columnspan=2, pady=10)

        # Type abonnement
        ttk.Label(abo_frame, text="Type abonnement").grid(row=0, column=0, padx=5, pady=2)
        self.type_abo = ttk.Combobox(abo_frame, values=["Annuel", "Occasionnel"], state="readonly", width=15)
        self.type_abo.grid(row=0, column=1, padx=5, pady=2)
        self.type_abo.bind("<<ComboboxSelected>>", self.update_abonnement_options)

        # Sous-type abonnement (pour l'annuel : classique ou réduit)
        ttk.Label(abo_frame, text="Sous-type abonnement").grid(row=1, column=0, padx=5, pady=2)
        self.sous_type_abo = ttk.Combobox(abo_frame, state="disabled", width=15)
        self.sous_type_abo.grid(row=1, column=1, padx=5, pady=2)

        # Garantie
        ttk.Label(abo_frame, text="Garantie").grid(row=2, column=0, padx=5, pady=2)
        self.garantie_entry = ttk.Entry(abo_frame, state="disabled", width=20)
        self.garantie_entry.grid(row=2, column=1, padx=5, pady=2)

        # Montant
        ttk.Label(abo_frame, text="Montant").grid(row=3, column=0, padx=5, pady=2)
        self.montant_entry = ttk.Entry(abo_frame, state="disabled", width=20)
        self.montant_entry.grid(row=3, column=1, padx=5, pady=2)

        # Carte d'identité
        ttk.Label(abo_frame, text="Carte d'identité").grid(row=4, column=0, padx=5, pady=2)
        self.option_carte = ttk.Entry(abo_frame, state="disabled", width=20)
        self.option_carte.grid(row=4, column=1, padx=5, pady=2)

        # Durée (pour l'abonnement occasionnel)
        ttk.Label(abo_frame, text="Durée (1 à 7 jours)").grid(row=5, column=0, padx=5, pady=2)
        self.duree_entry = ttk.Combobox(abo_frame, state="disabled", width=15)
        self.duree_entry.grid(row=5, column=1, padx=5, pady=2)

        # Boutons
        ttk.Button(self, text="Créer", command=self.create_account).grid(row=8, column=0, pady=10)
        ttk.Button(self, text="Retour", command=self.controller.afficher_connexion).grid(row=8, column=1, pady=10)

    def update_abonnement_options(self, event):
        """Met à jour les options en fonction du type d'abonnement sélectionné."""
        abonnement_type = self.type_abo.get()

        # Réinitialiser les champs
        self.sous_type_abo.set("")
        self.garantie_entry.delete(0, 'end')
        self.montant_entry.delete(0, 'end')
        self.option_carte.delete(0, 'end')
        self.duree_entry.set("")

        # Désactiver tous les champs au départ
        self.sous_type_abo.config(state="disabled")
        self.garantie_entry.config(state="disabled")
        self.montant_entry.config(state="disabled")
        self.option_carte.config(state="disabled")
        self.duree_entry.config(state="disabled")

        # Mettre à jour en fonction du type d'abonnement
        if abonnement_type == "Annuel":
            # Activer le sous-type et la garantie
            self.sous_type_abo['values'] = ["Classique", "Réduit"]
            self.sous_type_abo.set("")
            self.sous_type_abo.config(state="normal")

            # Activer la garantie et le montant
            self.garantie_entry.config(state="normal")
            self.montant_entry.config(state="normal")
            self.option_carte.config(state="disabled")
            self.duree_entry.config(state="disabled")

        elif abonnement_type == "Occasionnel":
            # Désactiver le sous-type, activer la durée et le montant
            self.sous_type_abo.set("")
            self.sous_type_abo.config(state="disabled")

            self.duree_entry['values'] = [f"{i} jour(s)" for i in range(1, 8)]
            self.duree_entry.set("")
            self.duree_entry.config(state="normal")

            # Activer uniquement le montant
            self.montant_entry.config(state="normal")
            self.garantie_entry.config(state="disabled")
            self.option_carte.config(state="disabled")

    def create_account(self):
        email = self.mail_entry.get()
        mdp = self.mdp_entry.get()
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()
        numtel = self.numtel_entry.get()
        carte_bancaire = self.numcb_entry.get()

        # Adresse
        numrue = self.numrue_entry.get()
        nomrue = self.nomrue_entry.get()
        code_postal = self.code_postal_entry.get()
        ville_nom = self.ville_entry.get()

        # Vérification des champs obligatoires
        if not all([email, mdp, nom, prenom, numtel, carte_bancaire, numrue, nomrue, code_postal, ville_nom]):
            messagebox.showwarning("Attention", "Tous les champs doivent être remplis.")
            return

        # Vérifier si email existe déjà
        for utilisateur in self.utilisateurs:
            if utilisateur.email == email:
                messagebox.showerror("Erreur", "Cet email est déjà utilisé.")
                return

        # Création de l'abonnement
        abonnement = None
        type_abo = self.type_abo.get()

        if type_abo == "Annuel":
            sous_type = self.sous_type_abo.get()
            montant = self.montant_entry.get()
            if sous_type == "Classique":
                garantie = self.garantie_entry.get()
                abonnement = Abonnement(None, type_abo="Annuel", sous_type_abo="Classique", montant=float(montant), garantie=garantie)
            elif sous_type == "Réduit":
                carte_id = self.option_carte.get()
                abonnement = Abonnement(None, type_abo="Annuel", sous_type="Réduit", montant=float(montant), carte_id=carte_id)

        elif type_abo == "Occasionnel":
            duree = self.duree_entry.get()
            montant = self.montant_entry.get()
            abonnement = Abonnement(None, type_abo="Occasionnel", duree=duree, montant=float(montant))

        else:
            messagebox.showerror("Erreur", "Veuillez sélectionner un type d'abonnement.")
            return

        # Création de l'abonné
        abonne = Abonne(
            id_abonne=None,
            email=email,
            motdepasse=mdp,
            nom=nom,
            prenom=prenom,
            numtel=numtel,
            nomrue=nomrue,
            numrue=numrue,
            abonnement=abonnement,
            ville=ville_nom
        )

        # Insertion dans la base de données
        try:
            dao_abonne = DAOAbonne.get_instance()
            id_insere = dao_abonne.insert_abonne(abonne)

            if id_insere != -1:
                self.utilisateurs.append(abonne)  # Mettre à jour la liste locale aussi
                messagebox.showinfo("Succès", "Compte créé avec succès !")
                self.controller.afficher_connexion()
            else:
                messagebox.showerror("Erreur", "Erreur lors de la création de l'abonné.")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la création : {str(e)}")