class Ville:
    def __init__(self, id_ville, nom, codepostal, px_min_gratuites, px_abo_annuel, px_abo_occasionnel):
        self.id_ville = id_ville
        self.nom = nom
        self.codepostal = codepostal
        self.px_min_gratuites = px_min_gratuites
        self.px_abo_annuel = px_abo_annuel
        self.px_abo_occasionnel = px_abo_occasionnel

    # Getters et setters
    def get_id_ville(self):
        return self.id_ville

    def set_id_ville(self, id_ville):
        self.id_ville = id_ville

    def get_nom(self):
        return self.nom

    def set_nom(self, nom):
        self.nom = nom

    def get_codepostal(self):
        return self.codepostal

    def set_codepostal(self, codepostal):
        self.codepostal = codepostal

    def get_px_min_gratuites(self):
        return self.px_min_gratuites

    def set_px_min_gratuites(self, px_min_gratuites):
        self.px_min_gratuites = px_min_gratuites

    def get_px_abo_annuel(self):
        return self.px_abo_annuel

    def set_px_abo_annuel(self, px_abo_annuel):
        self.px_abo_annuel = px_abo_annuel

    def get_px_abo_occasionnel(self):
        return self.px_abo_occasionnel

    def set_px_abo_occasionnel(self, px_abo_occasionnel):
        self.px_abo_occasionnel = px_abo_occasionnel

    # Affichage de la ville
    def __str__(self):
        return f"Ville {self.nom} (Code Postal: {self.codepostal}), " \
               f"Prix min gratuités: {self.px_min_gratuites}€, " \
               f"Abonnement Annuel: {self.px_abo_annuel}€, " \
               f"Abonnement Occasionnel: {self.px_abo_occasionnel}€"

    # Méthodes
    def calculer_cout_total(self, type_abonnement):
        """Retourne le coût total en fonction du type d'abonnement."""
        if type_abonnement == "annuel":
            return self.px_abo_annuel
        elif type_abonnement == "occasionnel":
            return self.px_abo_occasionnel
        else:
            raise ValueError("Type d'abonnement invalide. Choisissez 'annuel' ou 'occasionnel'.")

