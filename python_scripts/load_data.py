import os
import pandas as pd
from google.cloud import storage, bigquery

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../alert_credentials.json"


def load_data(bucket_name, source_file_path, destination_file_name):
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(destination_file_name)
    blob.upload_from_filename(source_file_path)

    print(f"File uploaded to Google Cloud Storage Bucket")


def bigquery_load(bucket_name, blob_name, dataset_id, table_id):
    big_query_client = bigquery.Client()

    # configure BigQuery Load Job
    load_job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )

    gcs_uri = f"gs://{bucket_name}/{blob_name}"

    table_ref = f"{big_query_client.project}.{dataset_id}.{table_id}"

    try:
        load_job = big_query_client.load_table_from_uri(
            source_uris=gcs_uri,
            destination=table_ref,
            job_config=load_job_config
        )

        print("Starting load job")
        load_job.result()

        destination_table = big_query_client.get_table(table_ref)
        print("Load job complete")
    except Exception as e:
        print(f"Error loading data into database table: {e}")



# process_data("../data/ecommerce_clickstream_transactions.csv")
load_data(
    "raw-ecommerce-data",
    "../data/ecommerce_clickstream_transactions.csv",
    "raw_data/ecommerce_clickstream_transactions.csv"
    )

bigquery_load(
    "raw-ecommerce-data",
    "raw_data/ecommerce_clickstream_transactions.csv",
    "raw_data",
    "ecommerce_clickstream"
    )