from mysql.connector import Error
from DAO.DAOSession import DAOSession
from entites.station import Station
from entites.reseau import Reseau  # <-- important, on utilise Reseau

class DAOStation:
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOStation.unique_instance is None:
            DAOStation.unique_instance = DAOStation()
        return DAOStation.unique_instance

    # Insertion d'une station dans la base de données
    def insert_station(self, une_station):
        sql = "INSERT INTO station (nom, gps, nom_rue, num_rue, place_elec, place_non_elec, numRes) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        valeurs = (
            une_station.get_nom(), une_station.get_gps(), une_station.get_nom_rue(),
            une_station.get_num_rue(), une_station.get_place_elec(), une_station.get_place_non_elec(),
            une_station.get_reseau().get_numRes()  # très important !!
        )

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            connection.commit()  
            return cursor.lastrowid
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création de la station : {e}")
            connection.rollback()
            return -1
        finally:
            if cursor:
                cursor.close()

    # Suppression d'une station
    def delete_station(self, une_station):
        sql = "DELETE FROM station WHERE numStation = %s"
        valeurs = (une_station.get_numStation(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            connection.commit()
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la suppression de la station : {e}")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    # Recherche d'une station par son ID
    def find_station(self, numStation):
        sql = "SELECT * FROM station WHERE numStation = %s"
        valeurs = (numStation,)
        cursor = None  # <-- ajout ici
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
            return None
        finally:
            if cursor:
                cursor.close()


    # Mise à jour d'une station
    def update_station(self, une_station):
        sql = """
        UPDATE station 
        SET nom = %s, gps = %s, nom_rue = %s, num_rue = %s, place_elec = %s, place_non_elec = %s, numRes = %s 
        WHERE numStation = %s
        """
        valeurs = (
            une_station.get_nom(),
            une_station.get_gps(),
            une_station.get_nom_rue(),
            une_station.get_num_rue(),
            une_station.get_place_elec(),
            une_station.get_place_non_elec(),
            une_station.get_reseau().get_numRes(),
            une_station.get_numStation()
        )
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            connection.commit()
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la mise à jour de la station : {e}")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    # Sélection de toutes les stations
    def select_station(self):
        les_stations = []
        sql = "SELECT * FROM station"
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql)
            rs = cursor.fetchall()
            for row in rs:
                les_stations.append(self.set_all_values(row))
            return les_stations
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche des stations : {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    # Transformer une ligne SQL en objet Station
    def set_all_values(self, rs):
        from entites.reseau import Reseau

        reseau = Reseau(
            rs["numRes"],
            None,  # on ne connait pas ici les autres attributs
            None,
            None
        )

        une_station = Station(
            rs["numStation"],
            rs["nom"],
            rs["gps"],
            rs["nom_rue"],
            rs["num_rue"],
            rs["place_elec"],
            rs["place_non_elec"],
            reseau
        )

        return une_station