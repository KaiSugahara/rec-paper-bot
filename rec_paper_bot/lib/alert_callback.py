import os

import requests

from airflow.sdk.definitions.context import Context


def on_success_callback(context: Context):
    dag_id = context["dag"].dag_id
    run_id = context["run_id"]
    requests.post(
        os.environ.get("AIRFLOW_SLACK_WEBHOOK_URL_SUCCESS"),
        json={
            "text": "The DAG `{dag_id}` succeeded ( run_id: `{run_id}` )".format(
                dag_id=dag_id,
                run_id=run_id,
            ),
        },
    )


def on_failure_callback(context: Context):
    dag_id = context["dag"].dag_id
    run_id = context["run_id"]
    requests.post(
        os.environ.get("AIRFLOW_SLACK_WEBHOOK_URL_FAILURE"),
        json={
            "text": "The DAG `{dag_id}` failed ( run_id: `{run_id}` )".format(
                dag_id=dag_id,
                run_id=run_id,
            ),
        },
    )
