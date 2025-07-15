from airflow.sdk import dag
from rec_paper_bot.tasks import generate_search_query, save_papers_to_database, search_for_papers

default_args = {
    "owner": "airflow",
}


@dag(
    "crawling",
    default_args=default_args,
    schedule="0 * * * *",
    catchup=False,
)
def generate_dag():
    query = generate_search_query()

    papers_json_path = search_for_papers(
        query=query,  # type: ignore
    )

    save_papers_to_database(
        papers_json_path=papers_json_path,  # type: ignore
    )


generate_dag()
