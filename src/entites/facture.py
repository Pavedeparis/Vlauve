from personne import Abonne as a

class Facture:
    def __init__(self, idFact, date, montant, carteAbo):
        self.idFact = idFact
        self.date = date
        self.montant = montant
        self.carteAbo = carteAbo

    # Getters
    def get_idFact(self): return self.idFact
    def get_date(self): return self.date
    def get_montant(self): return self.montant
    def get_carteAbo(self): return self.carteAbo
    
    # Setters 
    def set_idFact(self, idFact) : self.idFact = idFact
    def set_date(self, date): self.date = date
    def set_montant(self, montant): self.montant = montant
    def set_carteAbo(self, carteAbo): self.carteAbo = carteAbo

    # Affichage de la facture
    def __str__(self):
        return f"Facture #{self.idFact} pour l'abonné {self.carteAbo}, montant: {self.montant}€"
    
    # Ajouter statut?