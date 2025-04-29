from mysql.connector import Error
from DAO.DAOSession import DAOSession
from entites.paiement import Paiement

class DAOPaiement:
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOPaiement.unique_instance is None:
            DAOPaiement.unique_instance = DAOPaiement()
        return DAOPaiement.unique_instance

    # Insertion d'un paiement dans la BDD
    def insert_paiement(self, un_paiement):
        sql = "INSERT INTO paiement (date, montant, idFact) VALUES (%s, %s, %s)"
        valeurs = (un_paiement.get_date(), un_paiement.get_montant(), un_paiement.get_idFact())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            cle = cursor.lastrowid
            return cle
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création du paiement : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return -1
        finally:
            if cursor:
                cursor.close()

    # Suppression d'un paiement dans la BDD
    def delete_paiement(self, un_paiement):
        sql = "DELETE FROM paiement WHERE idPaie = %s"
        valeurs = (un_paiement.get_idPaie(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la suppression du paiement : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    # Recherche d'un paiement par son ID
    def find_paiement(self, idPaie):
        sql = "SELECT * FROM paiement WHERE idPaie = %s"
        valeurs = (idPaie,)
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
            print(f"Erreur lors de la recherche d'un paiement : {e}")
            print(sql)
            print(valeurs)
            return None
        finally:
            if cursor:
                cursor.close()

    # Mise à jour d'un paiement
    def update_paiement(self, un_paiement):
        sql = "UPDATE paiement SET date = %s, montant = %s WHERE idPaie = %s"
        valeurs = (un_paiement.get_date(), un_paiement.get_montant(), un_paiement.get_idPaie())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la mise à jour de paiement : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    # Recherche les paiements selon des critères
    def select_paiement(self, critere_facture=None, critere_date=None):
        les_paiements = []
        sql = "SELECT * FROM paiement WHERE "
        valeurs = []

        if critere_facture:
            sql += "idFact = %s"
            valeurs.append(critere_facture.get_idFact())
        if critere_date:
            if len(valeurs) > 0:
                sql += " AND "
            sql += "date = %s"
            valeurs.append(critere_date)

        if len(valeurs) == 0:
            sql = "SELECT * FROM paiement"  # Si aucun critère n'est fourni, on sélectionne tous les paiements

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, tuple(valeurs))
            rs = cursor.fetchall()
            for row in rs:
                les_paiements.append(self.set_all_values(row))
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche des paiements : {e}")
            print(sql)
            print(valeurs)
        finally:
            if cursor:
                cursor.close()
        return les_paiements

    def select_paiement(self, critere_facture=None, critere_date=None):
        les_paiements = []
        sql = "SELECT * FROM paiement "
   
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql)
            rs = cursor.fetchall()
            for row in rs:
                les_paiements.append(self.set_all_values(row))
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche des paiements : {e}")
            print(sql)
        finally:
            if cursor:
                cursor.close()
        return les_paiements
    
    # Méthode pour transfromer une ligne en un objet Paiement
    def set_all_values(self, rs):
        un_paiement = Paiement(rs["idPaie"], rs["date"], rs["montant"], rs["idFact"])
        return un_paiement
