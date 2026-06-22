import subprocess
from mojo import parallelize  # Utilitaire de parallélisation de Mojo

def installer_kafka(**kwargs):
    try:
        # Installer Kafka en utilisant la parallélisation de Mojo
        @parallelize
        def installer_composants_kafka():
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", "kafka"], check=True)
            subprocess.run(["sudo", "systemctl", "start", "kafka"], check=True)
            subprocess.run(["sudo", "systemctl", "enable", "kafka"], check=True)

        installer_composants_kafka()

        print("Installation de Kafka terminée avec succès.")

    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'installation de Kafka : {e}")