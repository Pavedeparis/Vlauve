import ville as v

class Reseau:
    def __init__(self, id_reseau, nom, annee, ville: v):
        self.id_reseau = id_reseau
        self.nom = nom
        self.annee = annee
        self.ville = ville

    # Getters et setters
    def get_id_reseau(self):
        return self.id_reseau

    def set_id_reseau(self, id_reseau):
        self.id_reseau = id_reseau

    def get_nom(self):
        return self.nom

    def set_nom(self, nom):
        self.nom = nom

    def get_annee(self):
        return self.annee

    def set_annee(self, annee):
        self.annee = annee

    def get_ville(self):
        return self.ville

    def set_ville(self, ville):
        self.ville = ville

    # Affichage du réseau
    def __str__(self):
        return f"Réseau '{self.nom}' créé en {self.annee} dans la ville de {self.ville.nom}."
