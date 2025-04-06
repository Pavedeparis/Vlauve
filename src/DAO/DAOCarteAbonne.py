from mysql.connector import Error
from DAO.DAOSession import DAOSession
from entités.carteAbonne import CarteAbonne

class DAOCarteAbonne:
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOCarteAbonne.unique_instance is None:
            DAOCarteAbonne.unique_instance = DAOCarteAbonne()
        return DAOCarteAbonne.unique_instance

    # Insertion d'une carte abonné dans la BDD
    def insert_carte_abonne(self, une_carte):
        sql = "INSERT INTO carte_abonne (id_abonne, type) VALUES (%s, %s)"
        valeurs = (une_carte.get_abonne().get_id_abonne(), une_carte.get_type())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            cle = cursor.lastrowid
            return cle
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création de la carte abonné : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return -1
        finally:
            if cursor:
                cursor.close()
    
    # Suppression d'une carte abonné dans la BDD
    def delete_carte_abonne(self, une_carte):
        sql = "DELETE FROM carte_abonne WHERE id_carte = %s"
        valeurs = (une_carte.get_id_carte(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la suppression de la carte abonné : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    # Recherche d'une carte abonné par son ID
    def find_carte_abonne(self, id_carte):
        sql = "SELECT * FROM carte_abonne WHERE id_carte = %s"
        valeurs = (id_carte,)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, valeurs)
            rs = cursor.fetchone()
            if rs:
                return self.set_all_values(rs)
            return None
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche d'une carte : {e}")
            print(sql)
            print(valeurs)
            return None
        finally:
            if cursor:
                cursor.close()

    # Mettre à jour d'une carte 
    def update_carte_abonne(self, une_carte):
        sql = "UPDATE carte_abonne SET type = %s WHERE id_carte = %s"
        valeurs = (une_carte.get_type(), une_carte.get_id_carte())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la mise à jour de la carte abonné : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    # Rechercher des cartes par critères
    def select_carte_abonne(self, une_carte):
        les_cartes = []
        sql = "SELECT * FROM carte_abonne WHERE "
        critere_id = une_carte.get_id_carte()
        critere_type = une_carte.get_type()
        critere_abonne = une_carte.get_abonne()
        valeurs = []

        if critere_id is not None:
            sql += "id_carte = %s"
            valeurs.append(critere_id)
        elif critere_type is None and critere_abonne is None:
            sql = "SELECT * FROM carte_abonne"
        else:
            conditions = []
            if critere_type is not None:
                conditions.append("type = %s")
                valeurs.append(critere_type)
            if critere_abonne is not None:
                conditions.append("id_abonne = %s")
                valeurs.append(critere_abonne.get_id_abonne())
            sql += " AND ".join(conditions)

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, tuple(valeurs))
            rs = cursor.fetchall()
            for row in rs:
                les_cartes.append(self.set_all_values(row))
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche des cartes abonnés : {e}")
            print(sql)
            print(valeurs)
        finally:
            if cursor:
                cursor.close()
        return les_cartes
    
    # Méthode pour transformer une ligne de résultats en un objet CarteAbonne
    def set_all_values(self, rs):
        from entités.abonne import Abonne
        abonne = DAOSession.get_instance().find_abonne(rs["id_abonne"])
        une_carte = CarteAbonne(rs["id_carte"], abonne, rs["type"])
        return une_carte