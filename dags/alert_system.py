from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import requests
from airflow.operators.empty import EmptyOperator
from alert_query_freshness import query_data_freshness
from alert_query_volume import query_data_volume

gcf_url = "https://us-central1-alert-system-464222.cloudfunctions.net/send_slack_alert"
gcf_url_success = "https://us-central1-alert-system-464222.cloudfunctions.net/airflow-success-slack-alert"


def send_slack_success_alert():
    try:
        response = requests.post(gcf_url_success)
        response.raise_for_status()
        print(f"Success alert sent")
    except Exception as e:
        print(f"Success message failed to execute. Error: {str(e)}")


def send_slack_alert(context):
    try:
        task_instance = context['task_instance']
        dag_id = context['dag'].dag_id
        task_id = task_instance.task_id
        execution_date = context['execution_date'].isoformat()
        log_url = task_instance.log_url
        error = str(context.get('exception', 'Unknown error'))
        
        payload = {
            "task_id": task_id,
            "dag_id": dag_id,
            "execution_date": execution_date,
            "error": error,
            "log_url": "https://localhost:8080"
        }
        
        response = requests.post(gcf_url, json=payload)
        response.raise_for_status()
        print(f"Alert sent successfully: {response.status_code}")
    except Exception as e:
        print(f"Failed to send Slack alert: {str(e)}")


def send_slack_alert_sla(dag):
    try:
        execution_date = datetime.now()
        payload = {
            "error": "CRITICAL: SLA miss - Database has not been refreshed in 2 hours,",
            "dag_id": dag.dag_id,
            "task": "https://localhort",
            "log_url": "https://localhost:8080",

        }
    except Exception as e:
        print("Failed to send and alert for a missed SLA")


default_args = {
    "owner": "Adam Worede",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "on_failure_callback": send_slack_alert,
    # "on_success_callback": send_slack_alert_success,
    # dbt run should take two hours as that is the data ingestion time interval
    "sla": timedelta(hours=2)
}

with DAG(
    dag_id="warehouse_alert_system",
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2025, 6, 29),
    catchup=False,
    sla_miss_callback=send_slack_alert_sla
) as dag:
    dbt_staging_run = BashOperator(
        # purposely broke this to get an error 
        task_id="dbt_staging_run",
        bash_command="""
            cd /opt/airflow/dbt/ecommerce_data && \
            dbt deps && \
            dbt run --select models/staging --profiles-dir /opt/airflow/dbt/ecommerce_data
        """,
        trigger_rule="all_done",
        do_xcom_push=True,
    )

    dbt_staging_test = BashOperator(
        task_id="dbt_staging_test",
        bash_command="""
            cd /opt/airflow/dbt/ecommerce_data && \
            dbt deps && \
            dbt test --select models/staging --profiles-dir /opt/airflow/dbt/ecommerce_data
        """,
        do_xcom_push=True,
        dag=dag
    )

    dbt_mart_run = BashOperator(
        task_id="dbt_mart_run",
        bash_command="""
            cd /opt/airflow/dbt/ecommerce_data && \
            dbt deps && \
            dbt run --select models/mart --profiles-dir /opt/airflow/dbt/ecommerce_data
        """,
        do_xcom_push=True,
        dag=dag
    )

    dbt_mart_test = BashOperator(
        task_id = "dbt_mart_test",
        bash_command="""
            cd /opt/airflow/dbt/ecommerce_data && \
            dbt deps && \
            dbt test --select models/mart --profiles-dir /opt/airflow/dbt/ecommerce_data
        """,
        do_xcom_push=True,
        dag=dag
    )

    dbt_alert_freshness = PythonOperator(
        task_id = "dbt_alert_freshness",
        python_callable=query_data_freshness
    )

    dbt_alert_volume = PythonOperator(
        task_id = "dbt_alert_volume",
        python_callable=query_data_volume
    )

    success_slack_message = PythonOperator(
        task_id = "slack_success_alert",
        python_callable=send_slack_success_alert,
        trigger_rule="all_success"
    )


    dbt_staging_run >> dbt_staging_test
    dbt_staging_test >> dbt_mart_run >> dbt_mart_test
    dbt_staging_test >> dbt_alert_freshness >> dbt_alert_volume 
    dbt_alert_volume >> success_slack_message
    dbt_mart_test >> success_slack_message