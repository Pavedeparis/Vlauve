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

    def __str__(self):
        return f"Contrat de {self.abonne.nom} avec l'abonnement {self.abonnement.id_abonnement}, du {self.date_debut} au {self.date_fin}, montant: {self.montant}€"
