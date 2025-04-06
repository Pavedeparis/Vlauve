import personne as p
import abonnement as a
import ville as v

class abonne(p):
    def __init__(self, id_abonne, email, mot_de_passe, nom, prenom, numtel, nomrue, numrue, abonnement:a, ville:v):
        self.id_abonne = id_abonne
        self.email = email
        self.mot_de_passe = mot_de_passe
        self.nom = nom
        self.prenom = prenom
        self.numtel = numtel
        self.nomrue = nomrue
        self.numrue = numrue
        self.abonnement = abonnement
        self.ville = ville

"""
class abonne(p):
    def __init__(self, id_abonne, mot_de_passe, nomrue, numrue, abonnement:a, ville:v):
        super.__init__(self)
        self.id_abonne = id_abonne
        self.mot_de_passe = mot_de_passe
        self.nomrue = nomrue
        self.numrue = numrue
        self.abonnement = abonnement
        self.ville = ville
"""