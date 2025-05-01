from mysql.connector import Error
from DAO.DAOSession import DAOSession
from entites.contrat import Contrat

class DAOContrat:
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOContrat.unique_instance is None:
            DAOContrat.unique_instance = DAOContrat()
        return DAOContrat.unique_instance

    # Insertion d'un contrat
    def insert_contrat(self, nouv_contrat):
        sql = "INSERT INTO contrat (idAbo, carteAbo, date_debut, date_fin, montant, garantie, carte_identite) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        valeurs = (nouv_contrat.idAbo, nouv_contrat.carteAbo, nouv_contrat.date_debut, nouv_contrat.date_fin, nouv_contrat.montant, nouv_contrat.garantie, nouv_contrat.carte_identite)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            connection.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Erreur insertion contrat : {e}")
            connection.rollback()
            return -1
        finally:
            if cursor:
                cursor.close()

    # Trouver un contrat par son ID
    def find_contrat(self, id_contrat):
        sql = "SELECT * FROM contrat WHERE idCont = %s"
        valeurs = (id_contrat,)
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
            print(f"Erreur lors de la recherche d'un contrat : {e}")
            print(sql)
            print(valeurs)
            return None
        finally:
            if cursor:
                cursor.close()

    # Mettre à jour un contrat
    def update_contrat(self, un_contrat):
        sql = "UPDATE contrat SET date_debut = %s, date_fin = %s, montant = %s, garantie = %s, carte_identite = %s WHERE idCont = %s"
        valeurs = (un_contrat.get_date_debut(), un_contrat.get_date_fin(), un_contrat.get_montant(),
                   un_contrat.get_garantie(), un_contrat.carte_identite(),
                   un_contrat.get_idCont())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            connection.commit()
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la mise à jour du contrat : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    # Suppression d'un contrat
    def delete_contrat(self, id_contrat):
        sql = "DELETE FROM contrat WHERE idCont = %s"
        valeurs = (id_contrat.get_idCont(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            connection.commit()
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la suppression d'un contrat : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    # Rechercher les contrats
    def select_contrat(self):
        les_contrats = []
        sql = "SELECT * FROM contrat "

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql)
            rs = cursor.fetchall()
            for row in rs:
                les_contrats.append(self.set_all_values(row))
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche de contrat : {e}")
            print(sql)
        finally:
            if cursor:
                cursor.close()
        return les_contrats

    # Méthode pour transformer chaque ligne en un objet Contrat
    def set_all_values(self, rs):
        try:
            un_contrat = Contrat(
                rs["idCont"], 
                rs["idAbo"], 
                rs["carteAbo"], 
                rs["date_debut"], 
                rs["date_fin"], 
                rs["montant"], 
                rs["garantie"], 
                rs["carte_identite"]
                )
            return un_contrat
        except KeyError as e:
            print(f"Erreur lors de la récupération des données : {e}")
            return None