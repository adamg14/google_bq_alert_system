from google.cloud import bigquery
from google.oauth2 import service_account
import pandas
import pandas_gbq
from flask import jsonify

def query_alert_volume(request):
    project_id = "alert-system-464222"
    dataset_id = "alert_system_alerts"
    view_name = "alert_volume"
    view = f"{project_id}.{dataset_id}.{view_name}"
    query = f"SELECT * FROM `{view}`"

    try:
        df = pandas_gbq.read_gbq(query, project_id=project_id)
        return jsonify(df.to_dict(orient="records"))

    except Exception as e:
        print(f"Error querying database view: {str(e)}")
        return f"Error querying database view: {str(e)}", 500


def query_alert_freshness(request):
    project_id = "alert-system-464222"
    dataset_id = "alert_system_alerts"
    view_name = "alert_data_freshness"
    view = f"{project_id}.{dataset_id}.{view_name}"
    query = f"SELECT * FROM `{view}`"

    try:
        df = pandas_gbq.read_gbq(query, project_id=project_id)
        return jsonify(df.to_dict(orient="records"))

    except Exception as e:
        print(f"Error querying database view: {str(e)}")
        return f"Error querying database view: {str(e)}", 500
