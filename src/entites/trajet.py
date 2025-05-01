from entites import station as s
from entites import velo as v
from entites.personne import Abonne as a
import csv


class Trajet:
    def __init__(self, refTrajet, station_depart: s, station_arrivee: s, nbr_km, dateheure_debut, dateheure_fin, abonne:a, velo: v):
        self.refTrajet = refTrajet
        self.station_depart = station_depart
        self.station_arrivee = station_arrivee
        self.nbr_km = nbr_km
        self.dateheure_debut = dateheure_debut
        self.dateheure_fin = dateheure_fin
        self.abonne = abonne
        self.velo = velo
        
    # Getters
    def get_refTrajet(self): return self.refTrajet
    def get_station_depart(self): return self.station_depart
    def get_station_arrivee(self): return self.station_arrivee
    def get_nbr_km(self): return self.nbr_km
    def get_dateheure_debut(self): return self.dateheure_debut
    def get_dateheure_fin(self): return self.dateheure_fin
    def get_abonne(self): return self.abonne
    def get_carteAbo(self): return self.abonne.get_carteAbo()
    def get_velo(self): return self.velo
    def get_refVelo(self): return self.velo.get_refVelo()

    # Setters
    def set_station_depart(self, val): self.station_depart = val
    def set_station_arrivee(self, val): self.station_arrivee = val
    def set_nbr_km(self, val): self.nbr_km = val
    def set_dateheure_debut(self, val): self.dateheure_debut = val
    def set_dateheure_fin(self, val): self.dateheure_fin = val
    def set_abonne(self, val): self.abonne = val
    def set_refVelo(self, val): self.refVelo = val

    # Méthodes 
    def tempsDeTrajet(self):
        return self.dateheure_fin - self.dateheure_debut
    
    # Méthode pour exporter les trajets
    @staticmethod
    def exporter_trajets(trajets):
        with open('src/donnee/trajet.csv', 'w', encoding='UTF8',) as f:
            writer = csv.writer(f)
            
            # Vérifier l'existence de trajets
            if not trajets:
                print("Aucun trajet à exporter.")
                return
            
            # En-têtes du fichier cvs créé
            writer.writerow([
                 "Identifiant du trajet", 
                 "Station de départ",
                 "Station d'arrivée",
                 "Distance parcourue",
                 "Date et heure de départ",
                 "Date et heure d'arrivée"])
            
            # Données du fichier cvs créé
            for trajet in trajets:
                date_depart = trajet.dateheure_debut.strftime('%Y-%m-%d %H:%M:%S') if trajet.dateheure_debut else ""
                date_arrivee = trajet.dateheure_fin.strftime('%Y-%m-%d %H:%M:%S') if trajet.dateheure_fin else ""
                stationdepart=trajet.station_depart.get_nom()
                stationarrivee=trajet.station_arrivee.get_nom()
                distance=f"{trajet.nbr_km}km"
                writer.writerow([
                    trajet.refTrajet,
                    stationdepart,
                    stationarrivee,
                    distance,
                    date_depart,
                    date_arrivee,
                ])
        print("Exportation terminée")

"""
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