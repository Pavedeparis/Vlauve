from mysql.connector import Error
from DAO.DAOSession import DAOSession
from DAO.DAOVelo import DAOVelo
from DAO.DAOStation import DAOStation
from DAO.DAOAbonne import DAOAbonne
from entites.trajet import Trajet

class DAOTrajet:
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOTrajet.unique_instance is None:
            DAOTrajet.unique_instance = DAOTrajet()
        return DAOTrajet.unique_instance

    # Insertion d'un trajet dans la BDD
    def insert_trajet(self, trajet):
        sql = "INSERT INTO trajet (station_depart, station_arrivee, nbr_km, dateheure_debut, dateheure_fin, carteAbo, refVelo) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        valeurs = (
            trajet.get_station_depart().get_id_station(),
            trajet.get_station_arrivee().get_id_station(),
            trajet.get_nbr_km(),
            trajet.get_dateheure_debut(),
            trajet.get_dateheure_fin(),
            trajet.get_abonne().get_carteAbo(),
            trajet.get_velo().get_refVelo()
        )
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return cursor.lastrowid
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création du trajet : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return -1
        finally:
            if cursor:
                cursor.close()
    
    # Suppression d'un trajet dans la BDD
    def delete_trajet(self, trajet):
        sql = "DELETE FROM trajet WHERE refTrajet = %s"
        valeurs = (trajet.get_refTrajet(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la suppression du trajet : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    # Recherche d'un trajet en particulier avec son ID
    def find_trajet(self, refTrajet):
        sql = "SELECT * FROM trajet WHERE refTrajet = %s"
        valeurs = (refTrajet,)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, (valeurs,))
            rs = cursor.fetchone()
            if rs:
                return self.set_all_values(rs)
            else:
                return None
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche du trajet : {e}")
            print(sql)
            print(valeurs)
            return None
        finally:
            if cursor:
                cursor.close()

    # Mise à jour des informations d'un trajet
    def update_trajet(self, un_trajet):
        sql = "UPDATE trajet SET station_depart = %s, station_arrivee = %s, nbr_km = %s, dateheure_debut = %s, dateheure_fin = %s, carteAbo = %s, refVelo = %s WHERE refTrajet = %s"
        valeurs = (
            un_trajet.get_station_depart().get_id_station(),
            un_trajet.get_station_arrivee().get_id_station(),
            un_trajet.get_nbr_km(),
            un_trajet.get_dateheure_debut(),
            un_trajet.get_dateheure_fin(),
            un_trajet.get_abonne().get_carteAbo(),
            un_trajet.get_velo().get_refVelo(),
            un_trajet.get_refTrajet()
        )
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la mise à jour du trajet : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    # Recherche d'un trajet avec des critères
    def select_trajet(self):
        les_trajets = []
        sql = "SELECT * FROM trajet"

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql)
            rs = cursor.fetchall()
            for row in rs:
                les_trajets.append(self.set_all_values(row))
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche de trajet : {e}")
            print(sql)
        finally:
            if cursor:
                cursor.close()
        return les_trajets

    # Méthode pour transformer une ligne en un objet Trajet
    def set_all_values(self, rs):
        dao_velo = DAOVelo.get_instance()
        dao_station = DAOStation.get_instance()
        dao_abonne = DAOAbonne.get_instance()

        station_depart = dao_station.find_station(rs["station_depart"])
        station_arrivee = dao_station.find_station(rs["station_arrivee"])
        velo = dao_velo.find_velo(rs["refVelo"])
        abonne = dao_abonne.find_abonne(rs["carteAbo"])

        return Trajet(
            rs["refTrajet"], 
            station_depart, 
            station_arrivee, 
            rs["nbr_km"], 
            rs["dateheure_debut"], 
            rs["dateheure_fin"], 
            abonne, 
            velo
        )