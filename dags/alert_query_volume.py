import requests
from datetime import datetime

gcf_url = "https://us-central1-alert-system-464222.cloudfunctions.net/send_slack_alert"


def query_data_volume():
    url = "https://us-central1-alert-system-464222.cloudfunctions.net/query_alert_volume"

    try:
        response = requests.post(url)

        data = response.json()

        if not data:
            print("Query returned no results")
        else:
            row = data[0]

            warning = row["volume_alert"]
            day = row["day"]
            error_message = f"{ warning }: { day }."

            payload = {
                "task_id": "Data Volume Query",
                "dag_id": "warehouse_alert_system",
                "execution_date": str(datetime.now()),
                "error": error_message,
                "log_url": "https://localhost:8080"
            }

            response = requests.post(gcf_url, json=payload)

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")


# query_data_volume()