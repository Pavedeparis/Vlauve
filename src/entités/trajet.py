import station as s
import velo as v
import abonne as a

class Trajet:
    def __init__(self, id_trajet, station_depart: s, station_arrivee: s, km_parcourus,
                 date_heure_depart, date_heure_arrivee, velo: v, abonne: a):
        self._id_trajet = id_trajet
        self._station_depart = station_depart
        self._station_arrivee = station_arrivee
        self._km_parcourus = km_parcourus
        self._date_heure_depart = date_heure_depart
        self._date_heure_arrivee = date_heure_arrivee
        self._velo = velo
        self._abonne = abonne

    # Getters
    def get_id_trajet(self): return self._id_trajet
    def get_station_depart(self): return self._station_depart
    def get_station_arrivee(self): return self._station_arrivee
    def get_km_parcourus(self): return self._km_parcourus
    def get_date_heure_depart(self): return self._date_heure_depart
    def get_date_heure_arrivee(self): return self._date_heure_arrivee
    def get_velo(self): return self._velo
    def get_abonne(self): return self._abonne

    # Setters
    def set_station_depart(self, val): self._station_depart = val
    def set_station_arrivee(self, val): self._station_arrivee = val
    def set_km_parcourus(self, val): self._km_parcourus = val
    def set_date_heure_depart(self, val): self._date_heure_depart = val
    def set_date_heure_arrivee(self, val): self._date_heure_arrivee = val
    def set_velo(self, val): self._velo = val
    def set_abonne(self, val): self._abonne = val
