from mysql.connector import Error
from DAO.DAOSession import DAOSession
from entités.personne import Personne

class DAOPersonne:
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOPersonne.unique_instance is None:
            DAOPersonne.unique_instance = DAOPersonne()
        return DAOPersonne.unique_instance

    # Insertion d'une personne dans la BDD
    def insert_personne(self, une_personne):
        sql = "INSERT INTO personne (nom, prenom, email, mot_de_passe, role) VALUES (%s, %s, %s, %s, %s)"
        valeurs = (une_personne.get_nom(), une_personne.get_prenom(), une_personne.get_email(), une_personne.get_mot_de_passe(), une_personne.get_role())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            cle = cursor.lastrowid
            return cle
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création de la personne : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return -1
        finally:
            if cursor:
                cursor.close()

    # Suppression d'une personne dans la BDD
    def delete_personne(self, une_personne):
        sql = "DELETE FROM personne WHERE id_personne = %s"
        valeurs = (une_personne.get_id_personne(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la suppression de la personne : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    # Recherche d'une personne par son ID
    def find_personne(self, id_personne):
        sql = "SELECT * FROM personne WHERE id_personne = %s"
        valeurs = (id_personne,)
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
            print(f"Erreur lors de la recherche de la personne : {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    # Mise à jour d'une personne
    def update_personne(self, une_personne):
        sql = "UPDATE personne SET nom = %s, prenom = %s, email = %s, mot_de_passe = %s, role = %s WHERE id_personne = %s"
        valeurs = (une_personne.get_nom(), une_personne.get_prenom(), une_personne.get_email(), une_personne.get_mot_de_passe(), une_personne.get_role(), une_personne.get_id_personne())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la mise à jour de la personne : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    # Sélectionner des personnes par critères (nom, email, rôle, etc.)
    def select_personne(self, critere_nom=None, critere_email=None, critere_role=None):
        les_personnes = []
        sql = "SELECT * FROM personne WHERE "
        valeurs = []

        if critere_nom:
            sql += "nom = %s"
            valeurs.append(critere_nom)
        if critere_email:
            if len(valeurs) > 0:
                sql += " AND "
            sql += "email = %s"
            valeurs.append(critere_email)
        if critere_role:
            if len(valeurs) > 0:
                sql += " AND "
            sql += "role = %s"
            valeurs.append(critere_role)

        if len(valeurs) == 0:
            sql = "SELECT * FROM personne"  # Si aucun critère n'est fourni, on sélectionne toutes les personnes

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, tuple(valeurs))
            rs = cursor.fetchall()
            for row in rs:
                les_personnes.append(self.set_all_values(row))
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche de la personne : {e}")
            print(sql)
            print(valeurs)
        finally:
            if cursor:
                cursor.close()
        return les_personnes

    # Méthode pour transformer une ligne de résultats en un objet Personne
    def set_all_values(self, rs):
        une_personne = Personne(rs["id_personne"], rs["nom"], rs["prenom"], rs["email"], rs["mot_de_passe"], rs["role"])
        return une_personne