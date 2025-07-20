import sqlite3

import polars as pl

from airflow.sdk import task


@task
def sample_no_summarized_papers(langs: list[str]) -> list[dict]:
    """Sample no summarized papers

    Args:
        langs (list[str]): The language used for summary

    Returns:
        list[dict]: The sampled papers
    """

    query = """
        WITH t AS (
            SELECT
                id
            FROM
                paper_summary
            WHERE
                lang IN ('{langs}')
            GROUP BY
                id
            HAVING
                COUNT(*) = 2
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
            paper.id NOT IN t
    """.format(langs="', '".join(langs))

    with sqlite3.connect("/workspace/db/papers.db") as conn:
        df = pl.read_database(query, conn)

    return df.sample(n=1, shuffle=True).to_dicts() if df.height > 0 else []
