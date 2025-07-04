def send_slack_alert(context_payload):
    # google cloud function URL
    function_url = "https://us-central1-alert-system-464222.cloudfunctions.net/send_slack_alert"

    # error information
    task_instance = context_payload.get("task_instance")
    dag_id = context_payload.get("dag").dag_id
    task_id = task_instance.task_id
    execution_date = context.get("execution_date")
    log_url = task_instance.log_url
    error = str(context.get("exception"))

    payload = {
        "task_id": "Data Freshness Alert",
        "dag_id": "Alert System Dag",
        "execution_date": str(),
        "error": error,
        "log_url": log_url
    }

    try:
        response = requests.post(gcf_url, json=payload)
        print(f"Slack Task Fail Alert sent:")
    except Exception as e:
        print(f"Slack Alert failed to send: {e}")