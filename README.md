# Google BigQuery Alert System
A serverless real-time alerting system for Google BigQuery that sends slack alerts using Google Cloud Functions using two types of alert methods: the result of data refresh/testing tasks within the Airflow DAG and queries to views within the Data Warehouse. 

## Google Cloud Functions
1. Authenticate yourself on the using the Google CLI
gcloud auth login
2. Deploying Cloud Functions to create a serverless function to send success/failure messages via Slack API

Terminal command for deploy Python Function to a Google Cloud Function
```bash gcloud functions deploy CLOUD_FUNCTION_NAME \
  --region=us-central1 \
  --runtime=python39 \
  --trigger-http \
  --allow-unauthenticated \
  --source=LOCAL_DIR \
  --entry-point=LOCAL_FUNCTION_NAME
```

Example of a Google cloud function deployment
```bash
gcloud functions deploy airflow-success-slack-alert \
  --region=us-central1 \
  --runtime=python39 \
  --trigger-http \
  --allow-unauthenticated \
  --source=success_cloud_functions \
  --entry-point=slack_success_alert
```


• This is an ELT pipeline - source data is loaded straight to BigQuery and transformed there

• Our main dbt pipelines run once every 2 hours

• Newly introduced errors into the modelling process WILL affect historical data

• We have access to GCP cloud resources but will want to keep costs down

• We use Slack and email to communicate internally

