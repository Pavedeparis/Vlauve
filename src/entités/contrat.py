import abonnement as a
import abonne as v

class Contrat:
    def __init__(self, abonnement: a, abonne: v, date_debut, date_fin, montant, depot_garantie, num_carte_identite):
        self.abonnement = abonnement
        self.abonne = abonne
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.montant = montant
        self.depot_garantie = depot_garantie
        self.num_carte_identite = num_carte_identite

    # Getters et setters
    def get_abonnement(self):
        return self.abonnement

    def set_abonnement(self, abonnement):
        self.abonnement = abonnement

    def get_abonne(self):
        return self.abonne

    def set_abonne(self, abonne):
        self.abonne = abonne

    def get_date_debut(self):
        return self.date_debut
    
    def set_date_debut(self, date_debut):
        self.date_debut = date_debut

    def get_date_fin(self):
        return self.date_fin

    def set_date_fin(self, date_fin):
        self.date_fin = date_fin

    def get_montant(self):
        return self.montant

    def set_montant(self, montant):
        self.montant = montant

    def get_depot_garantie(self):
        return self.depot_garantie

    def set_depot_garantie(self, depot_garantie):
        self.depot_garantie = depot_garantie

    def get_num_carte_identite(self):
        return self.num_carte_identite

    def set_num_carte_identite(self, num_carte_identite):
        self.num_carte_identite = num_carte_identite
    
    # Affichage de contrat
    def __str__(self):
        return f"Contrat de {self.abonne.nom} avec l'abonnement {self.abonnement.id_abonnement}, du {self.date_debut} au {self.date_fin}, montant: {self.montant}€"
