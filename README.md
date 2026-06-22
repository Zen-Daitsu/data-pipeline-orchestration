# NASA Industrial Data Pipeline & Streaming Architecture

An Apache Airflow DAG orchestrating infrastructure provisioning, parallel data extraction, relational warehouse population, and throughput Apache Kafka streaming event serialization.

## 1. Architectural Overview
The pipeline executes a synchronous 5-stage orchestration graph running on a daily interval:

1. **Provisioning Engine:** Detects, installs, and validates native system services for local Docker environments.

2. **Streaming Stack Deployment:** Automated system configuration of Apache Kafka infrastructure.

3. **Parallel Ingestion & ETL:** Fetches compressed telemetry archives directly via HTTP from public NASA repositories, unzips sources, and leverages multi-threaded parallel extraction routines to process and map sequential block records to a structured SQLite destination.

4. **Kafka Message Streaming:** Batches historical records out of database tables, applies internal GZIP serialization, and dispatches payloads onto active Kafka message queues.

5. **Analytical Visualization:** Pulls dataset samples to render multi-variable lines and data trends utilizing advanced Seaborn styling pipelines.

## 2. Engineering Highlights & Trade-offs
* **Modular Task Optimization:** Isolated individual execution scripts out of the main execution graph to enforce strict maintainability and code clarity.
* **Optimized Data Flow Throughput:** Leveraged customized batching structures (`batch_size = 100`) coupled with parallelized routines to handle large-scale database operations and prevent message-queue saturation.
* **Network & Storage Rigor:** Implemented explicit resource cleanup protocols across execution tasks (`os.remove()`) to minimize storage bloat during continuous system runtime.

## 3. Technical Stack
* **Orchestration:** Apache Airflow
* **Core Language:** Python
* **Data Processing & Analytics:** Pandas, SQLite3, Matplotlib, Seaborn
* **Event Streaming:** Apache Kafka, Kafka-Python
* **Parallel Utilities:** Mojo-backed optimization wrappers
* **Infrastructure Target:** Ubuntu Linux system services (Apt-get package configurations)

## 4. Local Deployment & Setup

### Prerequisites
Ensure your local Linux machine has system administration access (`sudo` capabilities verified).

### Installation
1. Clone the project locally:
   ```bash
   git clone git@https://github.com/Zen-Daitsu/data-pipeline-orchestration
   cd nasa-data-pipeline-orchestration