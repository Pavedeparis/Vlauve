import tkinter as tk
from interfaces.app_controller import AppController
from DAO.DAOAbonne import DAOAbonne
from DAO.DAOAdministrateur import DAOAdministrateur

def centrer_fenetre(fenetre, largeur, hauteur):
    # Obtenir la taille de l'écran
    ecran_largeur = fenetre.winfo_screenwidth()
    ecran_hauteur = fenetre.winfo_screenheight()

    # Calculer la position x et y pour centrer
    x = (ecran_largeur - largeur) // 2
    y = (ecran_hauteur - hauteur) // 2

    # Appliquer la taille et la position
    fenetre.geometry(f"{largeur}x{hauteur}+{x}+{y}")

if __name__ == "__main__":
    # Récupérer les utilisateurs depuis la base de données
    abonnés = DAOAbonne.get_instance().select_abonnes()
    administrateurs = DAOAdministrateur.get_instance().select_administrateurs()
    utilisateurs = abonnés + administrateurs

    # Création de la fenêtre principale
    root = tk.Tk()
    root.title("VLauve")
    centrer_fenetre(root, 600, 600)

    # Passer la liste des utilisateurs à AppController
    app = AppController(root, utilisateurs)
    
    # Lancer l'application
    root.mainloop()
