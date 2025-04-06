from mysql.connector import Error
from DAO.DAOSession import DAOSession
import entités.abonne as a 

class DAOAbonne:
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOAbonne.unique_instance is None:
            DAOAbonne.unique_instance = DAOAbonne()
        return DAOAbonne.unique_instance

    # Insertion d'un abonné dans la BDD
    def insert_abonne(self, un_abonne):
        sql = "INSERT INTO abonne (email, mot_de_passe, nom, prenom, numtel, nomrue, numrue, id_abonnement, id_ville) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        valeurs = (un_abonne.get_email(), un_abonne.get_mot_de_passe(), un_abonne.get_nom(), un_abonne.get_prenom(),
                   un_abonne.get_numtel(), un_abonne.get_nomrue(), un_abonne.get_numrue(),
                   un_abonne.get_abonnement().get_id_abonnement(), un_abonne.get_ville().get_id_ville())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            cle = cursor.lastrowid
            return cle
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création de l'abonné : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return -1
        finally:
            if cursor:
                cursor.close()

    # Suppression d'un abonné de la base de données
    def delete_abonne(self, un_abonne):
        sql = "DELETE FROM abonne WHERE id_abonne = %s"
        valeurs = (un_abonne.get_id_abonne(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la suppression de l'abonné : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    # Recherche d'un abonné par son ID
    def find_abonne(self, id_abonne):
        sql = "SELECT * FROM abonne WHERE id_abonne = %s"
        valeurs = (id_abonne,)
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
            print(f"Erreur lors de la recherche de l'abonné : {e}")
            print(sql)
            print(valeurs)
            return None
        finally:
            if cursor:
                cursor.close()

    # Mise à jour des informations d'un abonné
    def update_abonne(self, un_abonne):
        sql = "UPDATE abonne SET email = %s, mot_de_passe = %s, nom = %s, prenom = %s, numtel = %s, nomrue = %s, numrue = %s, id_abonnement = %s, id_ville = %s WHERE id_abonne = %s"
        valeurs = (un_abonne.get_email(), un_abonne.get_mot_de_passe(), un_abonne.get_nom(), un_abonne.get_prenom(),
                   un_abonne.get_numtel(), un_abonne.get_nomrue(), un_abonne.get_numrue(),
                   un_abonne.get_abonnement().get_id_abonnement(), un_abonne.get_ville().get_id_ville(),
                   un_abonne.get_id_abonne())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la mise à jour de l'abonné : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    # Recherche d'abonnés en utilisant des critères
    def select_abonne(self, un_abonne):
        les_abonnes = []
        sql = "SELECT * FROM abonne WHERE "
        critere_id = un_abonne.get_id_abonne()
        critere_nom = un_abonne.get_nom()
        critere_prenom = un_abonne.get_prenom()
        critere_email = un_abonne.get_email()
        critere_ville = un_abonne.get_ville()
        valeurs = []

        if critere_id is not None:
            sql += "id_abonne = %s"
            valeurs.append(critere_id)
        elif critere_nom == None and critere_prenom == None and critere_email == None:
            sql = "SELECT * FROM abonne"
        else:
            conditions = []
            if critere_nom is not None:
                conditions.append("nom = %s")
                valeurs.append(critere_nom)
            if critere_prenom is not None:
                conditions.append("prenom = %s")
                valeurs.append(critere_prenom)
            if critere_email is not None:
                conditions.append("email = %s")
                valeurs.append(critere_email)
            if critere_ville is not None:
                conditions.append("id_ville = %s")
                valeurs.append(critere_ville.get_id_ville())
            sql += " AND ".join(conditions)

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, tuple(valeurs))
            rs = cursor.fetchall()
            for row in rs:
                les_abonnes.append(self.set_all_values(row))
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche d'abonnés : {e}")
            print(sql)
            print(valeurs)
        finally:
            if cursor:
                cursor.close()
        return les_abonnes

    # Méthode pour transformer une ligne de résultats en un objet Abonne
    def set_all_values(self, rs):
        from entités.abonnement import Abonnement
        from entités.ville import Ville
        from entités.abonne import Abonne
        
        abonnement = Abonnement(rs["id_abonnement"])
        ville = Ville(rs["id_ville"], rs["nom_ville"], rs["codepostal"], rs["px_min_gratuites"], 
                      rs["px_abo_annuel"], rs["px_abo_occasionnel"])
        
        un_abonne = Abonne(rs["id_abonne"], rs["email"], rs["mot_de_passe"], rs["nom"], rs["prenom"],
                            rs["numtel"], rs["nomrue"], rs["numrue"], abonnement, ville)
        return un_abonne

