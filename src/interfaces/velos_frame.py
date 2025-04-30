
from tkinter import ttk, messagebox
from DAO.DAOVelo import DAOVelo
from entites.velo import StatutVelo
from entites.personne import Administrateur



class VelosFrame(ttk.Frame):
    def __init__(self, container, controller, utilisateur, id_station):
        super().__init__(container)
        self.controller = controller
        self.utilisateur = utilisateur
        self.id_station = id_station

        # Titre
        ttk.Label(self, text=f"Vélos de la station {self.id_station}", font=("Helvetica", 16)).pack(pady=30)
        
        # Affichage en fonction des rôles
        if isinstance(utilisateur, Administrateur):
            # ADMIN : changer l'état du vélo 
            ttk.Label(self, text="Changer l'état du vélo n°").pack(pady=5)
            self.idVeloUpdate_entry = ttk.Entry(self)
            self.idVeloUpdate_entry.pack(pady=5)
            
            # Combobox pour proposer les choix à l'administrateur choisir le nouveau statut
            ttk.Label(self, text="Sélectionner le nouveau statut :").pack(pady=5)
            self.status_combobox = ttk.Combobox(self, values=[StatutVelo.DISPONIBLE.name, 
                                                              StatutVelo.EN_CIRCULATION.name, 
                                                              StatutVelo.EN_REPARATION.name, 
                                                              StatutVelo.EN_PANNE.name, 
                                                              StatutVelo.PERDU.name, 
                                                              StatutVelo.NON_DISPONIBLE.name])
            self.status_combobox.pack(pady=5)

            ttk.Button(self, text="Mettre à jour le vélo", command=self.maj_velo).pack(pady=10)
        else: 
            # ABO : louer un vélo
            ttk.Label(self, text="ID du vélo :").pack(pady=5)
            self.idVelo_entry = ttk.Entry(self)
            self.idVelo_entry.pack(pady=5)
            ttk.Button(self, text="Louer le vélo", command=self.louer_velo).pack(pady=10)

        ttk.Button(self, text="Retour", command=self.retour).pack(pady=10)
        
        # Création du tableau pour afficher les vélos
        self.tab = ttk.Treeview(self, columns=("ID", "Type", "Batterie", "État", "Km", "Date"), show="headings")
        self.tab.heading("ID", text="ID Vélo")
        self.tab.heading("Type", text="Type")
        self.tab.heading("Batterie", text="Batterie")
        self.tab.heading("État", text="État")
        self.tab.heading("Km", text="Km Parcourus")
        self.tab.heading("Date", text="Date Circulation")
        self.tab.pack(expand=True, fill="both", padx=20, pady=10)

        self.charger_velos()

    # Méthode retour car bug donc c'est une bonne alternative
    def retour(self):
        self.controller.afficher_stations(self.utilisateur)

    # Méthode pour charger les vélos de la station à partir de la BDD et les afficher en tableau
    def charger_velos(self):
        daoVelo = DAOVelo.get_instance()
        velos = daoVelo.find_velos_by_station(self.id_station)

        # Vider le tableau avant de le remplir
        for row in self.tab.get_children():
            self.tab.delete(row)

        # Remplir le tableau avec les informations des vélos
        for velo in velos:
            type_velo = "Électrique" if velo.get_electrique() else "Pas électrique"
            batterie = f"{velo.get_batterie()}%" if velo.get_batterie() is not None else "Pas de batterie"
            etat = velo.get_statut().name  # ENUM donc prendre "".name "" pour afficher le nom des possibilités
            km_parcourus = velo.get_km_total()
            date_circulation = velo.get_date_circu()
            
            self.tab.insert('', 'end', values=(
                velo.get_refVelo(),
                type_velo,
                batterie,
                etat,
                km_parcourus,
                date_circulation
            ))

    # ABO : Méthode pour louer un vélo
    def louer_velo(self):
        ref_velo = self.idVelo_entry.get()
        if not ref_velo:
            messagebox("Veuillez entrer un ID de vélo valide")
            return

        daoVelo = DAOVelo.get_instance()
        velo = daoVelo.find_velo(ref_velo)

        if velo is None:
            messagebox.showerror("Erreur", f"Vélo avec l'ID {ref_velo} non trouvé.")
            return

        if velo.get_statut().name != StatutVelo.DISPONIBLE:
            messagebox.showwarning("Alerte", f"Vélo {ref_velo} déjà loué ou indisponible.")
            return

        try:
            velo.set_statut(StatutVelo.EN_CIRCULATION)  
            daoVelo.update_velo(velo) 
            self.charger_velos() 
            messagebox.showinfo("Succès", f"Vélo {ref_velo} loué avec succès !")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur: {e}")

    # ADMIN : Méthode pour mettre à jour l'état d'un vélo 
    def maj_velo(self):
        ref_velo = self.idVeloUpdate_entry.get()  # Récupère l'ID du vélo
        if not ref_velo:
            messagebox.showinfo("Information", "Veuillez entrer un ID de vélo valide")
            return

        # Trouver le vélo à mettre à jour
        daoVelo = DAOVelo.get_instance()
        velo = daoVelo.find_velo(ref_velo)

        if velo is None:
            messagebox.showerror("Erreur", f"Vélo n° {ref_velo} non trouvé.")
            return

        # Récupérer le statut choisi dans la liste déroulante (Combobox)
        nouveau_statut_str = self.status_combobox.get()  # Le statut sous forme de chaîne
        if not nouveau_statut_str:
            messagebox.showinfo("Information", "Veuillez sélectionner un statut valide")
            print("Veuillez sélectionner un statut valide")
            return

        # Convertir la chaîne en valeur de l'enum StatutVelo
        try:
            nouveau_statut = next((s for s in StatutVelo if s.name == nouveau_statut_str), None)
        except KeyError:
            print(f"Erreur : Statut {nouveau_statut_str} non valide.")
            return

        # Modifier le statut du vélo
        velo.set_statut(nouveau_statut)

        try:
            # Mise à jour du vélo dans la base de données
            daoVelo.update_velo(velo)  # Sauvegarde la mise à jour
            self.charger_velos()  # Recharge l'affichage des vélos
            messagebox.showinfo("Succès", f"Le statut du vélo {ref_velo} a été mis à jour avec succès !")
            print(f"Le statut du vélo {ref_velo} a été mis à jour avec succès !")
        except Exception as e:
            print(f"Erreur lors de la mise à jour du statut : {e}")
