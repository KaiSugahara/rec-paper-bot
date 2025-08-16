from datetime import timedelta

from airflow.sdk import dag
from rec_paper_bot.lib.alert_callback import on_failure_callback, on_success_callback
from rec_paper_bot.tasks import classify_paper, sample_no_classified_paper, save_paper_class_to_database

default_args = {
    "owner": "airflow",
    "retries": 3,
    "retry_delay": timedelta(minutes=10),
}


@dag(
    "classification",
    default_args=default_args,
    schedule="*/30 * * * *",
    catchup=False,
    on_success_callback=on_success_callback,
    on_failure_callback=on_failure_callback,
)
def generate_dag():
    papers = sample_no_classified_paper()
    flags = classify_paper.expand(paper=papers)
    save_paper_class_to_database.expand(paper=papers, is_recsys=flags)


generate_dag()
