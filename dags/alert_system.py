from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

SLACK_CONNECTION_ID = ""


# def slack_alert(context):
#     pass


# def handle_sla_miss(request):
#     data = request.json()

    # finish this function
default_args = {
    "owner": "Adam Worede",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    # "on_failure_callback": slack_alert,
    # dbt run should take two hours as that is the data ingestion time interval
    "sla": timedelta(hours=2)
}

with DAG(
    dag_id="warehouse_alert_system",
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2025, 6, 29),
    catchup=False,
    # sla_miss_callback=handle_sla_miss
) as dag:
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="""
            cd /opt/airflow/dbt/ecommerce_data && \
            dbt deps && \
            dbt run --profiles-dir /opt/airflow/dbt/ecommerce_data
        """,
        trigger_rule="all_done",
        do_xcom_push=True,
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="""
            cd /opt/airflow/dbt/ecommerce_data && \
            dbt deps && \
            dbt test --profiles-dir /opt/airflow/dbt/ecommerce_data
        """,
        do_xcom_push=True,
        dag=dag
    )


dbt_run >> dbt_test