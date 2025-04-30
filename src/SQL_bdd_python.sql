--Si une base existe déjà
DROP DATABASE IF EXISTS BDD_Python;

-- Création de la base
CREATE DATABASE IF NOT EXISTS BDD_Python;
USE BDD_Python;

-- Table Ville
CREATE TABLE IF NOT EXISTS Ville (
    idVille INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    nom VARCHAR(30) NOT NULL,
    code_postal INT NOT NULL,
    tarif_min_gratuite FLOAT NOT NULL,
    tarif_demi_occ FLOAT NOT NULL,
    tarif_demi_ann FLOAT NOT NULL
);

-- Table Reseau
CREATE TABLE IF NOT EXISTS Reseau (
    numRes INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    nom VARCHAR(30) NOT NULL,
    annee INT NOT NULL,
    idVille INT NOT NULL,
    FOREIGN KEY (idVille) REFERENCES Ville(idVille)
);

-- Table Station
CREATE TABLE IF NOT EXISTS Station (
    numStation INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    nom VARCHAR(30) NOT NULL,
    gps VARCHAR(15) NOT NULL,
    nom_rue VARCHAR(30) NOT NULL,
    num_rue INT NOT NULL,
    place_elec INT NOT NULL,
    place_non_elec INT NOT NULL,
    numRes INT NOT NULL,
    FOREIGN KEY (numRes) REFERENCES Reseau(numRes)
);

-- Table Velo
CREATE TABLE IF NOT EXISTS Velo (
    refVelo INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    electrique BOOLEAN NOT NULL,
    batterie INT,
    statut ENUM('Disponible', 'En circulation', 'En réparation', 'En panne', 'Perdu', 'Non disponible') NOT NULL,
    km_total INT NOT NULL,
    date_circu DATETIME NOT NULL,
    numStation INT NOT NULL,
    FOREIGN KEY (numStation) REFERENCES Station(numStation)
);

-- Table Abonne
CREATE TABLE IF NOT EXISTS Abonne (
    carteAbo INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    email VARCHAR(50) NOT NULL,
    mdp VARCHAR(30) NOT NULL,
    nom VARCHAR(30) NOT NULL,
    prenom VARCHAR(30) NOT NULL,
    num_tel BIGINT NOT NULL,
    num_rue INT NOT NULL,
    nom_rue VARCHAR(30) NOT NULL,
    num_cb VARCHAR(30)
);

-- Table Abonnement
CREATE TABLE IF NOT EXISTS Abonnement (
    idAbo INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    type_abo ENUM('Annuel', 'Occasionnel') NOT NULL,
    sous_type ENUM('1 jour', '2 jours', '3 jours', '4 jours', '5 jours', '6 jours', '7 jours', 'Classique', 'Réduit') NOT NULL
);

-- Table Contrat
CREATE TABLE IF NOT EXISTS Contrat (
    idCont INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    idAbo INT NOT NULL,
    carteAbo INT NOT NULL,
    date_debut DATE NOT NULL,
    date_fin DATE,
    montant FLOAT NOT NULL,
    garantie INT NOT NULL,
    carte_identite VARCHAR(30) NOT NULL,
    FOREIGN KEY (idAbo) REFERENCES Abonnement(idAbo),
    FOREIGN KEY (carteAbo) REFERENCES Abonne(carteAbo)
);

-- Table Trajet
CREATE TABLE IF NOT EXISTS Trajet (
    refTrajet INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    station_depart INT NOT NULL,
    station_arrivee INT NOT NULL,
    nbr_km INT NOT NULL,
    dateheure_debut DATETIME NOT NULL,
    dateheure_fin DATETIME NOT NULL,
    carteAbo INT NOT NULL,
    refVelo INT NOT NULL,
    FOREIGN KEY (station_depart) REFERENCES Station(numStation),
    FOREIGN KEY (station_arrivee) REFERENCES Station(numStation),
    FOREIGN KEY (carteAbo) REFERENCES Abonne(carteAbo),
    FOREIGN KEY (refVelo) REFERENCES Velo(refVelo)
);

-- Table Facturation
CREATE TABLE IF NOT EXISTS Facturation (
    idFacture INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    date DATE NOT NULL,
    montant FLOAT NOT NULL,
    carteAbo INT NOT NULL,
    FOREIGN KEY (carteAbo) REFERENCES Abonne(carteAbo)
);

-- Table Paiement
CREATE TABLE IF NOT EXISTS Paiement (
    idPaie INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    date DATE NOT NULL,
    montant FLOAT NOT NULL,
    idFacture INT NOT NULL,
    FOREIGN KEY (idFacture) REFERENCES Facturation(idFacture)
);

