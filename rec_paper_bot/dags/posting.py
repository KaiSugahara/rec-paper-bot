from airflow.sdk import dag
from rec_paper_bot.lib.alert_callback import on_failure_callback, on_success_callback
from rec_paper_bot.tasks import get_summary, log_post_time, post_paper_summary, sample_summarized_but_not_posted_papers

default_args = {
    "owner": "airflow",
}


@dag(
    "posting",
    default_args=default_args,
    schedule="0 */8 * * *",
    catchup=False,
    on_success_callback=on_success_callback,
    on_failure_callback=on_failure_callback,
)
def generate_dag():
    langs = ["ja", "en"]

    for lang in langs:
        papers = sample_summarized_but_not_posted_papers(lang=lang)
        summaries = get_summary.partial(lang=lang).expand(paper=papers)
        post_times = post_paper_summary.expand(paper=papers, summary=summaries)
        log_post_time.partial(lang=lang).expand(paper=papers, post_time=post_times)


generate_dag()
