import requests
from datetime import datetime

gcf_url = "https://us-central1-alert-system-464222.cloudfunctions.net/send_slack_alert"

def query_data_freshness():

    url = "https://us-central1-alert-system-464222.cloudfunctions.net/query_alert_freshness"

    try:
        response = requests.post(url)
        
        data = response.json()
        
        if not data:
            print("Query returned no results")
        else:
            row = data[0]

            freshness = row["freshness"]
            last_update = row["last_update"]
            latest_data_load = row["latest_data_load"]

            error_message = f"{ freshness }. There has been { last_update } hours since the last update. The last update was on: { latest_data_load }."
            payload = {
            "task_id": "Data Freshness Query",
            "dag_id": "warehouse_alert_system",
            "execution_date": str(datetime.now()),
            "error":error_message,
            "log_url": "https://localhost:8080"
        }

        response = requests.post(gcf_url, json=payload)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

# query_data_freshness()
