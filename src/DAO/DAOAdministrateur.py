from mysql.connector import Error
from DAO.DAOSession import DAOSession
from DAO.DAOPersonne import DAOPersonne
from entités.administrateur import Administrateur

class DAOAdministrateur:
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOAdministrateur.unique_instance is None:
            DAOAdministrateur.unique_instance = DAOAdministrateur()
        return DAOAdministrateur.unique_instance

    # Insertion d'un administrateur dans la BDD
    def insert_administrateur(self, un_admin):
        # Insérer dans la table personne via DAOPersonne
        dao_personne = DAOPersonne.get_instance()
        id_personne = dao_personne.insert_personne(un_admin)
        if id_personne == -1:
            return -1

        # Insérer dans administrateur
        sql = "INSERT INTO administrateur (id_personne) VALUES (%s)"
        valeurs = (id_personne,)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return id_personne
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création de l'administrateur : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return -1
        finally:
            if cursor:
                cursor.close()
    
    # Suppression d'un administrateur de la BDD
    def delete_administrateur(self, un_admin):
        sql = "DELETE FROM administrateur WHERE id_personne = %s"
        valeurs = (un_admin.get_id_personne(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            # Supprimer la personne associée
            dao_personne = DAOPersonne.get_instance()
            return dao_personne.delete_personne(un_admin)
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la suppression de l'administrateur : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()
    
    # Recherche d'un administrateur par son ID
    def find_administrateur(self, id_personne):
        sql = "SELECT * FROM administrateur WHERE id_personne = %s"
        valeurs = (id_personne,)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, valeurs)
            rs = cursor.fetchone()
            if rs:
                dao_personne = DAOPersonne.get_instance()
                personne = dao_personne.find_personne(id_personne)
                return self.set_all_values(personne)
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
        dao_personne = DAOPersonne.get_instance()
        return dao_personne.update_personne(un_admin)

    # Recherche d'administrateur en utilisant des critères
    def select_administrateur(self, un_admin):
        les_admins = []
        sql = "SELECT p.* FROM personne p JOIN administrateur a ON p.id_personne = a.id_personne WHERE "
        critere_id = un_admin.get_id_personne()
        critere_nom = un_admin.get_nom()
        critere_prenom = un_admin.get_prenom()
        critere_email = un_admin.get_email()
        valeurs = []

        if critere_id is not None:
            sql += "p.id_personne = %s"
            valeurs.append(critere_id)
        elif critere_nom is None and critere_prenom is None and critere_email is None:
            sql = "SELECT p.* FROM personne p JOIN administrateur a ON p.id_personne = a.id_personne"
        else:
            conditions = []
            if critere_nom is not None:
                conditions.append("p.nom = %s")
                valeurs.append(critere_nom)
            if critere_prenom is not None:
                conditions.append("p.prenom = %s")
                valeurs.append(critere_prenom)
            if critere_email is not None:
                conditions.append("p.email = %s")
                valeurs.append(critere_email)
            sql += " AND ".join(conditions)

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, tuple(valeurs))
            rs = cursor.fetchall()
            for row in rs:
                from entités.administrateur import Administrateur
                admin = Administrateur(
                    id_personne=row["id_personne"],
                    email=row["email"],
                    mot_de_passe=row["mot_de_passe"],
                    nom=row["nom"],
                    prenom=row["prenom"]
                )
                les_admins.append(admin)
        except Error as e:
            print(f"Erreur lors de la recherche d'administrateurs : {e}")
            print(sql)
            print(valeurs)
        finally:
            if cursor:
                cursor.close()
        return les_admins
    
    # Méthode pour transformer une ligne de résultats (rs) en un objet Administrateur
    def set_all_values(self, personne):
        return Administrateur(
            id_personne=personne.get_id_personne(),
            email=personne.get_email(),
            mot_de_passe=personne.get_mot_de_passe(),
            nom=personne.get_nom(),
            prenom=personne.get_prenom()
        )
