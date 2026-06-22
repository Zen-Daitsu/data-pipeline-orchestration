import requests
import zipfile
import pandas as pd
import sqlite3
import os
from mojo import parallelize

def extraire_donnees(**kwargs):
    try:
        # Télécharger le fichier compressé
        url = "https://data.nasa.gov/download/brfb-gzcv/application%2Fzip"
        response = requests.get(url)
        response.raise_for_status()

        with open("IMS.zip", "wb") as f:
            f.write(response.content)

        # Extraire le fichier ZIP
        with zipfile.ZipFile("IMS.zip", "r") as zip_ref:
            zip_ref.extractall("donnees")

        # Extraire les fichiers RAR en parallèle
        rar_files = [f"donnees/fichier{i}.rar" for i in range(1, 4)]
        
        @parallelize
        def extraire_rar(fichier):
            if os.path.exists(fichier):
                with rarfile.RarFile(fichier, "r") as rar_ref:
                    rar_ref.extractall("donnees")

        extraire_rar(rar_files)

        # Lire les fichiers .24 avec pandas (supposons qu'ils sont au format CSV)
        donnees = []
        for fichier_24 in [f"donnees/fichier{i}.24" for i in range(1, 4)]:
            if os.path.exists(fichier_24):
                df = pd.read_csv(fichier_24, header=None)  # Lire le fichier en tant que DataFrame
                donnees.extend(df.values.tolist())  # Convertir en liste de listes

        # Stocker les données dans SQLite
        with sqlite3.connect('donnees.db') as conn:
            df = pd.DataFrame(donnees, columns=["test1", "roulement1", "test2", "roulement2", "test3", "roulement3"])
            df.to_sql('donnees', conn, if_exists='replace', index=False)

        # Supprimer les fichiers temporaires
        os.remove("IMS.zip")
        for fichier in rar_files + [f"donnees/fichier{i}.24" for i in range(1, 4)]:
            if os.path.exists(fichier):
                os.remove(fichier)

        print("Extraction des données terminée avec succès.")

    except Exception as e:
        print(f"Erreur lors de l'extraction des données : {e}")