import reseau as r

class Station:
    def __init__(self, id_station, nom, nomrue, numrue, gps, capacite, velos, reseau: r):
        self.id_station = id_station
        self.nom = nom
        self.nomrue = nomrue
        self.numrue = numrue
        self.gps = gps
        self.capacite = capacite
        self.velos = velos
        self.reseau = reseau

    # Getters
    def get_id_station(self): return self.id_station
    def get_nom(self): return self.nom
    def get_nomrue(self): return self.nomrue
    def get_numrue(self): return self.numrue
    def get_gps(self): return self.gps
    def get_capacite(self): return self.capacite
    def get_velos(self): return self.velos
    def get_reseau(self): return self.reseau

    # Setters
    def set_id_station(self, id_station): self.id_station = id_station
    def set_nom(self, nom): self.nom = nom
    def set_nomrue(self, nomrue): self.nomrue = nomrue    
    def set_numrue(self, numrue): self.numrue = numrue
    def set_gps(self, gps): self.gps = gps
    def set_capacite(self, capacite): self.capacite = capacite
    def set_velos(self, velos): self.velos = velos
    def set_reseau(self, reseau): self.reseau = reseau

    # Affichage de la ville
    def __str__(self):
        nb_electriques = self.compter_velos_disponibles(True)
        nb_mecaniques = self.compter_velos_disponibles(False)
        return f"{self.nom} ({nb_electriques} élect. / {nb_mecaniques} méc.)"

    # Méthodes
    def compter_velos_disponibles(self, electrique=True):
        """Compte le nombre de vélos disponibles selon le type."""
        return sum(1 for v in self.velos if v.electrique == electrique and v.disponible)

    def louer_velo(self):
        """Loue un vélo disponible et change son état."""
        for velo in self.velos:
            if velo.est_disponible:
                velo.est_disponible = False
                return velo
        return None  # Aucun vélo disponible

    def retourner_velo(self):
        """Retourne un vélo en circulation."""
        for velo in self.velos:
            if not velo.est_disponible:
                velo.est_disponible = True
                return velo
        return None  # Aucun vélo à retourner

