class Trajet:
    def __init__(self, refTrajet, station_depart, station_arrivee, nbr_km, dateheure_debut, dateheure_fin, carteAbo, refVelo):
        self._refTrajet = refTrajet
        self._station_depart = station_depart
        self._station_arrivee = station_arrivee
        self._nbr_km = nbr_km
        self._dateheure_debut = dateheure_debut
        self._dateheure_fin = dateheure_fin
        self._carteAbo = carteAbo
        self._refVelo = refVelo
        
    # Getters
    def get_refTrajet(self): return self._refTrajet
    def get_station_depart(self): return self._station_depart
    def get_station_arrivee(self): return self._station_arrivee
    def get_nbr_km(self): return self._nbr_km
    def get_dateheure_debut(self): return self._dateheure_debut
    def get_dateheure_fin(self): return self._dateheure_fin
    def get_carteAbo(self): return self._carteAbo
    def get_refVelo(self): return self._refVelo

    # Setters
    def set_station_depart(self, val): self._station_depart = val
    def set_station_arrivee(self, val): self._station_arrivee = val
    def set_nbr_km(self, val): self._nbr_km = val
    def set_dateheure_debut(self, val): self._dateheure_debut = val
    def set_dateheure_fin(self, val): self._dateheure_fin = val
    def set_carteAbo(self, val): self._carteAbo = val
    def set_refVelo(self, val): self._refVelo = val

    # Méthodes 
    def tempsDeTrajet(self): # Pierre
        return self._dateheure_debut - self._dateheure_fin