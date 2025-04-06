import station as s
class Velo:
    def __init__(self, ref_velo, electrique, statut, date, km_parcourus, station:s):
        self.ref_velo = ref_velo
        self.electrique = electrique
        self.statut = statut
        self.date = date
        self.km_parcourus = km_parcourus
        self.station = station