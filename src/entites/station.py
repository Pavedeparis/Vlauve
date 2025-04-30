from . import reseau
from entites.velo import Velo, StatutVelo 

class Station:
    def __init__(self, numStation, nom, gps, nom_rue, num_rue, place_elec, place_non_elec, reseau: reseau):
    #def __init__(self, numStation, nom, gps, nom_rue, num_rue, place_elec, place_non_elec, numRes):
        self.numStation = numStation
        self.nom = nom
        self.gps = gps
        self.nom_rue = nom_rue
        self.num_rue = num_rue
        self.place_elec = place_elec
        self.place_non_elec = place_non_elec
        # self.numRes = numRes enlever? 
        self.reseau = reseau
        self.velos = []  # Liste des vélos dans la station

        # Créer les vélos dans la station
        # for _ in range(self.place_elec):
            # self.velos.append(Velo(refVelo=f"V{_}", electrique=True, batterie=100, statut=StatutVelo.DISPONIBLE, date_circu=None, km_total=0, numStation=self))
        # for _ in range(self.place_non_elec):
            # self.velos.append(Velo(refVelo=f"V{_+self.place_elec}", electrique=False, batterie=50, statut=StatutVelo.DISPONIBLE, date_circu=None, km_total=0, numStation=self))
        
    # Getters
    def get_numStation(self): return self.numStation
    def get_nom(self): return self.nom
    def get_nom_rue(self): return self.nom_rue
    def get_num_rue(self): return self.num_rue
    def get_gps(self): return self.gps
    def get_place_elec(self): return self.place_elec
    def get_place_non_elec(self): return self.place_non_elec
    def get_dispo_elec(self): return self.dispo_elec
    def get_dispo_non_elec(self): return self.dispo_non_elec
    #def get_numRes(self): return self.numRes

    # Setters
    def set_numStation(self, numStation): self.numStation = numStation
    def set_nom(self, nom): self.nom = nom
    def set_nom_rue(self, nom_rue): self.nom_rue = nom_rue    
    def set_num_rue(self, num_rue): self.num_rue = num_rue
    def set_gps(self, gps): self.gps = gps
    def set_place_elec(self, place_elec): self.place_elec = place_elec
    def set_place_non_elec(self, place_non_elec): self.place_non_elec = place_non_elec
    def set_dispo_elec(self, dispo_elec): self.dispo_elec = dispo_elec
    def set_dispo_non_elec(self, dispo_non_elec): self.dispo_non_elec = dispo_non_elec
    #def set_numRes(self, numRes): self.numRes = numRes

    def get_reseau(self): return self.reseau
    def set_reseau(self, reseau): self.reseau = reseau

    # Méthode pour affichery de la station
    def __str__(self):
        infos = [f"Station #{self.numStation}"]

        if self.nom:
            infos.append(f"Nom: {self.nom}")
        if self.nom_rue:
            infos.append(f"Adresse: {self.num_rue} {self.nom_rue}")
        if self.gps:
            infos.append(f"GPS: {self.gps}")
        if self.place_elec is not None:
            infos.append(f"Places électriques: {self.place_elec}")
        if self.place_non_elec is not None:
            infos.append(f"Places mécaniques: {self.place_non_elec}")
        if self.reseau:
            infos.append(f"Réseau: {self.reseau.nom}")

        # Affiche aussi le nombre de vélos s'ils existent
        nb_total = len(self.velos)
        if nb_total > 0:
            nb_elec = sum(1 for v in self.velos if v.electrique)
            nb_meca = nb_total - nb_elec
            infos.append(f"Vélos: {nb_total} (Électriques: {nb_elec}, Mécaniques: {nb_meca})")

        return " | ".join(infos)
    
    # Méthodes
    def louer_velo(self):
        """Loue un vélo disponible et change son état."""
        for velo in self.velos:
            if velo.get_statut() == StatutVelo.DISPONIBLE:
                velo.set_statut(StatutVelo.EN_CIRCULATION)  # Changer le statut
                return velo
        return None  # Aucun vélo disponible

    def retourner_velo(self):
        """Retourne un vélo en circulation."""
        for velo in self.velos:
            if velo.get_statut() == StatutVelo.EN_CIRCULATION:
                velo.set_statut(StatutVelo.DISPONIBLE)  # Changer le statut
                return velo
        return None  # Aucun vélo à retourner

    def compter_velos_disponibles(self, electrique=True):
        return sum(1 for v in self.velos if v.electrique == electrique and v.get_statut() == StatutVelo.DISPONIBLE)


    # Méthodes Pierre
    """
    @staticmethod
    def importStation(fichier_csv):
        
        stations = []
        id_courant = 1
        with open(fichier_csv, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for ligne in reader:
                if not ligne:  
                    continue
                
                nom_station = ligne[0]
                adresse = ligne[1]
                capacite_totale = int(ligne[2])
                capacite_electrique = int(ligne[3])
                capacite_mecanique = capacite_totale - capacite_electrique

                station = Station(
                    numStation=id_courant,  
                    nom=nom_station,
                    gps="",
                    nom_rue=adresse,
                    num_rue=0,              
                    place_elec=capacite_electrique,
                    place_non_elec=capacite_mecanique,
                    reseau=None,
                )
            
                stations.append(station)
                id_courant +=1

        return stations
    
    # Méthode pour ajouter un vélo à une station
    def ajouter_velo(self, velo):
        self.velos.append(velo)

    # Méthode pour compte le nombre de vélos disponibles selon le type
    def compter_velos_disponibles(self, electrique=True):
        return sum(1 for v in self.velos if v.electrique == electrique and v.statut == StatutVelo.DISPONIBLE)

    
    def retourner_velo(self):
        # Retourne un vélo en circulation.
        for velo in self.velos:
            if not velo.est_disponible:
                velo.est_disponible = True
                return velo
        return None  # Aucun vélo à retourner
    
    def louer_velo(self):
        # Loue un vélo disponible et change son état.
        for velo in self.velos:
            if velo.est_disponible:
                velo.est_disponible = False
                return velo
        return None  # Aucun vélo disponible
    """