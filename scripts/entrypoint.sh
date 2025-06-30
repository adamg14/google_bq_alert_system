#!/usr/bin/env bash
set -euo pipefail

$(command -v pip) install --user -r requirements.txt

airflow db init

airflow db upgrade


if [ "$1" = "webserver" ] && ! airflow users list | grep -q admin; then
  airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.org \
    --password admin
fi


exec airflow "$@