--Insertion des données dans les tables

INSERT INTO Ville (nom, code_postal, tarif_min_gratuite, tarif_demi_occ, tarif_demi_ann)
VALUES 
('Nancy', 54000, 15.0, 1.5, 1.0),
('Metz', 57000, 10.0, 1.2, 0.9),
('Strasbourg', 67000, 20.0, 2.0, 1.5),
('Toulouse', 31000, 18.0, 1.8, 1.3);

INSERT INTO Reseau (nom, annee, idVille)
VALUES 
('Reseau Nancy', 2022, 1),
('Reseau Metz', 2023, 2),
('Reseau Strasbourg', 2024, 3),
('Reseau Toulouse', 2025, 4);

INSERT INTO Station (nom, gps, nom_rue, num_rue, place_elec, place_non_elec, numRes)
VALUES 
('Gare Nancy', '48.6921,6.1844', 'Rue de la Gare', 12, 10, 20, 1),
('Place Stanislas', '48.6937,6.1834', 'Place Stanislas', 1, 8, 10, 1),
('Metz Centre', '49.1193,6.1757', 'Rue Serpenoise', 5, 12, 18, 2),
('Université Strasbourg', '48.5846,7.7507', 'Rue Blaise Pascal', 3, 15, 25, 3);

INSERT INTO Velo (electrique, batterie, statut, km_total, date_circu, numStation)
VALUES 
(TRUE, 90, 'Disponible', 1200, '2023-04-01 10:00:00', 1),
(FALSE, 0, 'Disponible', 300, '2023-05-10 08:00:00', 2),
(TRUE, 70, 'En circulation', 800, '2023-06-15 09:30:00', 3),
(FALSE, 0, 'En réparation', 1000, '2023-07-20 07:00:00', 4),
(TRUE, 40, 'Non disponible', 600, '2025-04-01 08:30:00', 1),
(TRUE, 90, 'Disponible', 1200, '2023-04-01 10:00:00', 1),
(FALSE, 0, 'Disponible', 300, '2023-05-10 08:00:00', 1),
(TRUE, 70, 'En circulation', 800, '2023-06-15 09:30:00', 1);

INSERT INTO Abonne (email, mdp, nom, prenom, num_tel, num_rue, nom_rue, num_cb)
VALUES 
('alice@example.com', 'mdphash1', 'Dupont', 'Alice', 1234567890, 5, 'Victor Hugo', '1234567812345678'),
('bob@example.com', 'mdphash2', 'Martin', 'Bob', 9876543210, 10, 'Jean Jaurès', '8765432187654321'),
('carla@example.com', 'mdphash3', 'Lemoine', 'Carla', 1122334455, 7, 'Pasteur', '1122334411223344'),
('david@example.com', 'mdphash4', 'Petit', 'David', 5566778899, 9, 'Lafayette', '4433221144332211');

INSERT INTO Abonnement (type_abo, sous_type)
VALUES 
('Annuel', 'Classique'),
('Occasionnel', '4 jours'),
('Occasionnel', '2 jours'),
('Annuel', 'Réduit');

INSERT INTO Contrat (idAbo, carteAbo, date_debut, date_fin, montant, garantie, carte_identite)
VALUES 
(1, 1, '2024-01-01', '2025-01-01', 120.0, 100, 'ID12345'),
(2, 2, '2025-04-01', '2025-04-05', 20.0, 0, 'ID67890'),
(3, 3, '2025-05-01', '2025-05-03', 10.0, 0, 'ID99887'),
(4, 4, '2024-09-01', '2025-09-01', 100.0, 80, 'ID55667');

INSERT INTO Trajet (station_depart, station_arrive, nbr_km, dateheure_debut, dateheure_fin, carteAbo, refVelo)
VALUES 
(1, 2, 2, '2025-04-02 09:00:00', '2025-04-02 09:20:00', 1, 1),
(2, 1, 3, '2025-04-03 14:00:00', '2025-04-03 14:25:00', 2, 2),
(3, 4, 4, '2025-04-04 16:00:00', '2025-04-04 16:35:00', 3, 3),
(4, 1, 5, '2025-04-05 11:00:00', '2025-04-05 11:40:00', 4, 4);

INSERT INTO Facturation (date, montant, carteAbo)
VALUES 
('2025-04-05', 3.0, 1),
('2025-04-06', 4.5, 2),
('2025-04-07', 5.0, 3),
('2025-04-08', 6.0, 4);

INSERT INTO Paiement (date, montant, idFacture)
VALUES 
('2025-04-06', 3.0, 1),
('2025-04-07', 4.5, 2),
('2025-04-08', 5.0, 3),
('2025-04-09', 6.0, 4);