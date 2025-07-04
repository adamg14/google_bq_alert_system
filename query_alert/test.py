import requests

url =  "https://us-central1-alert-system-464222.cloudfunctions.net/query_alert_volume"
url = "https://us-central1-alert-system-464222.cloudfunctions.net/query_alert_freshness"
payload = {
    "message": "Test alert from Python client"
}
response = requests.post(url, json=payload)

print("response" + response.text)
