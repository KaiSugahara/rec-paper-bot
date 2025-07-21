import sqlite3

import polars as pl

from airflow.sdk import task
from rec_paper_bot.schemas import Paper


@task
def sample_no_classified_paper() -> list[Paper]:
    """Sample no classified paper

    Returns:
        list[Paper]: The sampled papers
    """

    query = """
        WITH classified_paper AS (
            SELECT
                id
            FROM
                paper_classification
        )
        SELECT
            id
            , title
            , url
            , published_time
            , updated_time
            , authors
            , abstract
        FROM
            paper
        WHERE
            paper.id NOT IN classified_paper
    """

    with sqlite3.connect("/workspace/db/papers.db") as conn:
        df = pl.read_database(query, conn)

    return [Paper(**d) for d in df.sample(n=1, shuffle=True).to_dicts()] if df.height > 0 else []
