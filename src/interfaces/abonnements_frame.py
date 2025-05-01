import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from DAO.DAOAbonnement import DAOAbonnement
from entites.abonnement import Abonnement

class AbonnementsFrame(ttk.Frame):
    def __init__(self, container, controller, utilisateurs):
        super().__init__(container)
        self.controller = controller
        self.utilisateurs = utilisateurs

        # Titre et bouton retour
        ttk.Label(self, text="Gestion des abonnements", font=("Helvetica", 18)).grid(row=0, column=0, pady=20)
        ttk.Button(self, text="Retour", command=self.retour).grid(row=1, column=0, pady=10, padx=10)

        # Frame pour les actions proposées à l'admin (ajout, modif, supp)
        frame_actions = ttk.Frame(self)
        frame_actions.grid(row=2, column=0, pady=10)

        # Frame : Ajouter un abonnement
        frame_ajout = ttk.LabelFrame(frame_actions, text="Ajouter un abonnement", padding=10)
        frame_ajout.grid(row=0, column=0, padx=10)

        ttk.Label(frame_ajout, text="Type").grid(row=0, column=0, sticky="w")
        self.type_entry = ttk.Entry(frame_ajout, width=15)
        self.type_entry.grid(row=0, column=1)

        ttk.Label(frame_ajout, text="Sous-type / Durée").grid(row=1, column=0, sticky="w")
        self.sous_type_entry = ttk.Entry(frame_ajout, width=15)
        self.sous_type_entry.grid(row=1, column=1)

        ttk.Button(frame_ajout, text="Ajouter", command=self.ajouter_abonnement).grid(row=2, columnspan=2, pady=5)

        # Frame : Modifier un abonnement
        frame_modif = ttk.LabelFrame(frame_actions, text="Modifier un abonnement", padding=10)
        frame_modif.grid(row=0, column=1, padx=10)

        ttk.Label(frame_modif, text="ID Abonnement").grid(row=0, column=0, sticky="w")
        self.idModif_entry = ttk.Entry(frame_modif, width=15)
        self.idModif_entry.grid(row=0, column=1)

        ttk.Label(frame_modif, text="Nouveau type").grid(row=1, column=0, sticky="w")
        self.type_modif_entry = ttk.Entry(frame_modif, width=15)
        self.type_modif_entry.grid(row=1, column=1)

        ttk.Label(frame_modif, text="Nouveau sous-type").grid(row=2, column=0, sticky="w")
        self.sous_type_modif_entry = ttk.Entry(frame_modif, width=15)
        self.sous_type_modif_entry.grid(row=2, column=1)

        ttk.Button(frame_modif, text="Modifier", command=self.modifier_abonnement).grid(row=3, columnspan=2, pady=5)

        # Frame : Supprimer un abonnement avec l'id
        frame_suppr = ttk.LabelFrame(frame_actions, text="Supprimer un abonnement", padding=10)
        frame_suppr.grid(row=0, column=2, padx=10)

        ttk.Label(frame_suppr, text="ID Abonnement").grid(row=0, column=0, sticky="w")
        self.id_supp_entry = ttk.Entry(frame_suppr, width=15)
        self.id_supp_entry.grid(row=0, column=1)

        ttk.Button(frame_suppr, text="Supprimer", command=self.supprimer_abonnement).grid(row=1, columnspan=2, pady=5)

        # Frame pour le tableau en dessous des actions
        frame_tableau = ttk.LabelFrame(self, text="Liste des abonnements", padding=10)
        frame_tableau.grid(row=3, column=0, padx=20, pady=10)

        self.tree = ttk.Treeview(frame_tableau, columns=("ID", "Type", "Sous-type/Durée"), show="headings")
        self.tree.heading("ID", text="ID Abonnement")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Sous-type/Durée", text="Sous-type / Durée")
        self.tree.grid(row=0, column=0, padx=10, pady=10)

        self.charger_abonnements()

    # Méthode intermédiaire pour faire retour
    def retour(self):
        self.controller.afficher_accueil(self.utilisateurs)

    # Méthode pour charger les abonnements
    def charger_abonnements(self):
        dao_abo = DAOAbonnement.get_instance()
        abonnements = dao_abo.select_abonnement()

        self.tree.delete(*self.tree.get_children())  

        for abo in abonnements:
            self.tree.insert('', 'end', values=(
                abo.get_idAbo(),
                abo.get_type_abo(),
                abo.get_sous_type()
            ))

    # Méthode pour ajouter un abonnement
    def ajouter_abonnement(self):
        type_abo = self.type_entry.get()
        sous_type = self.sous_type_entry.get()

        # Validation de base
        if not type_abo or not sous_type:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return

        # Création de l'objet Abonnement
        abo = Abonnement(None, type_abo, sous_type)
        dao_abo = DAOAbonnement.get_instance()

        # Insertion dans la base de données via DAO
        result = dao_abo.insert_abonnement(abo)

        if result == -1:
            messagebox.showerror("Erreur", "Échec de l'ajout de l'abonnement.")
        else:
            messagebox.showinfo("Succès", "Abonnement ajouté avec succès.")
            self.charger_abonnements() 

    # Méthode pour modifier un abonnement en fonction de son id
    def modifier_abonnement(self):
        # Récupérer les informations renseignées
        abo_id = self.idModif_entry.get()
        type_abo = self.type_modif_entry.get()
        sous_type = self.sous_type_modif_entry.get()

        if not abo_id or not type_abo or not sous_type:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return

        # Rechercher l'abonnement avec l'id
        dao_abo = DAOAbonnement.get_instance()
        abo = dao_abo.find_abonnement(abo_id)

        if not abo:
            messagebox.showerror("Erreur", "Abonnement introuvable.")
            return

        # Mise à jour de l'abonnement
        abo.set_type_abo(type_abo)
        abo.set_sous_type(sous_type)
        result = dao_abo.update_abonnement(abo)

        # Vérification de l'action
        if result:
            messagebox.showinfo("Succès", "Abonnement modifié avec succès.")
            self.charger_abonnements() 
        else:
            messagebox.showerror("Erreur", "Échec de la modification de l'abonnement.")


    def supprimer_abonnement(self):
        abo_id = self.id_supp_entry.get()
        if not abo_id:
            messagebox.showerror("Erreur", "Veuillez entrer l'ID de l'abonnement à supprimer.")
            return
        
        dao_abo = DAOAbonnement.get_instance()
        abo = dao_abo.find_abonnement(abo_id)

        if not abo:
            messagebox.showerror("Erreur", "Abonnement introuvable.")
            return

        # Confirmation avant suppression
        confirmation = messagebox.askyesno("Confirmation", f"Voulez-vous vraiment supprimer l'abonnement {abo_id}?")
        if confirmation:
            result = dao_abo.delete_abonnement(abo_id)
            if result:
                messagebox.showinfo("Succès", "Abonnement supprimé avec succès.")
                self.charger_abonnements()
            else:
                messagebox.showerror("Erreur", "Échec de la suppression de l'abonnement.")
