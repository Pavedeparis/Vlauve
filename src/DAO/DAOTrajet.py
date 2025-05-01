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
    def insert_trajet(self, nouv_trajet):
        from datetime import datetime
        sql = "INSERT INTO trajet (station_depart, station_arrivee, nbr_km, dateheure_debut, dateheure_fin, carteAbo, refVelo) VALUES (%s, %s, %s, %s, %s, %s, %s)"        

        # Vérification : si ce sont des strings -> les convertir (mis en place à cause de bugs)
        if isinstance(nouv_trajet.get_dateheure_debut(), str):
            date_debut = datetime.strptime(nouv_trajet.get_dateheure_debut(), "%Y-%m-%d %H:%M:%S")
        else:
            date_debut = nouv_trajet.get_dateheure_debut()

        if isinstance(nouv_trajet.get_dateheure_fin(), str):
            date_fin = datetime.strptime(nouv_trajet.get_dateheure_fin(), "%Y-%m-%d %H:%M:%S")
        else:
            date_fin = nouv_trajet.get_dateheure_fin()
        
        valeurs = (
            nouv_trajet.get_station_depart().get_numStation(),
            nouv_trajet.get_station_arrivee().get_numStation(),
            nouv_trajet.get_nbr_km(),
            date_debut,
            date_fin,
            nouv_trajet.get_abonne().get_carteAbo(),
            nouv_trajet.get_refVelo()
        )

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            connection.commit()
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

    # Recherche d'un trajet en particulier avec son refTrajet
    def find_trajet(self, id_trajet):
        sql = "SELECT * FROM trajet WHERE refTrajet = %s"
        valeurs = (id_trajet,)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, (valeurs))
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
            un_trajet.get_station_depart().get_numStation(),
            un_trajet.get_station_arrivee().get_numStation(), 
            un_trajet.get_nbr_km(),
            un_trajet.get_dateheure_debut(),
            un_trajet.get_dateheure_fin(),
            un_trajet.get_abonne().get_carteAbo(),
            un_trajet.get_refVelo(),
            un_trajet.get_refTrajet()
        )
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            connection.commit()
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

    # Suppression d'un trajet dans la BDD
    def delete_trajet(self, id_trajet):
        sql = "DELETE FROM trajet WHERE refTrajet = %s"
        valeurs = (id_trajet.get_refTrajet(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            connection.commit()
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

    # Recherche des trajets
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

    # Méthode permettant de trouver les trajets effectué par un abonné grâce à son id
    def select_trajets_abonne(self, carteAbo):
        connection = DAOSession.get_connexion()
        cursor = connection.cursor(dictionary=True)  
        sql = "SELECT * FROM trajet WHERE carteAbo = %s"
        cursor.execute(sql, (carteAbo,))
        rows = cursor.fetchall()

        trajets = []
        for row in rows:
            station_depart = DAOStation.get_instance().find_station(row["station_depart"])
            station_arrivee = DAOStation.get_instance().find_station(row["station_arrivee"])
            velo = DAOVelo.get_instance().find_velo(row["refVelo"])
            abonne = DAOAbonne.get_instance().find_abonne(row["carteAbo"])

            trajet = Trajet(
                row["refTrajet"], 
                station_depart, 
                station_arrivee, 
                row["nbr_km"], 
                row["dateheure_debut"], 
                row["dateheure_fin"], 
                abonne, 
                velo
            )
            trajets.append(trajet)

        cursor.close()
        return trajets

    # Méthode pour transformer une ligne en un objet Trajet
    def set_all_values(self, rs):
        try:
            station_depart = DAOStation.get_instance().find_station(rs["station_depart"])
            station_arrivee = DAOStation.get_instance().find_station(rs["station_arrivee"])
            velo = DAOVelo.get_instance().find_velo(rs["refVelo"])
            abonne = DAOAbonne.get_instance().find_abonne(rs["carteAbo"])

            trajet = Trajet(
                rs["refTrajet"], 
                station_depart, 
                station_arrivee, 
                rs["nbr_km"], 
                rs["dateheure_debut"], 
                rs["dateheure_fin"], 
                abonne, 
                velo
            )
            return trajet
        except KeyError as e:
            print(f"Erreur lors de la récupération des données : {e}")
            return None