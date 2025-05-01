class Abonnement:
    def __init__(self, idAbo, type_abo, sous_type):
        self.idAbo = idAbo
        
        # validation du type
        types_valides = ["Annuel", "Occasionnel"]
        if type_abo not in types_valides:
            print("Mauvais type d'abonnement")
        self.type_abo = type_abo

        # Validation du sous-type
        sous_types_valides = ["1 jour", "2 jours", "3 jours", "4 jours", "5 jours", "6 jours", "7 jours", "Réduit", "Classique"]
        if sous_type not in sous_types_valides:
            print("Mauvais sous type d'abonnement")
        self.sous_type = sous_type

    # Getters 
    def get_idAbo(self): return self.idAbo
    def get_type_abo(self): return self.type_abo
    def get_sous_type(self): return self.sous_type

    # Setters
    def set_idAbo(self, id_abo): self.idAbo = id_abo
    def set_type_abo(self, type_abo): self.type_abo = type_abo
    def set_sous_type(self, sous_type): self.sous_type = sous_type