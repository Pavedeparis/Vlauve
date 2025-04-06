from entités.abonnement import Abonnement
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
        sql = "INSERT INTO abonnement (id_abonnement) VALUES (%s)"
        valeurs = (un_abonnement.get_id_abonnement(),)
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
        sql = "DELETE FROM abonnement WHERE id_abonnement = %s"
        valeurs = (un_abonnement.get_id_abonnement(),)
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
    def find_abonnement(self, id_abonnement):
        sql = "SELECT * FROM abonnement WHERE id_abonnement = %s"
        valeurs = (id_abonnement,)
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

    # Mise à jour des informations d'un abonnement
    def update_abonnement(self, un_abonnement):
        sql = "UPDATE abonnement SET id_abonnement = %s WHERE id_abonnement = %s"
        valeurs = (un_abonnement.get_id_abonnement(), un_abonnement.get_id_abonnement())
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
    def select_abonnement(self, un_abonnement):
        les_abonnements = []
        sql = "SELECT * FROM abonnement WHERE "
        critere_id = un_abonnement.get_id_abonnement()
        valeurs = []

        if critere_id is not None:
            sql += "id_abonnement = %s"
            valeurs.append(critere_id)
        else:
            sql = "SELECT * FROM abonnement"

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, tuple(valeurs))
            rs = cursor.fetchall()
            for row in rs:
                les_abonnements.append(self.set_all_values(row))
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche des abonnements : {e}")
            print(sql)
            print(valeurs)
        finally:
            if cursor:
                cursor.close()
        return les_abonnements

    # Méthode pour transformer une ligne de résultats en un objet Abonnement
    def set_all_values(self, rs):
        un_abonnement = Abonnement(rs["id_abonnement"])
        return un_abonnement