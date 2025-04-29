from enum import Enum

class StatutVelo(Enum):
    DISPONIBLE = "Disponible"
    EN_CIRCULATION = "En circulation"
    EN_REPARATION = "En réparation"
    EN_PANNE = "En panne"
    PERDU = "Perdu"
    NON_DISPONIBLE = "Non disponible"

class Velo:
    def __init__(self, refVelo, electrique, batterie, statut: StatutVelo, date_circu, km_total, numStation):
        self.refVelo = refVelo
        self.electrique = electrique
        self.batterie = batterie if electrique else None
        self.statut = statut
        self.km_total = km_total
        self.date_circu = date_circu
        self.numStation = numStation

    # Getter pour refVelo
    def get_refVelo(self): return self.refVelo
    def get_electrique(self): return self.electrique
    def get_batterie(self): return self.batterie
    def get_statut(self): return self.statut
    def get_date_circu(self): return self.date_circu
    def get_km_total(self): return self.km_total
    def get_numStation(self): return self.numStation

    # Setters
    def set_refVelo(self, refVelo): self.refVelo = refVelo
    def set_electrique(self, electrique): self.electrique = electrique
    def set_batterie(self, batterie) : self.batterie = batterie
    def set_statut(self, statut): self.statut = statut
    def set_date_circu(self, date_circu): self.date_circu = date_circu
    def set_km_total(self, km_total): self.km_total = km_total
    def set_numStation(self, numStation): self.numStation = numStation

    # Méthodes
    """
    def importVelo(fichier_csv,stations):
        
        velos = []
        
        with open(fichier_csv, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for ligne in reader:
                if not ligne:  
                    continue
                
                ref = ligne[0]
                type_velo = ligne[1]
                statut_velo = ligne[2]
                station_nom = ligne[3]
                
                station = next((s for s in stations if s.nom == station_nom), None)
                if not station:
                    print(f"Station non trouvée pour le vélo {ref}.")
                    continue 
                date = None
                km = 0
                velo = Velo(
                    ref_velo=ref,  
                    electrique=type_velo,
                    statut=statut_velo,
                    date=date,
                    km_parcourus=km,
                    station=station,
                )
            
                velos.append(velo)
                

        return velos
    """

    def louer(self):
        if self.statut == "disponible" and (not self.electrique or self.pourcentage >= 50):
            self.statut = "en circulation"
        else:
            raise Exception("Vélo déjà loué ou indisponible.")

    def retourner(self):
        if self.statut == "en circulation":
            self.statut = "disponible"
        else:
            raise Exception("Vélo non loué ou déjà retourné.")

    def ajouter_km(self, km):
        if km < 0:
            raise ValueError("Le nombre de kilomètres ne peut pas être négatif.")
        self.km_total += km