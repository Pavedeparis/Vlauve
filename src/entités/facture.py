import abonne as a

class Facture:
    def __init__(self, id_facture, abonne:a, date, montant, duree):
        self.id_facture = id_facture
        self.abonne = abonne
        self.date = date
        self.montant = montant
        self.duree = duree