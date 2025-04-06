class Abonnement:
    def __init__(self, id_abonnement):
        self._id_abonnement = id_abonnement

    # Getters et setters
    def get_id_abonnement(self):
        return self._id_abonnement

    def set_id_abonnement(self, id_abonnement):
        self._id_abonnement = id_abonnement

class AbonnementAnnuel(Abonnement):
    def __init__(self, id_abonnement, type):
        types_abo_annuel = ["classique", "tarif réduit"]
        if type not in types_abo_annuel:
            print("Le type doit être 'classique' ou 'tarif réduit'.")
        
        super().__init__(id_abonnement)
        self._type = type

    # Getters et setters
    def get_type(self):
        return self._type

    def set_type(self, type):
        self._type = type

class AbonnementOccasionnel(Abonnement):
    def __init__(self, id_abonnement, duree):
        super().__init__(id_abonnement)
        self._duree = duree
    
    # Getters et setters
    def get_duree(self):
        return self._duree

    def set_duree(self, duree):
        self._duree = duree
