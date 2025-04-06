import station as s

class Velo:
    def __init__(self, ref_velo, electrique, statut, date, km_parcourus, station: s):
        self.ref_velo = ref_velo
        self.electrique = electrique
        self.statut = statut
        self.date = date
        self.km_parcourus = km_parcourus
        self.station = station

    # Getter pour ref_velo
    def get_ref_velo(self):
        return self.ref_velo

    def set_ref_velo(self, ref_velo):
        self.ref_velo = ref_velo

    def get_electrique(self):
        return self.electrique

    def set_electrique(self, electrique):
        self.electrique = electrique

    def get_statut(self):
        return self.statut

    def set_statut(self, statut):
        self.statut = statut

    def get_date(self):
        return self.date

    def set_date(self, date):
        self.date = date
        
    def get_km_parcourus(self):
        return self.km_parcourus

    def set_km_parcourus(self, km_parcourus):
        self.km_parcourus = km_parcourus

    def get_station(self):
        return self.station

    def set_station(self, station):
        self.station = station
    
    # Affichage du vélo
    def __str__(self):
        type_velo = "électrique" if self.electrique else "mécanique"
        return f"Vélo {self.ref_velo} ({type_velo}), statut: {self.statut}, " \
               f"{self.km_parcourus} km, station: {self.station.nom}"

    # Méthodes
    def louer(self):
        if self.statut == "disponible":
            self.statut = "en circulation"
        else:
            raise Exception("Vélo déjà loué ou indisponible.")

    def retourner(self):
        if self.statut == "en circulation":
            self.statut = "disponible"
        else:
            raise Exception("Vélo non loué ou déjà retourné.")

    def ajouter_km(self, km):
        if km < 0:
            raise ValueError("Le nombre de kilomètres ne peut pas être négatif.")
        self.km_parcourus += km