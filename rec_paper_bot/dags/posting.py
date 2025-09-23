from datetime import timedelta

from airflow.sdk import dag
from rec_paper_bot.lib.alert_callback import on_failure_callback, on_success_callback
from rec_paper_bot.tasks import (
    get_now,
    get_summary,
    log_post_time,
    post_paper_summary,
    sample_summarized_but_not_posted_papers,
)

default_args = {
    "owner": "airflow",
    "retries": 3,
    "retry_delay": timedelta(hours=1, minutes=30),
}


@dag(
    "posting",
    default_args=default_args,
    schedule="0 */6 * * *",
    catchup=False,
    on_success_callback=on_success_callback,
    on_failure_callback=on_failure_callback,
)
def generate_dag():
    langs = ["ja", "en"]

    for lang in langs:
        papers = sample_summarized_but_not_posted_papers(lang=lang)
        summaries = get_summary.partial(lang=lang).expand(paper=papers)
        post_ids = post_paper_summary.partial(key="title").expand(paper=papers, summary=summaries)
        for key in ["objective", "methodology", "finding"]:
            post_ids = post_paper_summary.partial(key=key).expand(
                paper=papers, summary=summaries, in_reply_to_post_id=post_ids
            )
        post_times = get_now.expand(flag=post_ids)
        log_post_time.partial(lang=lang).expand(paper=papers, post_time=post_times)


generate_dag()
