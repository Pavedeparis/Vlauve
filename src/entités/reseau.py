import ville as v
class Reseau:
    def __init__(self, id_reseau, nom, annee, ville:v):
        self.id_reseau = id_reseau
        self.nom = nom
        self.annee = annee
        self.ville = ville