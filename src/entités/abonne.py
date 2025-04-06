import abonnement as a
import ville as v
import personne as p

class Abonne(p):
    def __init__(self, id_abonne, email, nom, prenom, numtel, mot_de_passe, nomrue, numrue, abonnement: a, ville: v):
        super().__init__(email, nom, prenom, numtel)
        self.id_abonne = id_abonne
        self.mot_de_passe = mot_de_passe
        self.nomrue = nomrue
        self.numrue = numrue
        self.abonnement = abonnement
        self.ville = ville

    # Getters et setters 
    def get_id_abonne(self):
        return self.id_abonne

    def set_id_abonne(self, id_abonne):
        self.id_abonne = id_abonne

    def get_mot_de_passe(self):
        return self.mot_de_passe

    def set_mot_de_passe(self, mot_de_passe):
        self.mot_de_passe = mot_de_passe

    def get_nomrue(self):
        return self.nomrue

    def set_nomrue(self, nomrue):
        self.nomrue = nomrue

    def get_numrue(self):
        return self.numrue

    def set_numrue(self, numrue):
        self.numrue = numrue

    def get_abonnement(self):
        return self.abonnement

    def set_abonnement(self, abonnement: a):
        self.abonnement = abonnement

    def get_ville(self):
        return self.ville

    def set_ville(self, ville: v):
        self.ville = ville
