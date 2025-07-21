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
                COUNT(*) = {lang_num}
        )
        SELECT
            paper.id
            , title
            , url
            , published_time
            , updated_time
            , authors
            , abstract
        FROM
            paper
            INNER JOIN paper_classification
                ON paper.id = paper_classification.id
        WHERE
            paper.id NOT IN t
            AND paper_classification.is_recsys = 1
    """.format(langs="', '".join(langs), lang_num=len(langs))

    with sqlite3.connect("/workspace/db/papers.db") as conn:
        df = pl.read_database(query, conn)

    return df.sample(n=1, shuffle=True).to_dicts() if df.height > 0 else []
