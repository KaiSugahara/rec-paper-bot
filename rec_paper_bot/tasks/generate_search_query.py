import datetime

from airflow.sdk import task


@task
def generate_search_query() -> str:
    """Generate search query for arXiv

    Returns:
        str: The search query
    """

    # Category
    categories: list[str] = ["cs.AI", "cs.IR", "cs.CV", "cs.SE", "cs.LG"]
    query_category: str = "(" + " OR ".join([f"cat:{c}" for c in categories]) + ")"

    # Keyword
    words: list[str] = ["recommender", "recommendation"]
    query_word: str = "(" + " OR ".join([f"all:{w}" for w in words]) + ")"

    # Submitted Date
    start_date: str = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y%m%d")
    end_date: str = datetime.datetime.now().strftime("%Y%m%d")
    query_date: str = f"submittedDate:[{start_date} TO {end_date}235959]"

    return " AND ".join([query_category, query_word, query_date])
