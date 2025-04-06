from mysql.connector import Error
from DAO.DAOSession import DAOSession

class DAOVelo:
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOVelo.unique_instance is None:
            DAOVelo.unique_instance = DAOVelo()
        return DAOVelo.unique_instance

    # Insertion d'un vélo dans la BDD
    def insert_velo(self, un_velo):
        sql = "INSERT INTO velo (ref_velo, electrique, statut, date, km_parcourus, id_station) VALUES (%s, %s, %s, %s, %s, %s)"
        valeurs = (un_velo.get_ref_velo(), un_velo.get_electrique(), un_velo.get_statut(), un_velo.get_date(), un_velo.get_km_parcourus(), un_velo.get_station().get_id_station())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            cle = cursor.lastrowid
            return cle
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la création du vélo : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return -1
        finally:
            if cursor:
                cursor.close()

    # Suppression d'un vélo dans la BDD
    def delete_velo(self, un_velo):
        sql = "DELETE FROM velo WHERE ref_velo = %s"
        valeurs = (un_velo.get_ref_velo(),)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la suppression du vélo : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    # Recherche d'un vélo par sa référence
    def find_velo(self, ref_velo):
        sql = "SELECT * FROM velo WHERE ref_velo = %s"
        valeurs = (ref_velo,)
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
            print(f"Erreur lors de la recherche du vélo : {e}")
            print(sql)
            print(valeurs)
            return None
        finally:
            if cursor:
                cursor.close()

    # Mise à jour d'un vélo dans la BDD
    def update_velo(self, un_velo):
        sql = "UPDATE velo SET electrique = %s, statut = %s, date = %s, km_parcourus = %s, id_station = %s WHERE ref_velo = %s"
        valeurs = (un_velo.get_electrique(), un_velo.get_statut(), un_velo.get_date(), un_velo.get_km_parcourus(), un_velo.get_station().get_id_station(), un_velo.get_ref_velo())
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor()
            cursor.execute(sql, valeurs)
            return True
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la mise à jour du vélo : {e}")
            print(sql)
            print(valeurs)
            print("rollback")
            connection.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    # Recherche de vélos en utilisant des critères (ex: ref_velo, statut, km_parcourus, etc.)
    def select_velo(self, un_velo):
        les_velos = []
        sql = "SELECT * FROM velo WHERE "
        critere_ref_velo = un_velo.get_ref_velo()
        critere_statut = un_velo.get_statut()
        critere_electrique = un_velo.get_electrique()
        critere_km_parcourus = un_velo.get_km_parcourus()
        critere_station = un_velo.get_station()
        valeurs = []

        if critere_ref_velo is not None:
            sql += "ref_velo = %s"
            valeurs.append(critere_ref_velo)
        elif critere_statut is None and critere_electrique is None and critere_km_parcourus is None and critere_station is None:
            sql = "SELECT * FROM velo" 
        else:
            conditions = []
            if critere_statut is not None:
                conditions.append("statut = %s")
                valeurs.append(critere_statut)
            if critere_electrique is not None:
                conditions.append("electrique = %s")
                valeurs.append(critere_electrique)
            if critere_km_parcourus is not None:
                conditions.append("km_parcourus = %s")
                valeurs.append(critere_km_parcourus)
            if critere_station is not None:
                conditions.append("id_station = %s")
                valeurs.append(critere_station.get_id_station())  # Assuming the station object has get_id_station
            sql += " AND ".join(conditions)

        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, tuple(valeurs))
            rs = cursor.fetchall()
            for row in rs:
                les_velos.append(self.set_all_values(row))
        except Error as e:
            print("\n<--------------------------------------->")
            print(f"Erreur lors de la recherche de vélos : {e}")
            print(sql)
            print(valeurs)
        finally:
            if cursor:
                cursor.close()
        return les_velos

    # Méthode pour transformer une ligne de résultats en un objet Velo
    def set_all_values(self, rs):
        from entités.velo import Velo
        station = DAOSession.get_instance().find_station(rs["id_station"])  # Une méthode dans DAOSession
        un_velo = Velo(rs["ref_velo"], rs["electrique"], rs["statut"], rs["date"], rs["km_parcourus"], station)
        return un_velo
