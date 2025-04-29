import tkinter as tk
from tkinter import ttk
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

        # Variables pour les filtres
        self.filtre_date = tk.StringVar(value="tous")  # "ancien", "recent", "tous"
        self.filtre_distance = tk.StringVar(value="tous")  # "grande", "petite", "tous"

        # Tableau des trajets
        self.tree = ttk.Treeview(self, columns=("ID", "Départ", "Arrivée", "KM", "Vélo"), show="headings")
        self.tree.heading("ID", text="ID Trajet")
        self.tree.heading("Départ", text="Station Départ")
        self.tree.heading("Arrivée", text="Station Arrivée")
        self.tree.heading("KM", text="Km parcourus")
        self.tree.heading("Vélo", text="Vélo")
        self.tree.pack(expand=True, fill="both", padx=20, pady=10)

        # Frame pour les boutons 
        bouton_frame = ttk.Frame(self)
        bouton_frame.pack(pady=10)

        ttk.Button(bouton_frame, text="Enregistrer un Trajet", command=self.ajouter_trajet).grid(row=0, column=0, padx=5)
        ttk.Button(bouton_frame, text="Exporter Historique", command=self.exporter_historique).grid(row=0, column=1, padx=5)
        ttk.Button(bouton_frame, text="Retour", command=self.controller.afficher_accueil).grid(row=0, column=2, padx=5)

        # Frame : filtrer par date
        filtre_frame = ttk.LabelFrame(self, text="Filtrer par date")
        filtre_frame.pack(pady=10)

        ttk.Radiobutton(filtre_frame, text="Tous", value="tous", variable=self.filtre_date, command=self.charger_trajets).grid(row=0, column=0, padx=5)
        ttk.Radiobutton(filtre_frame, text="Plus ancien", value="ancien", variable=self.filtre_date, command=self.charger_trajets).grid(row=0, column=1, padx=5)
        ttk.Radiobutton(filtre_frame, text="Plus récent", value="recent", variable=self.filtre_date, command=self.charger_trajets).grid(row=0, column=2, padx=5)

        # Frame : filtrer par distance
        filtre_distance_frame = ttk.LabelFrame(self, text="Filtrer par distance")
        filtre_distance_frame.pack(pady=10)

        ttk.Radiobutton(filtre_distance_frame, text="Tous", value="tous", variable=self.filtre_distance, command=self.charger_trajets).grid(row=0, column=0, padx=5)
        ttk.Radiobutton(filtre_distance_frame, text="Plus grande distance", value="grande", variable=self.filtre_distance, command=self.charger_trajets).grid(row=0, column=1, padx=5)
        ttk.Radiobutton(filtre_distance_frame, text="Plus petite distance", value="petite", variable=self.filtre_distance, command=self.charger_trajets).grid(row=0, column=2, padx=5)

        # Charger trajets
        self.charger_trajets()

    def charger_trajets(self):
        daoTrajet = DAOTrajet.get_instance()
        trajets = daoTrajet.select_trajet(self.abonne) 

        # Filtrer par date
        if self.filtre_date.get() == "ancien":
            trajets.sort(key=lambda t: t.get_date_heure_depart())  
        elif self.filtre_date.get() == "recent":
            trajets.sort(key=lambda t: t.get_date_heure_depart(), reverse=True)

        # Filtrer par distance
        if self.filtre_distance.get() == "petite":
            trajets.sort(key=lambda t: t.get_km_parcourus())  # petit -> grand
        elif self.filtre_distance.get() == "grande":
            trajets.sort(key=lambda t: t.get_km_parcourus(), reverse=True)  # grand -> petit

        # Vider le tableau pour le réinitialiser
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Remplir tableau avec les données voulues
        for trajet in trajets:
            self.tree.insert('', 'end', values=(
                trajet.get_id_trajet(),
                trajet.get_station_depart().get_nom_station(),
                trajet.get_station_arrivee().get_nom_station(),
                trajet.get_km_parcourus(),
                trajet.get_velo().get_ref_velo()
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

        ttk.Button(form, text="Valider", command=lambda: self.enregistrer_trajet(
            entry_depart.get(), entry_arrivee.get(), entry_km.get(), entry_velo.get(), form
        )).grid(row=4, column=0, columnspan=2, pady=10)
    
    # Méthode pour enregistrer le trajet avec les informations données
    def enregistrer_trajet(self, id_station_depart, id_station_arrivee, km_parcourus, ref_velo, form):
        try:
            daoStation = DAOStation.get_instance()
            daoVelo = DAOVelo.get_instance()
            daoTrajet = DAOTrajet.get_instance()

            # Retrouver les entités à partir des IDs entrés
            station_depart = daoStation.find_station(int(id_station_depart))
            station_arrivee = daoStation.find_station(int(id_station_arrivee))
            velo = daoVelo.find_velo(ref_velo)

            if not station_depart or not station_arrivee or not velo:
                print("Erreur : Station ou Vélo introuvable")
                return

            # Reformuler l'ajout du trajet
            trajet = Trajet(
                id_trajet=None,  # Auto-incrémenté
                station_depart=station_depart,
                station_arrivee=station_arrivee,
                km_parcourus=float(km_parcourus),
                date_heure_depart=datetime.now(),
                date_heure_arrivee=datetime.now(),
                velo=velo,
                abonne=self.abonne
            )

            id_trajet = daoTrajet.insert_trajet(trajet)

            if id_trajet != -1:
                print("Trajet ajouté avec succès ! ID:", id_trajet)
                self.charger_trajets()  # Recharger le tableau
                form.destroy() # Fermer l'onglet
            else:
                print("Erreur lors de l'insertion du trajet.")

        except Exception as e:
            print(f"Erreur : {e}")

    # Méthode  pour exporter l'historique des trajets (en fonction des filtres?)
    def exporter_historique(self):
        print("Exporter historique")
        # Ajouter code Pierre