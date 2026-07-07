from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from etl.extract import extract_tariffs, extract_freight_rates, extract_disruptions
from etl.transform import clean_tariffs, clean_freight_rates, clean_disruptions
from etl.load import load_tariffs, load_freight_rates, load_disruptions

default_args = {"owner": "borderiq", "retries": 2, "retry_delay": timedelta(minutes=10)}


def run_tariffs_pipeline():
    load_tariffs(clean_tariffs(extract_tariffs()))


def run_freight_pipeline():
    load_freight_rates(clean_freight_rates(extract_freight_rates()))


def run_disruptions_pipeline():
    load_disruptions(clean_disruptions(extract_disruptions()))


with DAG(
    dag_id="borderiq_pipeline",
    default_args=default_args,
    description="Daily ingestion of East African trade corridor data",
    schedule_interval="@daily",
    start_date=datetime(2026, 7, 6),
    catchup=False,
    tags=["borderiq", "trade-data"],
) as dag:
    tariffs_task = PythonOperator(task_id="ingest_tariffs", python_callable=run_tariffs_pipeline)
    freight_task = PythonOperator(task_id="ingest_freight_rates", python_callable=run_freight_pipeline)
    disruptions_task = PythonOperator(task_id="ingest_disruptions", python_callable=run_disruptions_pipeline)

    [tariffs_task, freight_task, disruptions_task]
