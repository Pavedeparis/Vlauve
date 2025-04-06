class Abonnement:
    def __init__(self, id_abonnement):
        self.id_abonnement = id_abonnement

class AbonnementAnnuel(Abonnement):
    def __init__(self, id_abonnement, type):
        super().__init__(id_abonnement)  
        self.type = type

class AbonnementOccasionnel(Abonnement):
    def __init__(self, id_abonnement, duree):
        super().__init__(id_abonnement) 
        self.duree = duree
