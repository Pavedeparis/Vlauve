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
    def insert_paiement(self, nouv_paie):
        sql = "INSERT INTO paiement (date, montant, idFact) VALUES (%s, %s, %s)"
        valeurs = (nouv_paie.get_date(), nouv_paie.get_montant(), nouv_paie.get_idFact())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            connection.commit()
            return cursor.lastrowid
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

    # Recherche d'un paiement par son ID
    def find_paiement(self, id_paie):
        sql = "SELECT * FROM paiement WHERE idPaie = %s"
        valeurs = (id_paie,)
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
            connection.commit()
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

    # Suppression d'un paiement dans la BDD
    def delete_paiement(self, id_paie):
        sql = "DELETE FROM paiement WHERE idPaie = %s"
        valeurs = (id_paie.get_idPaie(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            connection.commit()
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
            sql = "SELECT * FROM paiement" 

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

    # Rechercher tous les paiements
    def select_paiements(self):
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
        try:
            un_paiement = Paiement(
                rs["idPaie"], 
                rs["date"], 
                rs["montant"], 
                rs["idFact"]
                )
            return un_paiement
        except KeyError as e:
            print(f"Erreur lors de la récupération des données : {e}")
            return None