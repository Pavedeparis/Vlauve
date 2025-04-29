from mysql.connector import Error
from DAO.DAOSession import DAOSession
from entites.facture import Facture

class DAOFacture:
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOFacture.unique_instance is None:
            DAOFacture.unique_instance = DAOFacture()
        return DAOFacture.unique_instance

    # Insertion d'une facture dans la BDD
    def insert_facture(self, une_facture):
        sql = "INSERT INTO facture (date, montant, carteAbo) VALUES (%s, %s, %s, %s)"
        valeurs = (une_facture.get_date(), une_facture.get_montant(), une_facture.get_carteAbo())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            cle = cursor.lastrowid
            return cle
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création de la facture : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return -1
        finally:
            if cursor:
                cursor.close()
                
    # Suppression d'une facture dans la BDD
    def delete_facture(self, une_facture):
        sql = "DELETE FROM facture WHERE idFact = %s"
        valeurs = (une_facture.get_idFact(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la suppression de la facture : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    # Recherche d'une facture par son ID
    def find_facture(self, idFact):
        sql = "SELECT * FROM facture WHERE idFact = %s"
        valeurs = (idFact,)
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
            print(f"Erreur lors de la recherche de la facture : {e}")
            print(sql)
            print(valeurs)
            return None
        finally:
            if cursor:
                cursor.close()

    # Mise à jour d'une facture
    def update_facture(self, une_facture):
        sql = "UPDATE facture SET date = %s, montant = %s, WHERE idFact = %s"
        valeurs = (une_facture.get_date(), une_facture.get_montant(), une_facture.get_idFact())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la mise à jour de la facture : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    # Rechercher des factures selon des critères
    def select_facture(self):
        les_factures = []
        sql = "SELECT * FROM facture"

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql)
            rs = cursor.fetchall()
            for row in rs:
                les_factures.append(self.set_all_values(row))
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche de facture : {e}")
            print(sql)
        finally:
            if cursor:
                cursor.close()
        return les_factures

    # Méthode pour transformer chaque ligne de résultat en un objet Facture
    def set_all_values(self, rs):
        une_facture = Facture(rs["idFact"], rs["date"], rs["montant"], rs["carteAbo"])
        return une_facture
