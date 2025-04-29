class Ville:
    def __init__(self, idVille, nom, code_postal, tarif_min_gratuite, tarif_demi_occ, tarif_demi_ann):
        self.idVille = idVille
        self.nom = nom
        self.code_postal = code_postal
        self.tarif_min_gratuite = tarif_min_gratuite
        self.tarif_demi_occ = tarif_demi_occ
        self.tarif_demi_ann = tarif_demi_ann
        
    # Getters 
    def get_idVille(self): return self.idVille
    def get_nom(self): return self.nom
    def get_code_postal(self): return self.code_postal
    def get_tarif_min_gratuite(self): return self.tarif_min_gratuite
    def get_tarif_demi_occ(self): return self.tarif_demi_occ
    def get_tarif_demi_ann(self): return self.tarif_demi_ann

    # Setters
    def set_idVille(self, idVille): self.idVille = idVille
    def set_nom(self, nom): self.nom = nom
    def set_code_postal(self, code_postal): self.code_postal = code_postal
    def set_tarif_min_gratuite(self, tarif_min_gratuite): self.tarif_min_gratuite = tarif_min_gratuite
    def set_tarif_demi_ann(self, tarif_demi_ann): self.tarif_demi_ann = tarif_demi_ann
    def set_tarif_demi_occ(self, tarif_demi_occ): self.tarif_demi_occ = tarif_demi_occ

     # Affichage de la ville
    def __str__(self):
        return f"Ville {self.nom} (Code Postal: {self.codepostal}), " \
               f"Prix min gratuités: {self.px_min_gratuites}€, " \
               f"Abonnement Annuel: {self.px_abo_annuel}€, " \
               f"Abonnement Occasionnel: {self.px_abo_occasionnel}€"

    # Méthodes
    def get_cout_par_demi_heure(self, type_abonnement):
        """Retourne le coût par demi-heure en fonction du type d'abonnement."""
        if type_abonnement == "tarif réduit":
            return self.px_abo_annuel * 0.5  # Exemple de coût réduit
        elif type_abonnement == "classique":
            return self.px_abo_annuel  # Coût normal
        else:
            raise ValueError("Type d'abonnement invalide. Choisissez 'tarif réduit' ou 'classique'.")

    def calculer_cout_total(self, type_abonnement):
        """Retourne le coût total en fonction du type d'abonnement."""
        if type_abonnement == "annuel":
            return self.px_abo_annuel
        elif type_abonnement == "occasionnel":
            return self.px_abo_occasionnel
        else:
            raise ValueError("Type d'abonnement invalide. Choisissez 'annuel' ou 'occasionnel'.")