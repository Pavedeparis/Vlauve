class Abonnement:
    def __init__(self, idAbo, type_abo, sous_type):
        self._idAbo = idAbo
        
        type_abo = ["Annuel", "Occasionnel"]
        if type not in type_abo:
            print("Mauvais type d'abonnement")
        self.type_abo = type_abo

        sous_type = ["1 jour", "2 jours", "3 jours", "4 jours", "5 jours", "6 jours", "7 jours", "Réduit", "Classique"]
        if type not in sous_type:
            print("Mauvais sous type d'abonnement")
        self.sous_type = sous_type

    # Getters 
    def get_idAbo(self): return self._id_abo
    def get_type_abo(self): return self.type_abo
    def get_sous_type(self): return self.sous_type

    # Setters
    def set_idAbo(self, id_abo): self._id_abo = id_abo
    def set_type_abo(self, type_abo): self.type_abo = type_abo
    def set_sous_type(self, sous_type): self.sous_type = sous_type