from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from include.pipeline_airflow import executar_pipeline
from datetime import datetime

@dag(
    dag_id = "dag_executar_pipeline",
    description = "dag que executa minha pipeline de extração de dados do  banco de dados",
    schedule = "@daily",
    start_date = datetime(2025,12,21),
    catchup = False,
    tags=["fluxo_caixa", "dbt"]

)
def dag_executar_pipeline():

    @task
    def task_executar_pipeline():
        executar_pipeline()

    task_dbt_run = BashOperator(
        task_id = "dbt_run",
        bash_command = """
        cd /usr/local/airflow/dw_fluxo_caixa 
        """
    )


    task_executar_pipeline() >> task_dbt_run
    

dag_executar_pipeline()

