from mysql.connector import Error
from DAO.DAOSession import DAOSession

class DAOVille:
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOVille.unique_instance is None:
            DAOVille.unique_instance = DAOVille()
        return DAOVille.unique_instance

    # Insertion d'une ville dans la BDD
    def insert_ville(self, une_ville):
        sql = "INSERT INTO ville (id_ville, nom, codepostal, px_min_gratuites, px_abo_annuel, px_abo_occasionnel) VALUES (%s, %s, %s, %s, %s, %s)"
        valeurs = (une_ville.get_id_ville(), une_ville.get_nom(), une_ville.get_codepostal(), une_ville.get_px_min_gratuites(), une_ville.get_px_abo_annuel(), une_ville.get_px_abo_occasionnel())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            cle = cursor.lastrowid
            return cle
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création de la ville : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return -1
        finally:
            if cursor:
                cursor.close()

    # Suppression d'une ville de la BDD
    def delete_ville(self, une_ville):
        sql = "DELETE FROM ville WHERE id_ville = %s"
        valeurs = (une_ville.get_id_ville(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la suppression de la ville : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    # Recherche d'une ville par son ID
    def find_ville(self, id_ville):
        sql = "SELECT * FROM ville WHERE id_ville = %s"
        valeurs = (id_ville,)
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
            print(f"Erreur lors de la recherche de la ville : {e}")
            print(sql)
            print(valeurs)
            return None
        finally:
            if cursor:
                cursor.close()

    # Mise à jour des informations d'une ville
    def update_ville(self, une_ville):
        sql = "UPDATE ville SET nom = %s, codepostal = %s, px_min_gratuites = %s, px_abo_annuel = %s, px_abo_occasionnel = %s WHERE id_ville = %s"
        valeurs = (une_ville.get_nom(), une_ville.get_codepostal(), une_ville.get_px_min_gratuites(), une_ville.get_px_abo_annuel(), une_ville.get_px_abo_occasionnel(), une_ville.get_id_ville())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la mise à jour de la ville : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    # Sélection des villes avec des critères
    def select_ville(self, une_ville):
        les_villes = []
        sql = "SELECT * FROM ville WHERE "
        critere_id = une_ville.get_id_ville()
        critere_nom = une_ville.get_nom()
        critere_codepostal = une_ville.get_codepostal()
        valeurs = []

        if critere_id is not None:
            sql += "id_ville = %s"
            valeurs.append(critere_id)
        else:
            sql = "SELECT * FROM ville"

        # Ajout des autres critères à la requête SQL si nécessaire
        if critere_nom is not None:
            sql += " AND nom = %s"
            valeurs.append(critere_nom)
        if critere_codepostal is not None:
            sql += " AND codepostal = %s"
            valeurs.append(critere_codepostal)

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, tuple(valeurs))
            rs = cursor.fetchall()
            for row in rs:
                les_villes.append(self.set_all_values(row))
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche des villes : {e}")
            print(sql)
            print(valeurs)
        finally:
            if cursor:
                cursor.close()
        return les_villes

    # Méthode pour transformer une ligne de résultats en un objet Ville
    def set_all_values(self, rs):
        from entités.ville import Ville
        une_ville = Ville(rs["id_ville"], rs["nom"], rs["codepostal"], rs["px_min_gratuites"], rs["px_abo_annuel"], rs["px_abo_occasionnel"])
        return une_ville