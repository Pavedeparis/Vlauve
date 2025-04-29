from mysql.connector import Error
from DAO.DAOSession import DAOSession
from entites.velo import Velo, StatutVelo

class DAOVelo:
    unique_instance = None

    @staticmethod
    def get_instance():
        if DAOVelo.unique_instance is None:
            DAOVelo.unique_instance = DAOVelo()
        return DAOVelo.unique_instance

    # Insertion d'un vélo dans la BDD
    def insert_velo(self, un_velo):
        sql = "INSERT INTO velo (refVelo, electrique, batterie, statut, km_total, date_circu, numStation) VALUES (%s, %s, %s, %s, %s, %s)"
        valeurs = (un_velo.get_refVelo(), un_velo.get_electrique(), un_velo.get_batterie(), un_velo.get_statut(), un_velo.get_km_total(), un_velo.get_date_circu(), un_velo.get_station().get_numStation())
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
        sql = "DELETE FROM velo WHERE refVelo = %s"
        valeurs = (un_velo.get_refVelo(),)
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
    def find_velo(self, refVelo):
        sql = "SELECT * FROM velo WHERE refVelo = %s"
        valeurs = (refVelo,)
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
    
    def find_velos_by_station(self, numStation):
        connection = DAOSession.get_connexion()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM velo WHERE numStation = %s", (numStation,))

        velos = []
        for row in cursor.fetchall():
            velo = Velo(
                refVelo=row['refVelo'],
                electrique=bool(row['electrique']),
                batterie=row['batterie'],
                statut=StatutVelo(row['statut']),
                km_total=row['km_total'],
                date_circu=row['date_circu'],
                numStation=row['numStation']
            )
            velos.append(velo)
        return velos

    # Mise à jour d'un vélo dans la BDD
    def update_velo(self, un_velo):
        sql = "UPDATE velo SET electrique = %s, batterie = %s, statut = %s, km_total = %s, date_circu = %s, numStation = %s WHERE refVelo = %s"
        valeurs = (un_velo.get_electrique(), un_velo.get_batterie(), un_velo.get_statut(), un_velo.get_km_total(), un_velo.get_date_circu(), un_velo.get_station().get_numStation(), un_velo.get_refVelo())
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

    # Recherche de vélos en utilisant des critères 
    def select_velo(self, un_velo):
        les_velos = []
        sql = "SELECT * FROM velo WHERE "
        critere_refVelo = un_velo.get_refVelo()
        critere_batterie = un_velo.get_batterie(),
        critere_statut = un_velo.get_statut()
        critere_electrique = un_velo.get_electrique()
        critere_date_circu = un_velo.get_date_circu()
        critere_station = un_velo.get_station()
        valeurs = []

        if critere_refVelo is not None:
            sql += "refVelo = %s"
            valeurs.append(critere_refVelo)
        elif critere_statut is None and critere_electrique is None and critere_date_circu is None and critere_station is None:
            sql = "SELECT * FROM velo" 
        else:
            conditions = []
            if critere_batterie is not None:
                conditions.append("batterie = %s")
                valeurs.append(critere_batterie)
            if critere_statut is not None:
                conditions.append("statut = %s")
                valeurs.append(critere_statut)
            if critere_electrique is not None:
                conditions.append("electrique = %s")
                valeurs.append(critere_electrique)
            if critere_date_circu is not None:
                conditions.append("date_circu = %s")
                valeurs.append(critere_date_circu)
            if critere_station is not None:
                conditions.append("numStation = %s")
                valeurs.append(critere_station.get_numStation()) 
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
        from entites.velo import Velo
        from DAO.DAOStation import DAOStation
        station = DAOStation.get_instance().find_station(rs["numStation"]) 
        un_velo = Velo(
            refVelo=rs["refVelo"],
            electrique=bool(rs["electrique"]),
            batterie=rs["batterie"],
            statut=StatutVelo(rs["statut"]),
            date_circu=rs["date_circu"],
            km_total=rs["km_total"],
            numStation=rs["numStation"]
        )

        return un_velo

    def verifier_disponibilite(self, refVelo):
        sql = "SELECT statut FROM velo WHERE refVelo = %s"
        valeurs = (refVelo,)
        try:
            connection = DAOSession.get_connexion()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(sql, valeurs)
            rs = cursor.fetchone()
            if rs:
                return rs["statut"] == "disponible"
            return False
        except Error as e:
            print(f"Erreur lors de la vérification de la disponibilité du vélo : {e}")
            return False
        finally:
            if cursor:
                cursor.close()