import facture as f

class Paiement:
    def __init__(self, id_paiment, facture:f, date, montant):
        self.id_paiement = id_paiment
        self.facture = facture
        self.date = date
        self.montant = montant