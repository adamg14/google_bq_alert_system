import requests

url = "https://us-central1-alert-system-464222.cloudfunctions.net/airflow-success-slack-alert"
response = requests.post(url)
print(response.status_code)
print(response.text)