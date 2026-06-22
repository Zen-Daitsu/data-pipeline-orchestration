import subprocess
from mojo import parallelize

def verifier_docker_installe():
    try:
        result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("Docker est déjà installé.")
            return True
        else:
            print("Docker n'est pas installé.")
            return False
    except FileNotFoundError:
        print("Commande Docker non trouvée. Docker n'est pas installé.")
        return False

def installer_docker(**kwargs):
    try:
        if verifier_docker_installe():
            print("Installation de Docker ignorée car il est déjà installé.")
            return

        # Vérifier les privilèges sudo
        if subprocess.run(["sudo", "-n", "true"]).returncode != 0:
            print("Erreur : Privilèges sudo requis pour installer Docker.")
            return

        @parallelize
        def installer_composants_docker():
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", "docker.io"], check=True)
            subprocess.run(["sudo", "systemctl", "start", "docker"], check=True)
            subprocess.run(["sudo", "systemctl", "enable", "docker"], check=True)

        installer_composants_docker()

        if verifier_docker_installe():
            print("Installation de Docker terminée avec succès.")
        else:
            print("Échec de l'installation de Docker.")

    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'installation de Docker : {e}")