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

    def __str__(self):
        nb_electriques = self.compter_velos_disponibles(True)
        nb_mecaniques = self.compter_velos_disponibles(False)
        return f"{self.nom} ({nb_electriques} élect. / {nb_mecaniques} méc.)"
