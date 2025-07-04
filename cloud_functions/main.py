import requests
import json

def send_slack_alert(request):
    try:
        data = request.get_json()
        task_id = data.get('task_id', 'Unknown task')
        dag_id = data.get('dag_id', 'Unknown DAG')
        execution_date = data.get('execution_date', 'Unknown time')
        error = data.get('error', 'No error details')
        log_url = data.get('log_url', '')

        webhook_url = "https://hooks.slack.com/services/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"
        message = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"CRITICAL ERROR: ELT task failed"
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*DAG:*\n{dag_id}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Task:*\n{task_id}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Execution Time:*\n{execution_date}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Error:*\n```{error}```"
                        }
                    ]
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "View Logs",
                                "emoji": True
                            },
                            "url": log_url
                        }
                    ]
                }
            ]
        }
        
        response = requests.post(webhook_url, json=message)
        print("Alert sent")
        return f"Alert sent: {response.status_code}", 200
    except Exception as e:
        print("Error")
        return f"Error: {str(e)}", 500



result, status = send_slack_alert({
    "task_id": "example_task",
    "dag_id": "example_dag",
    "execution_date": "2025-07-01T00:00:00",
    "error": "Example error message",
    "log_url": "http://example.com/logs"
})
print(result, status)