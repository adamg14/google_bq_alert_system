# Google BigQuery Alert System
A serverless real-time alerting system for Google BigQuery that sends slack alerts using Google Cloud Functions using two types of alert methods: the result of data refresh/testing tasks within the Airflow DAG and queries to views within the Data Warehouse. 

## File Descriptions
### Cloud Function (`/cloud_functions/`)
### dags (`/dags/`)
This contains the initialisation of the Airflow Tasks, defining the orchastration required for the update, testing and alerting of the data warehouse.
### dbt (`/dbt/`)
Containes the schemas, inline tests and queries to create the tables and views within the DataWarehouse.
### postgres_data (`/postgres_data/`)
This is mounted to the Postgres databased defined in the docker file which contains metadata on the Airflow DAG such as results of previous runs.
### python_scripts (`/python_scripts/`)
Contains the data extraction scripts and functions to load the raw data into and then into the Google Big Query Data Warehouse.
### query_alert (`/query_alert/`)
### scripts (`/scripts/`)
### success_cloud_functions (`/success_cloud_functions/`)
### .env (`/.env`)
### Dockerfile (`/DockerFile`)
### docker-compose.yml (`/docker-compose.yml`)
### requirements.txt (`/requirements.txt`)
Contains the python modules and versions (to aviod compatibility issues) for the containers required for this project to be built.

## Running the Application 
1. Defining the Google Service Account Credentials. Create an `alert_credentials.json` is the root directory (This will be mounted to the containers to enable dbt and airflow access to your Google Cloud Bucket Storage and Google Big Query) and within the `/query_alert/` subdirectory which contains the a service accounts which has full rights to cloud storage and google big query within your Google Project. Update the `dbt/ecommerce_data/profiles.yml` for the correct project_id.
2. Create a Google Cloud Storage called 'raw-ecommerce-data', then Run the following python scrupt to upload the the raw data to the Google Cloud Storage bucket and then the Google Big Query Data Warehouse:
```bash
  python scripts/load_data.py
```
3. Running the docker-compose.yml file - ```bash
  docker-compose up --build
```
## Google Cloud Functions
1. Authenticate yourself on the using the Google CLI
gcloud auth login
2. Deploying Cloud Functions to create a serverless function to send success/failure messages via Slack API

Terminal command for deploy Python Function to a Google Cloud Function
```bash
gcloud functions deploy CLOUD_FUNCTION_NAME \
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

