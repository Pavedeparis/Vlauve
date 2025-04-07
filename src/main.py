# interface de l'accueil

from src.DAO.DAOAbonne import DAOAbonne
from src.entités.abonne import Abonne

# === FONCTIONS D’ACTION POUR CHAQUE ENTITÉ === #

def afficher_abonnes():
    dao = DAOAbonne.get_instance()
    Abonnes = dao.select_abonne(Abonne(None, None, None, None))
    for p in Abonnes:
        print(vars(p))  # Affiche l'objet en dict pour lisibilité

def ajouter_abonne():
    nom = input("Nom : ")
    adresse = input("Adresse : ")
    region = input("Région : ")
    p = Abonne(None, nom, adresse, region)
    id_insert = DAOAbonne.get_instance().insert_abonne(p)
    print("Ajouté avec ID :", id_insert)

def modifier_abonne():
    id_prod = input("ID à modifier : ")
    nom = input("Nouveau nom : ")
    adresse = input("Nouvelle adresse : ")
    region = input("Nouvelle région : ")
    p = Abonne(int(id_prod), nom, adresse, region)
    DAOAbonne.get_instance().update_abonne(p)
    print("Abonne mis à jour.")

def supprimer_abonne():
    id_prod = input("ID à supprimer : ")
    p = Abonne(int(id_prod), None, None, None)
    DAOAbonne.get_instance().delete_abonne(p)
    print("Abonne supprimé.")

# === DICTIONNAIRE DE MENU PAR ENTITÉ === #

menus = {
    "Abonne": {
        "actions": {
            "1": ("Afficher tous", afficher_abonnes),
            "2": ("Ajouter", ajouter_abonne),
            "3": ("Modifier", modifier_abonne),
            "4": ("Supprimer", supprimer_abonne)
        }
    }
    # Tu peux rajouter ici les blocs pour Velo, Abonne, Trajet, etc.
}

# === FONCTION GÉNÉRIQUE POUR MENU PAR ENTITÉ === #

def menu_entite(nom_entite, actions_dict):
    while True:
        print(f"\n--- Menu {nom_entite} ---")
        for key, (desc, _) in actions_dict.items():
            print(f"{key}. {desc}")
        print("0. Retour menu principal")
        
        choix = input("Ton choix : ")
        if choix == "0":
            break
        elif choix in actions_dict:
            actions_dict[choix][1]()  # Appelle la fonction liée
        else:
            print("Choix invalide.")

# === MENU PRINCIPAL === #

def main_menu():
    while True:
        print("\n=== MENU PRINCIPAL ===")
        for i, nom in enumerate(menus.keys(), start=1):
            print(f"{i}. Gestion des {nom}s")
        print("0. Quitter")

        choix = input("Ton choix : ")
        if choix == "0":
            print("Fermeture du programme.")
            break
        elif choix in [str(i) for i in range(1, len(menus)+1)]:
            nom_entite = list(menus.keys())[int(choix) - 1]
            menu_entite(nom_entite, menus[nom_entite]["actions"])
        else:
            print("Choix invalide.")

# === LANCEMENT ===

if __name__ == "__main__":
    main_menu()
