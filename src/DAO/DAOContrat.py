from mysql.connector import Error
from DAO.DAOSession import DAOSession
from entités.contrat import Contrat

class DAOContrat:
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOContrat.unique_instance is None:
            DAOContrat.unique_instance = DAOContrat()
        return DAOContrat.unique_instance

    # Insertion d'un contrat
    def insert_contrat(self, un_contrat):
        sql = "INSERT INTO contrat (id_abonnement, id_abonne, date_debut, date_fin, montant, depot_garantie, num_carte_identite) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        valeurs = (un_contrat.get_abonnement().get_id_abonnement(), 
                   un_contrat.get_abonne().get_id_abonne(),
                   un_contrat.get_date_debut(), 
                   un_contrat.get_date_fin(),
                   un_contrat.get_montant(),
                   un_contrat.get_depot_garantie(),
                   un_contrat.get_num_carte_identite())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            cle = cursor.lastrowid
            return cle
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création du contrat : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return -1
        finally:
            if cursor:
                cursor.close()
    
    # Suppression d'un contrat
    def delete_contrat(self, un_contrat):
        sql = "DELETE FROM contrat WHERE id_contrat = %s"
        valeurs = (un_contrat.get_id_contrat(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
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

    # Trouver un contrat par son ID
    def find_contrat(self, id_contrat):
        sql = "SELECT * FROM contrat WHERE id_contrat = %s"
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
        sql = "UPDATE contrat SET date_debut = %s, date_fin = %s, montant = %s, depot_garantie = %s, num_carte_identite = %s WHERE id_contrat = %s"
        valeurs = (un_contrat.get_date_debut(), un_contrat.get_date_fin(), un_contrat.get_montant(),
                   un_contrat.get_depot_garantie(), un_contrat.get_num_carte_identite(),
                   un_contrat.get_id_contrat())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
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

    # Rechercher les contrats associés à un abonné ou un abonnement
    def select_contrat(self, critere_abonne=None, critere_abonnement=None):
        les_contrats = []
        sql = "SELECT * FROM contrat WHERE "
        valeurs = []

        if critere_abonne:
            sql += "id_abonne = %s"
            valeurs.append(critere_abonne.get_id_abonne())
        if critere_abonnement:
            if len(valeurs) > 0:
                sql += " AND "
            sql += "id_abonnement = %s"
            valeurs.append(critere_abonnement.get_id_abonnement())
        
        if len(valeurs) == 0:
            sql = "SELECT * FROM contrat" 

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, tuple(valeurs))
            rs = cursor.fetchall()
            for row in rs:
                les_contrats.append(self.set_all_values(row))
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche de contrat : {e}")
            print(sql)
            print(valeurs)
        finally:
            if cursor:
                cursor.close()
        return les_contrats

    # Méthode pour transformer chaque ligne en un objet Contrat
    def set_all_values(self, rs):
        abonnement = DAOSession.get_instance().find_abonnement(rs["id_abonnement"])
        abonne = DAOSession.get_instance().find_abonne(rs["id_abonne"])
        un_contrat = Contrat(rs["id_contrat"], abonnement, abonne, rs["date_debut"], rs["date_fin"], rs["montant"], rs["depot_garantie"], rs["num_carte_identite"])
        return un_contrat
