from mysql.connector import Error
from DAO.DAOSession import DAOSession

class DAOReseau:
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOReseau.unique_instance is None:
            DAOReseau.unique_instance = DAOReseau()
        return DAOReseau.unique_instance

    # Insertion d'un réseau dans la BDD
    def insert_reseau(self, un_reseau):
        sql = "INSERT INTO reseau (id_reseau, nom, annee, id_ville) VALUES (%s, %s, %s, %s)"
        valeurs = (un_reseau.get_id_reseau(), un_reseau.get_nom(), un_reseau.get_annee(), un_reseau.get_ville().get_id_ville())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            cle = cursor.lastrowid
            return cle
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création du réseau : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return -1
        finally:
            if cursor:
                cursor.close()

    # Suppression d'un réseau de la base de données
    def delete_reseau(self, un_reseau):
        sql = "DELETE FROM reseau WHERE id_reseau = %s"
        valeurs = (un_reseau.get_id_reseau(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la suppression du réseau : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    # Recherche d'un réseau par son ID
    def find_reseau(self, id_reseau):
        sql = "SELECT * FROM reseau WHERE id_reseau = %s"
        valeurs = (id_reseau,)
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
            print(f"Erreur lors de la recherche du réseau : {e}")
            print(sql)
            print(valeurs)
            return None
        finally:
            if cursor:
                cursor.close()

    # Mise à jour des informations d'un réseau
    def update_reseau(self, un_reseau):
        sql = "UPDATE reseau SET nom = %s, annee = %s, id_ville = %s WHERE id_reseau = %s"
        valeurs = (un_reseau.get_nom(), un_reseau.get_annee(), un_reseau.get_ville().get_id_ville(), un_reseau.get_id_reseau())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la mise à jour du réseau : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    # Sélection des réseaux avec des critères
    def select_reseau(self, un_reseau):
        les_reseaux = []
        sql = "SELECT * FROM reseau WHERE "
        critere_id = un_reseau.get_id_reseau()
        critere_nom = un_reseau.get_nom()
        critere_annee = un_reseau.get_annee()
        critere_ville = un_reseau.get_ville()
        valeurs = []

        if critere_id is not None:
            sql += "id_reseau = %s"
            valeurs.append(critere_id)
        else:
            sql = "SELECT * FROM reseau"

        # Ajout des autres critères à la requête SQL si nécessaire
        if critere_nom is not None:
            sql += " AND nom = %s"
            valeurs.append(critere_nom)
        if critere_annee is not None:
            sql += " AND annee = %s"
            valeurs.append(critere_annee)
        if critere_ville is not None:
            sql += " AND id_ville = %s"
            valeurs.append(critere_ville.get_id_ville())

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, tuple(valeurs))
            rs = cursor.fetchall()
            for row in rs:
                les_reseaux.append(self.set_all_values(row))
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche du réseau : {e}")
            print(sql)
            print(valeurs)
        finally:
            if cursor:
                cursor.close()
        return les_reseaux

    # Méthode pour transformer une ligne de résultats en un objet Reseau
    def set_all_values(self, rs):
        from entités.reseau import Reseau
        from entités.ville import Ville
        id_ville = Ville(rs["id_ville"], rs["nom_ville"], rs["codepostal"], rs["px_min_gratuites"], rs["px_abo_annuel"], rs["px_abo_occasionnel"])
        un_reseau = Reseau(rs["id_reseau"], rs["nom"], rs["annee"], id_ville)
        return un_reseau
