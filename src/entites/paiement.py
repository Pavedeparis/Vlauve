import facture as f

class Paiement:
    def __init__(self, idPaie, date, montant, idFact):
        self.idPaie = idPaie
        self.date = date
        self.montant = montant
        self.idFact = idFact

    # Getters
    def get_idPaie(self): return self.idPaie
    def get_date(self): return self.date
    def get_montant(self): return self.montant
    def get_idFact(self): return self.idFact

    # Setters
    def set_idPaie(self, idPaie): self.idPaie = idPaie
    def set_date(self, date): self.date = date
    def set_montant(self, montant): self.montant = montant
    def set_idFact(self, idFact): self.idFact = idFact
    
    # Affichage du paiment
    def __str__(self):
        return f"Paiement de {self.montant}€ pour la facture {self.idFact}, effectué le {self.date}."