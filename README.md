# Google BigQuery Alert System
A serverless real-time alerting system for Google BigQuery that sends slack alerts using Google Cloud Functions using two types of alert methods: the result of data refresh/testing tasks within the Airflow DAG and queries to views within the Data Warehouse. 

## Project Details
- Sends two type of alerts error (failed Data refresh/test tasks) and warnings (based on irregularities within data)
- Code completely containerised using Docker for CI/CD good practice
- Uses Google Cloud Functions to send notifications to slack using Slack API

## Possible improvements to this project
- Seperate warning and error notification message formats.
- Deployment of the Airflow DAG to the cloud, via either:
    - Deployment of the containers via Kubernetes
    - Deployment of the DAG directly using Astronomer 
- More enhanced testing functionality e.g. focusing on edgecases where issues within the datawarehouse can be disputed as a warning/error

## File Descriptions

### Cloud Function (`/cloud_functions/`)

#### (`/cloud_functions/main.py`)
The python function within this file triggers the Google Cloud Function to send an error notification to slack, this function is triggered anytime there is an error in the DAG which prevents either the load, testing or warning notification within the data warehouse. 
#### (`/cloud_functions/requirements.txt`)
Contains the python packages required to carry out the Google Cloud Function.

### dags (`/dags/`)
This contains the initialisation of the Airflow Tasks, defining the orchastration required for the update, testing and alerting of the data warehouse.
#### (`/dags/alert_query_freshness.py`)
This file contains a python function that triggers the Google Cloud function to send a notification to slack when there is an issue with the freshness of data within the data warehouse (the newest record is more than 3 hours old).
#### (`/dags/alert_data_volume.py`)
Contains a python function that trigged a Google Cloud Function to send a slack notification if a view is queried highlighting an irregularity in the volume.
#### (`/dags/alert_system.py`)
Contains the definition of the tasks within the DAG and the order of the events.
### (`/dags/slack_function.py`)
Function that triggers the slack notification via the GCF for a task failure within the DAG

### dbt (`/dbt/ecommerce_data/`)
Containes the schemas, inline tests and queries to create the tables and views within the DataWarehouse.
#### (`/dbt/ecommerce_data/models/alerts/`)
Contains the schema definition and the inline tests for the alert views to be queried to identify irregularities within the data in the datawarehouse.
#### (`/dbt/ecommerce_data/models/mart/`)
Contains the schema definition and the inline tests for the data mart which includes advanced analytics such as cohort analysis.
#### (`/dbt/ecommerce_data/models/staging/`)
Contains the schema defintion and the inline tests for the staging which includes transformations from the raw data table directly loaded from the data within the google cloud storage bucket.
#### (`/dbt/ecommerce_data/models/sources.yml`)
Connection to the raw data table referencing the google cloud storage bucket
#### (`/dbt/ecommerce_data/dbt_project.yml)
Contains conceptual design information on the google big query data warehouse
#### (`/dbt/ecommerce_data/profiles.yml`)
Uses a Google Service Account to connect to the Google Big Query 

### postgres_data (`/postgres_data/`)
This is mounted to the Postgres databased defined in the docker file which contains metadata on the Airflow DAG such as results of previous runs.

### python_scripts (`/python_scripts/`)
Contains the data extraction scripts and functions to load the raw data into and then into the Google Big Query Data Warehouse.

### query_alert (`/query_alert/`)
Contains the a function that queries the database view which detects unusual data patterns, that is deployed to the google cloud

### success_cloud_functions (`/success_cloud_functions/`)
The google cloud function that send a slack success message when all the tasks within the DAG are ran successfully.

### .env (`/.env`)
Environment variables that define the google cloud project id PROJECT_ID and the IAM service account IAM.

### Dockerfile (`/DockerFile`)
Contains the definition of the python environment, along with the commands to install all the required dependencies to create the containers that initialises Airflow, runs the Airflow webserver UI and the scheduler that handles the runnning of Airflow DAG tasks.

### docker-compose.yml (`/docker-compose.yml`)
Contains the definition of all the containers needed to run this project:
- Postgres DB
- Airflow initialiser
- Airflow webserver
- Airflow scheduler

### requirements.txt (`/requirements.txt`)
Contains the python modules and versions (to aviod compatibility issues) for the containers required for this project to be built.


## Running the Application 
1. Defining the Google Service Account Credentials. Create an `alert_credentials.json` is the root directory (This will be mounted to the containers to enable dbt and airflow access to your Google Cloud Bucket Storage and Google Big Query) and within the `/query_alert/` subdirectory which contains the a service accounts which has full rights to cloud storage and google big query within your Google Project. Update the `dbt/ecommerce_data/profiles.yml` for the correct project_id.
2. Create a Google Cloud Storage called 'raw-ecommerce-data', then Run the following python scrupt to upload the the raw data to the Google Cloud Storage bucket and then the Google Big Query Data Warehouse:
```bash
  python scripts/load_data.py
```
3. Running the docker-compose.yml file -
4.
```bash
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

### Project Specification
• This is an ELT pipeline - source data is loaded straight to BigQuery and transformed there

• Our main dbt pipelines run once every 2 hours

• Newly introduced errors into the modelling process WILL affect historical data

• We have access to GCP cloud resources but will want to keep costs down

• We use Slack and email to communicate internally
