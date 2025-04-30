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
import csv

class Abonne(Personne): 
    def __init__(self, carteAbo, email, mdp, nom, prenom, num_tel, num_rue, nom_rue, num_cb):
        super().__init__(email, mdp, nom, prenom, num_tel)
        self.carteAbo = carteAbo
        self.num_rue = num_rue
        self.nom_rue = nom_rue
        self.num_cb = num_cb
        self.trajets = [] 
        self.factures = []

    # Getters  
    def get_carteAbo(self): return self.carteAbo
    def get_num_rue(self): return self.num_rue
    def get_nom_rue(self): return self.nom_rue
    def get_num_cb(self): return self.num_cb

    # Setters
    def set_carteAbo(self, carteAbo): self.carteAbo = carteAbo
    def set_num_rue(self, num_rue): self.num_rue = num_rue
    def set_nom_rue(self, nom_rue): self.nom_rue = nom_rue
    def set_num_cb(self, num_cb): self.num_cb = num_cb

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

    # Méthode permettant de s'abonner
    def s_abonner(self, idAbo, type_abo,sous_type):
        #Méthode pour s'abonner.
        if type_abo=="annuel":
            self.abonnement = Abonnement(idAbo, type_abo,sous_type)
        elif type_abo == "occasionnel":
            while True:  # Boucle pour s'assurer que la durée est valide
                try:
                    duree = int(input("Entrez la durée de l'abonnement occasionnel (en jours, entre 1 et 7) : "))
                    if 1 <= duree <= 7:
                        break  
                    else:
                        print("Erreur : La durée doit être comprise entre 1 et 7 jours.")
                except ValueError:
                    print("Erreur : Veuillez entrer un nombre valide.")

            self.abonnement = Abonnement(idAbo,type_abo, sous_type)
        else:
            print("Type d'abonnement non valide.")


    """Méthodes Pierre
    # Méthode pour ajouter un trajet
    def ajouter_trajet(self, trajet):
        self.trajets.append(trajet)

    # Méthode pour ajouter une facture
    def ajouter_facture(self,facture):
        self.factures.append(facture)
    
    # Mettre à jour les factures
    def mettre_a_jour_facture(self, facture):
        self.facture = facture
    
    # Méthode pour Calculer le montant total pour un mois donné
    def calculer_montant_mensuel(self, mois, annee):
        from .facture import Facture
        from datetime import date,datetime

        montant_total = 0
        for trajet in self.trajets:
            if trajet.dateheure_debut.month == mois and trajet.dateheure_debut.year == annee:
                montant = self.calculer_montant(trajet, self.abonnement.get_type_abo())
                montant_total += montant
        facture = Facture(
            idFact=len(self.factures) + 1,

            date=date(annee, mois, 1),
            montant=montant_total,
            statut="Facture impayé"
            )
        self.factures.append(facture)
        return montant_total

    # Méthode pour calculer le montant de la facture basé sur le trajet et l'abonnement
    def calculer_montant(self, trajet, type_abo, ville):    
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
        cout_par_demi_heure = ville.get_tarif_demi_ann() if type_abo == "classique" else ville.get_tarif_demi_occ()

        # Calculer le montant
        return heures_de_facturation * cout_par_demi_heure
    
    # Méthode pour changer le statut d'une facture 
    def changer_statut_facture(self, id_facture, nouveau_statut):
        for facture in self.factures:
            if facture.idFact == id_facture:
                facture.statut = nouveau_statut
                print(f"Le statut de la facture {id_facture} a été mis à jour en '{nouveau_statut}'.")
                return
        print(f"Aucune facture trouvée avec l'identifiant {id_facture}.")

    # Méthode pour exporter les trajets de l'abonné
    def exportTrajets(self):
        with open('src/donnee/trajet.csv', 'w', encoding='UTF8',) as f:
            writer = csv.writer(f)
            
            if not self.trajets:
                print("Aucun trajet à exporter.")
                return
            writer.writerow(["Identifiant du trajet", "Station de départ","Station d'arrivée","Distance parcourue","Date et heure de départ","Date et heure d'arrivée"])
            for trajet in self.trajets:
                    date_depart = trajet.dateheure_debut.strftime('%Y-%m-%d %H:%M:%S') if trajet.dateheure_debut else ""
                    date_arrivee = trajet.dateheure_fin.strftime('%Y-%m-%d %H:%M:%S') if trajet.dateheure_fin else ""
                    stationdepart=trajet.station_depart.nom
                    stationarrivee=trajet.station_arrivee.nom
                    distance=f"{trajet.nbr_km}km"
                    writer.writerow([
                    trajet.refTrajet,
                    stationdepart,
                    stationarrivee,
                    distance,
                    date_depart,
                    date_arrivee,
            ])

    # Méthode pour exporter les factures de l'abonné           
    def exportFactures(self):
        with open('src/donnee/facture.csv', 'w', encoding='UTF8',) as f:
            writer = csv.writer(f)
        
            if not self.factures:
                    print("Aucun factures associées à exporter.")
                    return
            writer.writerow(["L'identifiant de la facture","La date d'emmission","le montant total","Statut"])
            for facture in self.factures:
                    id=f"id:{facture.idFact}"
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

