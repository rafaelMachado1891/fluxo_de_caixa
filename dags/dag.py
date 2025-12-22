from airflow import DAG
from airflow.operators.python import PythonOperator
from include.pipeline_airflow import executar_pipeline
from datetime import datetime

with DAG(
    dag_id="fluxo_caixa_ingestao",
    start_date=datetime(2025, 12, 20),
    schedule="@daily",
    catchup=False
):

    carga = PythonOperator(
        task_id="carga_origem",
        python_callable=executar_pipeline
    )