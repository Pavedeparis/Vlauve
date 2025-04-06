from mysql.connector import Error
from DAO.DAOSession import DAOSession
from entités.station import Station

class DAOStation:
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOStation.unique_instance is None:
            DAOStation.unique_instance = DAOStation()
        return DAOStation.unique_instance

    # Insertion d'une station dans la base de données
    def insert_station(self, une_station):
        sql = "INSERT INTO station (nom, nomrue, numrue, gps, capacite, velos, id_reseau, id_ville) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        valeurs = (une_station.get_nom(), une_station.get_nomrue(), une_station.get_numrue(), une_station.get_gps(), une_station.get_capacite(), 
                   une_station.get_velos(), une_station.get_reseau().get_id_reseau(), une_station.get_ville().get_id_ville())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            cle = cursor.lastrowid
            return cle
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création de la station : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return -1
        finally:
            if cursor:
                cursor.close()

    # Suppression d'une station de la base de données
    def delete_station(self, une_station):
        sql = "DELETE FROM station WHERE id_station = %s"
        valeurs = (une_station.get_id_station(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la suppression de la station : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    # Recherche d'une station par son ID
    def find_station(self, id_station):
        sql = "SELECT * FROM station WHERE id_station = %s"
        valeurs = (id_station,)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, valeurs)
            rs = cursor.fetchone()
            if rs:
                return self.set_all_values(rs)
            else:
                return None
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche d'une station : {e}")
            print(sql)
            print(valeurs)
            return None
        finally:
            if cursor:
                cursor.close()

    # Mise à jour des informations d'une station
    def update_station(self, une_station):
        sql = "UPDATE station SET nom = %s, nomrue = %s, numrue = %s, gps = %s, capacite = %s, velos = %s, id_reseau = %s, id_ville = %s WHERE id_station = %s"
        valeurs = (une_station.get_nom(), une_station.get_nomrue(), une_station.get_numrue(), une_station.get_gps(), une_station.get_capacite(), 
                   une_station.get_velos(), une_station.get_reseau().get_id_reseau(), une_station.get_ville().get_id_ville(), une_station.get_id_station())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la mise à jour de la station : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    # Sélection des stations avec critères
    def select_station(self, une_station):
        les_stations = []
        sql = "SELECT * FROM station WHERE "
        critere_id = une_station.get_id_station()
        critere_nom = une_station.get_nom()
        critere_ville = une_station.get_ville()
        valeurs = []

        if critere_id is not None:
            sql += "id_station = %s"
            valeurs.append(critere_id)
        elif critere_nom is None:
            sql = "SELECT * FROM station"
        else:
            conditions = []
            if critere_nom is not None:
                conditions.append("nom = %s")
                valeurs.append(critere_nom)
            if critere_ville is not None:
                conditions.append("id_ville = %s")
                valeurs.append(critere_ville.get_id_ville())
            sql += " AND ".join(conditions)

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, tuple(valeurs))
            rs = cursor.fetchall()
            for row in rs:
                les_stations.append(self.set_all_values(row))
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche de la station : {e}")
            print(sql)
            print(valeurs)
        finally:
            if cursor:
                cursor.close()
        return les_stations

    # Méthode pour transformer une ligne de résultats en un objet Station
    def set_all_values(self, rs):
        from entités.ville import Ville
        from entités.reseau import Reseau
        from entités.velo import Velo
        
        ville = Ville(rs["id_ville"], rs["nom_ville"], rs["codepostal"], rs["px_min_gratuites"], rs["px_abo_annuel"], rs["px_abo_occasionnel"])
        reseau = Reseau(rs["id_reseau"], rs["nom_reseau"], rs["annee"], ville)
        velos = [] 
        une_station = Station(rs["id_station"], rs["nom"], rs["nomrue"], rs["numrue"], rs["gps"], rs["capacite"], velos, reseau, ville)
        return une_station