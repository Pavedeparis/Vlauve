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
    def insert_reseau(self, nouv_res):
        sql = "INSERT INTO reseau (numRes, nom, annee, idVille) VALUES (%s, %s, %s, %s)"
        valeurs = (nouv_res.get_numRes(), nouv_res.get_nom(), nouv_res.get_annee(), nouv_res.get_ville().get_idVille())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            connection.commit()
            return cursor.lastrowid
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

    # Recherche d'un réseau par son ID
    def find_reseau(self, id_res):
        sql = "SELECT * FROM reseau WHERE numRes = %s"
        valeurs = (id_res,)
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
        sql = "UPDATE reseau SET nom = %s, annee = %s, idVille = %s WHERE numRes = %s"
        valeurs = (un_reseau.get_nom(), un_reseau.get_annee(), un_reseau.get_ville().get_idVille(), un_reseau.get_numRes())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            connection.commit()
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

    # Suppression d'un réseau de la base de données
    def delete_reseau(self, id_res):
        sql = "DELETE FROM reseau WHERE numRes = %s"
        valeurs = (id_res.get_numRes(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            connection.commit()
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

    # Sélection des réseaux avec des critères
    def select_reseau(self, un_reseau):
        les_reseaux = []
        sql = "SELECT * FROM reseau WHERE "
        critere_id = un_reseau.get_numRes()
        critere_nom = un_reseau.get_nom()
        critere_annee = un_reseau.get_annee()
        critere_ville = un_reseau.get_ville()
        valeurs = []

        if critere_id is not None:
            sql += "numRes = %s"
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
            sql += " AND idVille = %s"
            valeurs.append(critere_ville.get_idVille())

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
        from entites.reseau import Reseau
        from entites.ville import Ville
        try: 
            idVille = Ville(
                rs["idVille"], 
                rs["nom_ville"], 
                rs["codepostal"], 
                rs["px_min_gratuites"], 
                rs["px_abo_annuel"], 
                rs["px_abo_occasionnel"]
                )
            un_reseau = Reseau(
                rs["numRes"], 
                rs["nom"], 
                rs["annee"], 
                idVille
                )
            return un_reseau
        except KeyError as e:
            print(f"Erreur lors de la récupération des données : {e}")
            return None