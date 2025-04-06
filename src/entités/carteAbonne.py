import abonne as a

class CarteAbonne:
    def __init__(self, id_carte, abonne, type):
        self.id_carte = id_carte
        self.abonne = abonne
        self.type = type
    
    # Getters et setters
    def get_id_carte(self):
        return self.id_carte

    def set_id_carte(self, id_carte):
        self.id_carte = id_carte

    def get_abonne(self):
        return self.abonne
    
    def set_abonne(self, abonne):
        self.abonne = abonne

    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type 