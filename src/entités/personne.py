class Personne:
    def __init__(self, email, nom, prenom, numtel):
        self.email = email
        self.nom = nom
        self.prenom = prenom
        self.numtel = numtel

    # Getters et setters
    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email = email

    def get_nom(self):
        return self.nom

    def set_nom(self, nom):
        self.nom = nom

    def get_prenom(self):
        return self.prenom

    def set_prenom(self, prenom):
        self.prenom = prenom

    def get_numtel(self):
        return self.numtel

    def set_numtel(self, numtel):
        self.numtel = numtel
