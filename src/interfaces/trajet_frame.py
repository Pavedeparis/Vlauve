import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from entites.trajet import Trajet
from DAO.DAOTrajet import DAOTrajet
from DAO.DAOStation import DAOStation
from DAO.DAOVelo import DAOVelo

class TrajetFrame(ttk.Frame):
    def __init__(self, container, controller, abonne):
        super().__init__(container)
        self.controller = controller
        self.abonne = abonne

        ttk.Label(self, text="Vos trajets", font=("Helvetica", 16)).pack(pady=30)

        # Variables pour les filtres
        self.filtre_date = tk.StringVar(value="rien")  # valeur par défaut
        self.filtre_distance = tk.StringVar(value="rien") # valeur par défaut

        # Frame horizontal combiné (filtres + boutons)
        top_controls = ttk.Frame(self)
        top_controls.pack(padx=10, pady=10, fill="x")

        # Sous-frame pour le filtre date
        fdate_frame = ttk.LabelFrame(top_controls, text="Filtrer par date")
        fdate_frame.grid(row=0, column=1, padx=5)

        ttk.Radiobutton(fdate_frame, text="Sans filtre", value="rien", variable=self.filtre_date, command=self.charger_trajets).grid(row=0, column=0, padx=2)
        ttk.Radiobutton(fdate_frame, text="Plus ancien", value="ancien", variable=self.filtre_date, command=self.charger_trajets).grid(row=0, column=1, padx=2)
        ttk.Radiobutton(fdate_frame, text="Plus récent", value="recent", variable=self.filtre_date, command=self.charger_trajets).grid(row=0, column=2, padx=2)

        # Sous-frame pour le filtre distance
        fdistance_frame = ttk.LabelFrame(top_controls, text="Filtrer par distance")
        fdistance_frame.grid(row=0, column=2, padx=5)

        ttk.Radiobutton(fdistance_frame, text="Sans filtre", value="rien", variable=self.filtre_distance, command=self.charger_trajets).grid(row=0, column=0, padx=2)
        ttk.Radiobutton(fdistance_frame, text="Plus grande distance", value="grande", variable=self.filtre_distance, command=self.charger_trajets).grid(row=0, column=1, padx=2)
        ttk.Radiobutton(fdistance_frame, text="Plus petite distance", value="petite", variable=self.filtre_distance, command=self.charger_trajets).grid(row=0, column=2, padx=2)

        # Sous-frame pour les boutons
        bouton_frame = ttk.Frame(top_controls)
        bouton_frame.grid(row=0, column=0, padx=5)

        ttk.Button(bouton_frame, text="Enregistrer un Trajet", command=self.ajouter_trajet).grid(row=0, column=0, padx=5)
        ttk.Button(bouton_frame, text="Exporter Historique", command=self.exporter_trajets).grid(row=0, column=1, padx=5)
        ttk.Button(bouton_frame, text="Retour", command=self.retour).grid(row=0, column=2, padx=5)


        # Tableau des trajets
        self.tree = ttk.Treeview(self, columns=("ID", "Départ", "Arrivée", "Début", "Fin", "KM", "Vélo"), show="headings")
        self.tree.heading("ID", text="ID Trajet")
        self.tree.heading("Départ", text="Station départ")
        self.tree.heading("Arrivée", text="Station arrivée")
        self.tree.heading("Début", text="Début trajet")
        self.tree.heading("Fin", text="Fin trajet")
        self.tree.heading("KM", text="Km parcourus")
        self.tree.heading("Vélo", text="Vélo utilisé")
        self.tree.pack(expand=True, fill="both", padx=20, pady=10)

    # Charger trajets
        self.charger_trajets()
    
    def retour(self):
        self.controller.afficher_accueil(self.abonne)

    def charger_trajets(self):
        daoTrajet = DAOTrajet.get_instance()
        trajets = daoTrajet.select_trajets_abonne(self.abonne.get_carteAbo())

        # Filtrer par date
        if self.filtre_date.get() == "ancien":
            trajets = sorted(trajets, key=lambda t: t.get_dateheure_debut())
        elif self.filtre_date.get() == "recent":
            trajets = sorted(trajets, key=lambda t: t.get_dateheure_debut(), reverse=True)

        # Filter par distance
        if self.filtre_distance.get() == "grande":
            trajets = sorted(trajets, key=lambda t: t.get_nbr_km(), reverse=True)
        elif self.filtre_distance.get() == "petite":
            trajets = sorted(trajets, key=lambda t: t.get_nbr_km())


        # Vider le tableau pour le réinitialiser
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Remplir tableau avec les données filtrées
        for trajet in trajets:
            velo = DAOVelo.get_instance().find_velo(trajet.get_velo().get_refVelo())
            self.tree.insert('', 'end', values=(
                trajet.get_refTrajet(),
                trajet.get_station_depart().get_nom(),
                trajet.get_station_arrivee().get_nom(),
                trajet.get_dateheure_debut().strftime("%Y-%m-%d %H:%M"),
                trajet.get_dateheure_fin().strftime("%Y-%m-%d %H:%M"),
                trajet.get_nbr_km(),
                velo.get_refVelo() 
            ))

    # Méthode pour ajouter un trajet à partir du bouton 
    def ajouter_trajet(self):
        form = tk.Toplevel(self)
        form.title("Ajouter un trajet")

        # Labels + Entrées
        ttk.Label(form, text="ID Station Départ:").grid(row=0, column=0, padx=5, pady=5)
        entry_depart = ttk.Entry(form)
        entry_depart.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="ID Station Arrivée:").grid(row=1, column=0, padx=5, pady=5)
        entry_arrivee = ttk.Entry(form)
        entry_arrivee.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form, text="Km parcourus:").grid(row=2, column=0, padx=5, pady=5)
        entry_km = ttk.Entry(form)
        entry_km.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form, text="Référence Vélo:").grid(row=3, column=0, padx=5, pady=5)
        entry_velo = ttk.Entry(form)
        entry_velo.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form, text="Date-Heure Début (YYYY-MM-DD HH:MM)").grid(row=4, column=0, padx=5, pady=5)
        entry_heure_debut = ttk.Entry(form)
        entry_heure_debut.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(form, text="Date-Heure Fin (YYYY-MM-DD HH:MM)").grid(row=5, column=0, padx=5, pady=5)
        entry_heure_fin = ttk.Entry(form)
        entry_heure_fin.grid(row=5, column=1, padx=5, pady=5)

        ttk.Button(form, text="Valider", command=lambda: self.enregistrer_trajet( entry_depart.get(), entry_arrivee.get(), entry_km.get(), entry_velo.get(), entry_heure_debut.get(), entry_heure_fin.get(), form)).grid(row=6, column=0, columnspan=2, pady=10)

    
    # Méthode pour enregistrer le trajet avec les informations données
    def enregistrer_trajet(self, station_depart, station_arrivee, nbr_km, refVelo, heure_debut, heure_fin, form):
        if not station_depart or not station_arrivee or not nbr_km or not refVelo:
            messagebox.showwarning("Attention", "Veuillez remplir tous les champs.")
            return

        try:
            daoStation = DAOStation.get_instance()
            daoVelo = DAOVelo.get_instance()
            daoTrajet = DAOTrajet.get_instance()

            # Retrouver les entités à partir des IDs entrés
            station_depart = daoStation.find_station(int(station_depart))
            station_arrivee = daoStation.find_station(int(station_arrivee))
            velo = daoVelo.find_velo(refVelo)

            if not station_depart or not station_arrivee or not velo:
                print("Erreur : Station ou Vélo introuvable")
                return

            # Format Date-Heure et gestion d'erreur de saisie au mauvais format
            try:
                date_debut = datetime.strptime(heure_debut, "%Y-%m-%d %H:%M")
                date_fin = datetime.strptime(heure_fin, "%Y-%m-%d %H:%M")
            except ValueError:
                messagebox.showerror("Format invalide", "Veuillez entrer la date et l'heure au format : YYYY-MM-DD HH:MM")
                return

            # Ajout du trajet avec les données
            trajet = Trajet(
                refTrajet=None,  # Auto-incrémenté
                station_depart=station_depart,
                station_arrivee=station_arrivee,
                nbr_km=float(nbr_km),
                dateheure_debut=date_debut,
                dateheure_fin=date_fin,
                velo=velo,
                abonne=self.abonne
            )

            refTrajet = daoTrajet.insert_trajet(trajet)

            if refTrajet != -1:
                print("Trajet ajouté avec succès ! ID:", refTrajet)
                messagebox.showinfo("Succès", "Trajet ajouté avec succès !")
                self.charger_trajets()  
                form.destroy() 
            else:
                print("Erreur lors de l'insertion du trajet.")

        except Exception as e:
            print(f"Erreur : {e}")


    # Méthode  pour exporter l'historique des trajets
    def exporter_trajets(self):
        daoTrajet = DAOTrajet.get_instance()
        trajets = daoTrajet.select_trajets_abonne(self.abonne.get_carteAbo())
        if trajets:
            Trajet.exporter_trajets(trajets)
        else:
            print("Aucun trajet à exporter")