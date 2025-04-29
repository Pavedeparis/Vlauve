from entites import ville as v

class Reseau:
    def __init__(self, numRes, nom, annee, idVille):
        self.numRes = numRes
        self.nom = nom
        self.annee = annee
        self.idVille = idVille
        self.stations=set()

    # Getters 
    def get_numRes(self): return self.numRes
    def get_nom(self): return self.nom
    def get_annee(self): return self.annee
    def get_idVille(self): return self.idVille
    
    # Setters
    def set_numRes(self, numRes): self.numRes = numRes
    def set_nom(self, nom): self.nom = nom
    def set_annee(self, annee): self.annee = annee
    def set_idVille(self, idVille): self.idVille = idVille
    
    # Affichage du réseau
    def __str__(self):
        return f"Réseau '{self.nom}' créé en {self.annee} dans la idVille de {self.idVille.nom}."
    
    # Méthodes Pierre 
    """
    def ajouter_station(self, station):
        if len(station.liste_de_velo) <= station.get_capacite_totale():
            self.stations.add(station)
        else:
            print(f"erreur, Station {station.nom} non ajoutée : trop de vélos ({len(station.liste_de_velo)} / {station.get_capacite_totale()})")
    """