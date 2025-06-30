FROM apache/airflow:2.6.0-python3.9

COPY ./requirements.txt ./requirements.txt


RUN pip install --default-timeout=200 --no-cache-dir -r ./requirements.txt