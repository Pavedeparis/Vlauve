from mysql.connector import Error
from DAO.DAOSession import DAOSession
from entites.personne import Abonne

class DAOAbonne:
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOAbonne.unique_instance is None:
            DAOAbonne.unique_instance = DAOAbonne()
        return DAOAbonne.unique_instance

    # Insertion d'un abonné dans la BDD
    def insert_abonne(self, un_abonne):
        sql = """INSERT INTO abonne (email, mdp, nom, prenom, num_tel, num_rue, nom_rue, num_cb, ville) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        valeurs = (un_abonne.get_email(), un_abonne.get_mdp(), un_abonne.get_nom(), un_abonne.get_prenom(),
                   un_abonne.get_num_tel(), un_abonne.get_num_rue(), un_abonne.get_nom_rue(), un_abonne.get_num_cb(), un_abonne.get_ville())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            connection.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Erreur lors de l'insertion de l'abonné : {e}")
            connection.rollback()
            return -1
        finally:
            if cursor:
                cursor.close()

    # Recherche d'un abonné par son ID
    def find_abonne(self, id_abonne):
        sql = "SELECT * FROM abonne WHERE carteAbo = %s"
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
            print(f"Erreur lors de la recherche de l'abonné : {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    # Méthode pour transformer une ligne de résultats en un objet Abonne
    def set_all_values(self, rs):
        from entites.personne import Abonne
        try:
            abonne = Abonne(
                rs["carteAbo"], 
                rs["email"], 
                rs["mdp"], 
                rs["nom"], 
                rs["prenom"],
                rs["num_tel"], 
                rs["num_rue"], 
                rs["nom_rue"], 
                rs["num_cb"], 
                rs["ville"]
                )
            return abonne
        except KeyError as e:
            print(f"Erreur lors de la récupération des données : {e}")
            return None

    # Recherche d'abonnés en utilisant des critères
    def select_abonnes(self):
        try:
            resultats = self.db.query("SELECT * FROM abonne") 
            abonnes = []
            for row in resultats:
                try:
                    abonne = Abonne(
                        carteAbo=row['carteAbo'],
                        email=row['email'],
                        mdp=row['mdp'],
                        nom=row['nom'],
                        prenom=row['prenom'],
                        num_tel=row['num_tel'],
                        num_rue=row['num_rue'],
                        nom_rue=row['nom_rue'],
                        num_cb=row['num_cb'],
                        ville=row['ville']
                    )
                    abonnes.append(abonne)
                except KeyError as e:
                    print(f"Erreur lors de la récupération des données : {e}")
            return abonnes
        except Exception as e:
            print(f"Erreur lors de la récupération des abonnés : {e}")
            return []