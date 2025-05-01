from mysql.connector import Error
from DAO.DAOSession import DAOSession
from entites.personne import Administrateur

class DAOAdministrateur:
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOAdministrateur.unique_instance is None:
            DAOAdministrateur.unique_instance = DAOAdministrateur()
        return DAOAdministrateur.unique_instance

    # Insertion d'un administrateur dans la BDD
    def insert_administrateur(self, nouv_admin):
        sql = "INSERT INTO administrateur (email, mdp, nom, prenom, num_tel) VALUES (%s, %s, %s, %s, %s)"
        valeurs = (nouv_admin.get_email(), nouv_admin.get_mdp(), nouv_admin.get_nom(), nouv_admin.get_prenom(), nouv_admin.get_num_tel())
        cursor = None
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            connection.commit()
            return cursor.lastrowid
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de l'insertion de l'administrateur : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return -1
        finally:
            if cursor:
                cursor.close()

    # Recherche d'un administrateur par son ID
    def find_administrateur(self, id_admin):
        sql = "SELECT * FROM administrateur WHERE id_admin = %s"
        valeurs = (id_admin,)
        cursor = None
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
            print(f"Erreur lors de la recherche d'un administrateur : {e}")
            print(sql)
            print(valeurs)
            return None
        finally:
            if cursor:
                cursor.close()

    # Mise à jour des informations de l'administrateur
    def update_administrateur(self, un_admin):
        sql = "UPDATE administrateur SET email = %s, mdp = %s, nom = %s, prenom = %s, num_tel = %s WHERE id_admin = %s"
        valeurs = (un_admin.get_email(), un_admin.get_mdp(), un_admin.get_nom(), un_admin.get_prenom(), un_admin.get_num_tel(), un_admin.get_id_admin())
        cursor = None
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            connection.commit()
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la mise à jour de l'administrateur : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    # Sélection de tous les administrateurs
    def select_administrateurs(self):
        les_admins = []
        sql = "SELECT * FROM administrateur"
        cursor = None
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql)
            rs = cursor.fetchall()
            for row in rs:
                les_admins.append(self.set_all_values(row))
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche d'administrateurs : {e}")
            print(sql)
        finally:
            if cursor:
                cursor.close()
        return les_admins

    # Méthode pour transformer une ligne de résultats (rs) en un objet Administrateur
    def set_all_values(self, rs):
        try:
            admin = Administrateur(
                id_admin=rs["id_admin"],
                email=rs["email"],
                mdp=rs["mdp"],
                nom=rs["nom"],
                prenom=rs["prenom"],
                num_tel=rs["num_tel"]
            )
            return admin
        except KeyError as e:
            print(f"Erreur lors de la récupération des données : {e}")
            return None