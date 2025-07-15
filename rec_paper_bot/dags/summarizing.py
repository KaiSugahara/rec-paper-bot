from airflow.sdk import dag, task
from rec_paper_bot.tasks import sample_no_summarized_papers, save_paper_summary_to_database, summarize_abstract

default_args = {
    "owner": "airflow",
}


@dag(
    "summarizing",
    default_args=default_args,
    schedule="0 * * * *",
    catchup=False,
)
def generate_dag():
    @task
    def get_combinations(papers, langs):
        return [{"paper": paper, "lang": lang} for paper in papers for lang in langs]

    langs = ["ja", "en"]

    papers = sample_no_summarized_papers(langs=langs)
    combinations = get_combinations(papers=papers, langs=langs)
    paper_summaries = summarize_abstract.expand_kwargs(combinations)
    save_paper_summary_to_database.expand(paper_summary=paper_summaries)


generate_dag()
