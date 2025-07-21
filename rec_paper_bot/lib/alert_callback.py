import os
import textwrap

import requests

from airflow.sdk.definitions.context import Context

success_message = """
    The DAG {dag_id} succeeded
    ```
    run_id: {run_id}
    ```
"""

failure_message = """
    The DAG {dag_id} failed
    ```
    run_id: {run_id}
    ```
"""


def on_success_callback(context: Context):
    dag_id = context["dag"].dag_id
    run_id = context["run_id"]
    requests.post(
        os.environ.get("AIRFLOW_SLACK_WEBHOOK_URL_SUCCESS"),
        json={
            "text": textwrap.dedent(success_message)
            .strip()
            .format(
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
            "text": textwrap.dedent(failure_message)
            .strip()
            .format(
                dag_id=dag_id,
                run_id=run_id,
            ),
        },
    )
