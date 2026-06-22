import kafka
import sqlite3
import json
from mojo import parallelize

def configurer_kafka(**kwargs):
    try:
        # Configurer le producteur Kafka avec compression
        producer = kafka.KafkaProducer(
            bootstrap_servers=["localhost:9092"],
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            compression_type='gzip'  # Compression des messages
        )

        # Récupérer les données de la base de données
        with sqlite3.connect('donnees.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM donnees')
            donnees = cursor.fetchall()

        # Envoyer les données par lots (batch)
        batch_size = 100  # Taille du lot
        for i in range(0, len(donnees), batch_size):
            batch = donnees[i:i + batch_size]
            @parallelize
            def envoyer_batch(batch):
                for donnee in batch:
                    producer.send("donnees", value=donnee)
            envoyer_batch(batch)

        producer.flush()  # S'assurer que tous les messages sont envoyés
        print("Configuration de Kafka terminée avec succès.")

    except kafka.errors.KafkaError as e:
        print(f"Erreur Kafka lors de l'envoi des données : {e}")
    except Exception as e:
        print(f"Erreur générale lors de la configuration de Kafka : {e}")