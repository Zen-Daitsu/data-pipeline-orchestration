import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from mojo import parallelize

def visualiser_donnees(**kwargs):
    try:
        with sqlite3.connect('donnees.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM donnees')
            donnees = cursor.fetchall()

        @parallelize
        def traiter_donnees(data):
            return data[1]  # Extraire la deuxième colonne

        donnees_traitees = traiter_donnees(donnees)

        # Utiliser seaborn pour une visualisation avancée
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.lineplot(x=range(len(donnees_traitees)), y=donnees_traitees)
        plt.xlabel("Donnée")
        plt.ylabel("Valeur")
        plt.title("Visualisation des données")

        # Sauvegarder le graphique
        plt.savefig("visualisation.png")
        print("Visualisation des données terminée avec succès. Graphique sauvegardé sous 'visualisation.png'.")

    except Exception as e:
        print(f"Erreur lors de la visualisation des données : {e}")