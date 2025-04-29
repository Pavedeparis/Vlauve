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
        sql = "INSERT INTO ville (idVille, nom, code_postal, tarif_min_gratuite, tarif_demi_occ, tarif_demi_ann) VALUES (%s, %s, %s, %s, %s, %s)"
        valeurs = (une_ville.get_idVille(), une_ville.get_nom(), une_ville.get_code_postal(), une_ville.get_tarif_min_gratuite(), une_ville.get_tarif_demi_occ(), une_ville.get_tarif_demi_ann())
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
        sql = "DELETE FROM ville WHERE idVille = %s"
        valeurs = (une_ville.get_idVille(),)
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
    def find_ville(self, idVille):
        sql = "SELECT * FROM ville WHERE idVille = %s"
        valeurs = (idVille,)
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
        sql = "UPDATE ville SET nom = %s, code_postal = %s, tarif_min_gratuite = %s, tarif_demi_occ = %s, tarif_demi_ann = %s WHERE idVille = %s"
        valeurs = (une_ville.get_nom(), une_ville.get_code_postal(), une_ville.get_tarif_min_gratuite(), une_ville.get_tarif_demi_occ(), une_ville.get_tarif_demi_ann(), une_ville.get_idVille())
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
        critere_id = une_ville.get_idVille()
        critere_nom = une_ville.get_nom()
        critere_code_postal = une_ville.get_code_postal()
        valeurs = []

        if critere_id is not None:
            sql += "idVille = %s"
            valeurs.append(critere_id)
        else:
            sql = "SELECT * FROM ville"

        # Ajout des autres critères à la requête SQL si nécessaire
        if critere_nom is not None:
            sql += " AND nom = %s"
            valeurs.append(critere_nom)
        if critere_code_postal is not None:
            sql += " AND code_postal = %s"
            valeurs.append(critere_code_postal)

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
        from entites.ville import Ville
        une_ville = Ville(rs["idVille"], rs["nom"], rs["code_postal"], rs["tarif_min_gratuite"], rs["tarif_demi_occ"], rs["tarif_demi_ann"])
        return une_ville