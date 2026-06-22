from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
import logging

# Import tasks from the tasks folder
from tasks.installer_docker import installer_docker
from tasks.installer_kafka import installer_kafka
from tasks.extraire_donnees import extraire_donnees
from tasks.configurer_kafka import configurer_kafka
from tasks.visualiser_donnees import visualiser_donnees

# Configurer le logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

default_args = {
    'owner': 'amink',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'A53_projet',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    catchup=False,
)

with dag:
    t1 = PythonOperator(task_id="installer_docker", python_callable=installer_docker)
    t2 = PythonOperator(task_id="installer_kafka", python_callable=installer_kafka)
    t3 = PythonOperator(task_id="extraire_donnees", python_callable=extraire_donnees)
    t4 = PythonOperator(task_id="configurer_kafka", python_callable=configurer_kafka)
    t5 = PythonOperator(task_id="visualiser_donnees", python_callable=visualiser_donnees)

    # Définir l'ordre des tâches
    t1 >> t2 >> t3 >> t4 >> t5

    # Logging pour le début et la fin du DAG
    logger.info("DAG 'A53_projet' configuré avec succès.")