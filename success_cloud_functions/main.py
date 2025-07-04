import requests
import json
from datetime import datetime

def slack_success_alert(request):
    try:
        dag_id = "warehouse_alert_system"
        execution_date = datetime.now()
        log_url = "https://localhost:8000"

        webhook_url = "https://hooks.slack.com/services/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"

        message = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"SUCCESS: ELT task complete"
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
                            "text": f"*Execution Time:*\n{execution_date}"
                        },
                    ]
                },
            ]
        }

        response = requests.post(webhook_url, json=message)
        print("Success alert sent")
        return f"Success alert sent"
    except Exception as e:
        print("Error sending the success alert to slack: "  + str(e))
        return f"Error: {str(e)}"


