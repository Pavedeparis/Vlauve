import tkinter as tk
from tkinter import ttk
from DAO.DAOStation import DAOStation
from entites.personne import Administrateur

class StationsFrame(ttk.Frame):
    def __init__(self, container, controller, utilisateur):
        super().__init__(container)
        self.controller = controller
        self.utilisateur = utilisateur

        # Titre
        ttk.Label(self, text="Stations Vlauve", font=("Helvetica", 16)).pack(pady=30)

        # Champ pour entrer l'ID de la station
        ttk.Label(self, text="ID de la station pour voir ses vélos :").pack(pady=5)
        self.idStat_entry = ttk.Entry(self)
        self.idStat_entry.pack(pady=5)
        ttk.Button(self, text="Voir les vélos de la station", command=self.afficher_velos).pack(pady=5)

        # Tableau des stations
        self.tab = ttk.Treeview(self, columns=("ID", "Nom", "NbPlaces", "nbVE", "nbVNE"), show="headings")
        self.tab.heading("ID", text="ID station")
        self.tab.heading("Nom", text="Nom station")
        self.tab.heading("NbPlaces", text="Places totales")
        self.tab.heading("nbVE", text="Vélos electriques disponibles")
        self.tab.heading("nbVNE", text="Vélos non electriques disponibles")
        self.tab.pack(expand=True, fill="both", padx=20, pady=10)

        bouton_frame = ttk.Frame(self)
        bouton_frame.pack(pady=10)

        if isinstance(self.utilisateur, Administrateur):
            ttk.Button(bouton_frame, text="Ajouter une Station", command=self.ajouter_station).grid(row=0, column=0, padx=5)

        ttk.Button(bouton_frame, text="Retour", command=self.retour).grid(row=0, column=1, padx=5)

        self.charger_stations()

    # Méthode retour
    def retour(self):
        self.controller.afficher_accueil(self.utilisateur)

    def charger_stations(self):
        from DAO.DAOVelo import DAOVelo
        daoStation = DAOStation.get_instance()
        stations = daoStation.select_station()

        # Vider le tableau
        for row in self.tab.get_children():
            self.tab.delete(row)

        # Remplir tableau avec les informations des stations
        for station in stations:
            # Charger les vélos associés à cette station depuis la base de données
            daoVelo = DAOVelo.get_instance()
            velos_station = daoVelo.find_velos_by_station(station.get_numStation())

            # Ajouter les vélos à la station
            station.velos = velos_station

            # Calculer le nombre de vélos disponibles (électriques et non électriques)
            nb_places_totales = station.get_place_elec() + station.get_place_non_elec()
            nb_velos = station.compter_velos_disponibles(True) + station.compter_velos_disponibles(True)
            nb_velos_disponibles = station.compter_velos_disponibles(True) + station.compter_velos_disponibles(False)

            self.tab.insert('', 'end', values=(
                station.get_numStation(),
                station.get_nom(),
                nb_places_totales,
                nb_velos,
                nb_velos_disponibles
            ))

    def ajouter_station(self):
        form = tk.Toplevel(self)
        form.title("Ajouter une Station")

        # Champs à remplir
        labels = ["Nom Station", "GPS", "Nom Rue", "Numéro Rue", 
                "Places Vélos électriques", "Places Vélos non électriques", "Numéro Réseau"]
        entries = []

        for idx, label in enumerate(labels):
            ttk.Label(form, text=label + ":").grid(row=idx, column=0, padx=5, pady=5)
            entry = ttk.Entry(form)
            entry.grid(row=idx, column=1, padx=5, pady=5)
            entries.append(entry)

        # Bouton de validation
        ttk.Button(form, text="Valider", command=lambda: self.enregistrer_station(
            entries, form
        )).grid(row=len(labels), column=0, columnspan=2, pady=10)


    def enregistrer_station(self, entries, form):
        try:
            from entites.station import Station
            from entites.reseau import Reseau
            
            daoStation = DAOStation.get_instance()

            # Récupération des valeurs depuis le formulaire
            nom = entries[0].get()
            gps = entries[1].get()
            nom_rue = entries[2].get()
            num_rue = int(entries[3].get())
            place_elec = int(entries[4].get())
            place_non_elec = int(entries[5].get())
            numRes = int(entries[6].get())

            # Création d'un objet Reseau
            reseau = Reseau(numRes, None, None, None)

            # Création d'un objet Station
            station = Station(
                None,  # numStation sera généré automatiquement par la BDD
                nom,
                nom_rue,
                num_rue,
                gps,
                place_elec,
                place_non_elec,
                reseau
            )

            # Insertion de la station
            daoStation.insert_station(station)

            print("Station ajoutée avec succès")
            self.charger_stations()
            form.destroy()

        except Exception as e:
            print(f"Erreur lors de l'ajout de la station : {e}")


    def afficher_velos(self):
        id_text = self.idStat_entry.get()
        if id_text.isdigit():
            id_station = int(id_text)
            self.controller.afficher_velos(self.utilisateur, id_station)
        else:
            print("Veuillez entrer un ID valide.")
