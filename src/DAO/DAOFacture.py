from mysql.connector import Error
from DAO.DAOSession import DAOSession
from entités.facture import Facture

class DAOFacture:
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOFacture.unique_instance is None:
            DAOFacture.unique_instance = DAOFacture()
        return DAOFacture.unique_instance

    # Insertion d'une facture dans la BDD
    def insert_facture(self, une_facture):
        sql = "INSERT INTO facture (id_abonne, date, montant, duree) VALUES (%s, %s, %s, %s)"
        valeurs = (une_facture.get_abonne().get_id_abonne(), une_facture.get_date(), une_facture.get_montant(), une_facture.get_duree())
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
        sql = "DELETE FROM facture WHERE id_facture = %s"
        valeurs = (une_facture.get_id_facture(),)
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
    def find_facture(self, id_facture):
        sql = "SELECT * FROM facture WHERE id_facture = %s"
        valeurs = (id_facture,)
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
        sql = "UPDATE facture SET date = %s, montant = %s, duree = %s WHERE id_facture = %s"
        valeurs = (une_facture.get_date(), une_facture.get_montant(), une_facture.get_duree(), une_facture.get_id_facture())
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
    def select_facture(self, critere_abonne=None, critere_date=None):
        les_factures = []
        sql = "SELECT * FROM facture WHERE "
        valeurs = []

        if critere_abonne:
            sql += "id_abonne = %s"
            valeurs.append(critere_abonne.get_id_abonne())
        if critere_date:
            if len(valeurs) > 0:
                sql += " AND "
            sql += "date = %s"
            valeurs.append(critere_date)
        
        if len(valeurs) == 0:
            sql = "SELECT * FROM facture"  # Si aucun critère n'est fourni, on sélectionne toutes les factures

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, tuple(valeurs))
            rs = cursor.fetchall()
            for row in rs:
                les_factures.append(self.set_all_values(row))
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche de facture : {e}")
            print(sql)
            print(valeurs)
        finally:
            if cursor:
                cursor.close()
        return les_factures

    # Méthode pour transformer chaque ligne de résultat en un objet Facture
    def set_all_values(self, rs):
        abonne = DAOSession.get_instance().find_abonne(rs["id_abonne"])
        une_facture = Facture(rs["id_facture"], abonne, rs["date"], rs["montant"], rs["duree"])
        return une_facture
