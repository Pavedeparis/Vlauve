import personne as p
class abonne(p):
    def __init__(self, nom, prenom, abonnement):
        super.__init__(self)
        self.abonnement = abonnement