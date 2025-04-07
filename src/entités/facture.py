import abonne as a

class Facture:
    def __init__(self, id_facture, abonne: a, date, montant, duree):
        self.id_facture = id_facture
        self.abonne = abonne
        self.date = date
        self.montant = montant
        self.duree = duree

    # Getters
    def get_id_facture(self): return self.id_facture
    def get_abonne(self): return self.abonne
    def get_date(self): return self.date
    def get_montant(self): return self.montant
    def get_duree(self): return self.duree
    
    # Setters 
    def set_id_facture(self, id_facture) : self.id_facture = id_facture
    def set_abonne(self, abonne): self.abonne = abonne
    def set_date(self, date): self.date = date
    def set_montant(self, montant): self.montant = montant
    def set_duree(self, duree): self.duree = duree

    # Affichage de la facture
    def __str__(self):
        return f"Facture #{self.id_facture} pour l'abonné {self.abonne.nom}, montant: {self.montant}€, durée: {self.duree} mois."