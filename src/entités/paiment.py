import facture as f

class Paiement:
    def __init__(self, id_paiement, facture: f, date, montant):
        self.id_paiement = id_paiement
        self.facture = facture
        self.date = date
        self.montant = montant

    # Getters et setters
    def get_id_paiement(self):
        return self.id_paiement

    def set_id_paiement(self, id_paiement):
        self.id_paiement = id_paiement

    def get_facture(self):
        return self.facture

    def set_facture(self, facture):
        self.facture = facture

    def get_date(self):
        return self.date

    def set_date(self, date):
        self.date = date

    def get_montant(self):
        return self.montant

    def set_montant(self, montant):
        self.montant = montant
    
    # Affichage du paiment
    def __str__(self):
        return f"Paiement de {self.montant}€ pour la facture {self.facture.id_facture}, effectué le {self.date}."
