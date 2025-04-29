from abc import ABC, abstractmethod

# Classe qui représente tous les utilisateurs
class Personne(ABC):
    def __init__(self, email, mdp, nom, prenom, num_tel):
        self.email = email
        self.mdp = mdp
        self.nom = nom
        self.prenom = prenom
        self.num_tel = num_tel

    # Getters
    def get_email(self): return self.email
    def get_mdp(self): return self.mdp
    def get_nom(self): return self.nom
    def get_prenom(self): return self.prenom
    def get_num_tel(self): return self.num_tel

    # Setters
    def set_email(self, email): self.email = email
    def set_mdp(self, mdp): self.mdp = mdp
    def set_nom(self, nom): self.nom = nom
    def set_prenom(self, prenom): self.prenom = prenom
    def set_num_tel(self, num_tel): self.num_tel = num_tel

    # Méthodes
    def verifier_identifiants(self, email, mdp):
        return self.email == email and self.mdp == mdp

# Classe pour l'abonné qui utilise les fonctionnalités
from .abonnement import Abonnement 

class Abonne(Personne): 
    def __init__(self, carteAbo, email, mdp, nom, prenom, num_tel, num_rue, nom_rue, num_cb, ville):
        super().__init__(email, mdp, nom, prenom, num_tel)
        self.carteAbo = carteAbo
        self.num_rue = num_rue
        self.nom_rue = nom_rue
        self.num_cb = num_cb
        self.ville = ville
        self.trajets = [] 
        self.factures = []

    # Getters  
    def get_email(self): return self.email
    def get_carteAbo(self): return self.carteAbo
    def get_num_rue(self): return self.num_rue
    def get_nom_rue(self): return self.nom_rue
    def get_num_cb(self): return self.num_cb
    def get_ville(self): return self.ville 

    # Setters
    def set_carteAbo(self, carteAbo): self.carteAbo = carteAbo
    def set_num_rue(self, num_rue): self.num_rue = num_rue
    def set_nom_rue(self, nom_rue): self.nom_rue = nom_rue
    def set_num_cb(self, num_cb): self.num_cb = num_cb
    def set_ville(self, ville): self.ville = ville

    # Getters Personne car bug
    def get_email(self): return self.email
    def get_mdp(self): return self.mdp
    def get_nom(self): return self.nom
    def get_prenom(self): return self.prenom
    def get_num_tel(self): return self.num_tel

    # Setters Personne car bug
    def set_email(self, email): self.email = email
    def set_mdp(self, mdp): self.mdp = mdp
    def set_nom(self, nom): self.nom = nom
    def set_prenom(self, prenom): self.prenom = prenom
    def set_num_tel(self, num_tel): self.num_tel = num_tel

    # Méthodes Pierre
    """
    def s_abonner(self, id_abonnement, type_abonnement):
        #Méthode pour s'abonner.
        if type_abonnement == "annuel":
            if self.est_eligible_tarif_reduit():
                type = "tarif réduit"
            else:
                type = "classique"
            self.abonnement = AbonnementAnnuel(id_abonnement, type)
        elif type_abonnement == "occasionnel":
            while True:  # Boucle pour s'assurer que la durée est valide
                try:
                    duree = int(input("Entrez la durée de l'abonnement occasionnel (en jours, entre 1 et 7) : "))
                    if 1 <= duree <= 7:
                        break  # Si la durée est valide, sortir de la boucle
                    else:
                        print("Erreur : La durée doit être comprise entre 1 et 7 jours.")
                except ValueError:
                    print("Erreur : Veuillez entrer un nombre valide.")

            self.abonnement = AbonnementOccasionnel(id_abonnement, duree)
        else:
            print("Type d'abonnement non valide.")


    def ajouter_trajet(self, trajet):
        self.trajets.append(trajet)

    def ajouter_facture(self,facture):
        self.factures.append(facture)
    
    def mettre_a_jour_facture(self, facture):
        self.facture = facture
        
    def calculer_montant_mensuel(self, mois, annee):
        # Calculer le montant total pour un mois donné.
        montant_total = 0
        for trajet in self.trajets:
            if trajet.dateHeureDepart.month == mois and trajet.dateHeureDepart.year == annee:
                montant = self.calculer_montant(trajet, self.abonnement.get_type(), self.ville)
                montant_total += montant
        facture = Facture(
            id_facture=len(self.factures) + 1,
            abonne=self,
            date=date(annee, mois, 1),
            montant=montant_total,
            statut="Facture impayé"
            )
        self.factures.append(facture)
        return montant_total


    def calculer_montant(self, trajet, abonnement_type, ville):
        # Calculer le montant de la facture basé sur le trajet et l'abonnement.
    
        # Obtenir le temps de trajet
        temps = trajet.tempsDeTrajet()  
        temps_minutes = temps.total_seconds() / 60  # Convertion en minutes
        
        # Si le temps de trajet est inférieur à 30min
        if temps_minutes < 30:
            return 0.0  
        
        # Calcule du temps de facturation
        heures_de_facturation = (temps_minutes - 30) / 30  # Temps au-delà de 30 minutes
        heures_de_facturation = min(heures_de_facturation, 24 * 2)  # Limite à 24 heures
        
        # Détermine le coût par demi-heure selon le type d'abonnement et le prix spécifique de la ville
        cout_par_demi_heure = ville.get_px_abo_annuel() if abonnement_type == "classique" else ville.get_px_abo_occasionnel()

        # Calculer le montant
        return heures_de_facturation * cout_par_demi_heure
    
    
    def changer_statut_facture(self, id_facture, nouveau_statut):
        for facture in self.factures:
            if facture.id_facture == id_facture:
                facture.statut = nouveau_statut
                print(f"Le statut de la facture {id_facture} a été mis à jour en '{nouveau_statut}'.")
                return
        print(f"Aucune facture trouvée avec l'identifiant {id_facture}.")


    def exportTrajets(self):
        with open('src/donnee/trajet.csv', 'w', encoding='UTF8',) as f:
            writer = csv.writer(f)
            

            
            if not self.trajets:
                print("Aucun trajet à exporter.")
                return
            writer.writerow(["Identifiant du trajet", "Station de départ","Station d'arrivée","Distance parcourue","Date et heure de départ","Date et heure d'arrivée"])
            for trajet in self.trajets:
                    date_depart = trajet.dateHeureDepart.strftime('%Y-%m-%d %H:%M:%S') if trajet.dateHeureDepart else ""
                    date_arrivee = trajet.dateHeureArrivee.strftime('%Y-%m-%d %H:%M:%S') if trajet.dateHeureArrivee else ""
                    stationdepart=trajet.station_de_depart.nom
                    stationarrivee=trajet.station_arrivee.nom
                    distance=f"{trajet.km}km"
                    writer.writerow([
                    trajet.id_trajet,
                    stationdepart,
                    stationarrivee,
                    distance,
                    date_depart,
                    date_arrivee,
            ])
    def exportFactures(self):
        with open('src/donnee/facture.csv', 'w', encoding='UTF8',) as f:
            writer = csv.writer(f)
        
            if not self.factures:
                    print("Aucun factures associées à exporter.")
                    return
            writer.writerow(["L'identifiant de la facture","La date d'emmission","le montant total","Statut"])
            for facture in self.factures:
                    id=f"id:{facture.id_facture}"
                    montant=f"{facture.montant}€"
                    writer.writerow([   
                    id,
                    facture.date,
                    montant,
                    facture.statut,
            ])
    """

# Classe pour l'administrateur qui gère les fonctionnalités et l'optimisation du service
class Administrateur(Personne): 
    def __init__(self, id_admin, email, mdp, nom, prenom, num_tel):
        super().__init__(email, mdp, nom, prenom, num_tel)
        self.id_admin = id_admin

    # Getters et setters
    def get_id_admin(self) : return self.id_admin
    def set_id_admin(self, id_admin): self.id_admin = id_admin

    # Getters Personne car bug
    def get_email(self): return self.email
    def get_mdp(self): return self.mdp
    def get_nom(self): return self.nom
    def get_prenom(self): return self.prenom
    def get_num_tel(self): return self.num_tel

    # Setters Personne car bug
    def set_email(self, email): self.email = email
    def set_mdp(self, mdp): self.mdp = mdp
    def set_nom(self, nom): self.nom = nom
    def set_prenom(self, prenom): self.prenom = prenom
    def set_num_tel(self, num_tel): self.num_tel = num_tel

