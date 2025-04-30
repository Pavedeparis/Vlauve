from entites.abonnement import Abonnement
from mysql.connector import Error
from DAO.DAOSession import DAOSession

class DAOAbonnement:
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOAbonnement.unique_instance is None:
            DAOAbonnement.unique_instance = DAOAbonnement()
        return DAOAbonnement.unique_instance

    # Insertion d'un abonnement dans la BDD
    def insert_abonnement(self, un_abonnement):
        sql = "INSERT INTO abonnement (idAbo, type_abo, sous_type) VALUES (%s, %s, %s)"
        valeurs = (un_abonnement.get_idAbo(), un_abonnement.get_type_abo(), un_abonnement.get_sous_type())

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            cle = cursor.lastrowid
            return cle
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création d'un abonnement : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return -1
        finally:
            if cursor:
                cursor.close()

    # Suppression d'un abonnement dans la BDD
    def delete_abonnement(self, un_abonnement):
        sql = "DELETE FROM abonnement WHERE idAbo = %s"
        valeurs = (un_abonnement.get_idAbo(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la suppression de l'abonnement : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    # Recherche d'un abonnement par ID
    def find_abonnement(self, idAbo):
        sql = "SELECT * FROM abonnement WHERE idAbo = %s"
        valeurs = (idAbo,)
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
            print(f"Erreur lors de la recherche d'un abonnement : {e}")
            print(sql)
            print(valeurs)
            return None
        finally:
            if cursor:
                cursor.close()

    # Mise à jour des informations d'un abonnement : à revoir
    def update_abonnement(self, un_abonnement):
        sql = "UPDATE abonnement SET type_abo = %s, sous_type = %s WHERE idAbo = %s"
        valeurs = (un_abonnement.get_type_abo(), un_abonnement.get_sous_type(), un_abonnement.get_idAbo())

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la mise à jour de l'abonnement : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    # recherche d'abonnements avec critères
    def select_abonnement(self):
        les_abonnements = []
        sql = "SELECT * FROM abonnement "

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql)
            rs = cursor.fetchall()
            for row in rs:
                les_abonnements.append(self.set_all_values(row))
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche des abonnements : {e}")
            print(sql)
        finally:
            if cursor:
                cursor.close()
        return les_abonnements
    
    # Méthode qui retourne l'abonnement correspondant aux critères fournis (pour l'inscription notamment)
    def select_abonnement_criteres(self, type_abo=None, sous_type=None):
        sql = "SELECT * FROM abonnement WHERE 1=1" # Astuce de WHERE 1=1 pour rendre ça dynamique et ne pas s'encombrer avec des doublons de WHERE
        valeurs = []

        if type_abo:
            sql += " AND type_abo = %s"
            valeurs.append(type_abo)
        if sous_type is not None:
            sql += " AND sous_type = %s"
            valeurs.append(sous_type)

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, tuple(valeurs))
            rs = cursor.fetchone()
            if rs:
                return self.set_all_values(rs)
            return None
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche avec critères : {e}")
            print(sql)
            print(valeurs)
            return None
        finally:
            if cursor:
                cursor.close()


    # Méthode pour transformer une ligne de résultats en un objet Abonnement
    def set_all_values(self, rs):
        return Abonnement(rs["idAbo"], rs["type_abo"], rs["sous_type"])
