class Contrat:
    def __init__(self, idCont, idAbo, carteAbo, date_debut, date_fin, montant, garantie, carte_identite):
        self.idCont = idCont
        self.idAbo = idAbo
        self.carteAbo = carteAbo
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.montant = montant
        self.garantie = garantie
        self.carte_identite = carte_identite

    # Getters 
    def get_idCont(self): return self.idCont
    def get_idAbo(self): return self.idAbo
    def get_carteAbo(self): return self.carteAbo
    def get_date_debut(self): return self.date_debut
    def get_date_fin(self): return self.date_fin
    def get_montant(self): return self.montant
    def get_garantie(self): return self.garantie
    def get_carte_identite(self): return self.carte_identite

    # Setters
    def set_idCont(self, idCont): self.idCont = idCont
    def set_idAbo(self, idAbo): self.idAbo = idAbo
    def set_carteAbo(self, carteAbo): self.carteAbo = carteAbo
    def set_date_debut(self, date_debut): self.date_debut = date_debut
    def set_date_fin(self, date_fin): self.date_fin = date_fin
    def set_montant(self, montant): self.montant = montant
    def set_garantie(self, garantie): self.garantie = garantie
    def set_carte_identite(self, carte_identite): self.carte_identite = carte_identite
    
    # Affichage de contrat
    def __str__(self):
        return f"Contrat de {self.abonne.nom} avec l'idAbo {self.idAbo.id_abonnement}, du {self.date_debut} au {self.date_fin}, montant: {self.montant}€"
