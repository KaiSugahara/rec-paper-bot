import sqlite3
import textwrap

import polars as pl

from airflow.sdk import task
from rec_paper_bot.schemas import Paper


@task
def sample_summarized_but_not_posted_papers(lang: str) -> list[Paper]:
    """Sample summarized, but not posted, papers

    Args:
        lang (str): The language used for summary

    Returns:
        list[Paper]: The list of the papers
    """

    query = (
        textwrap.dedent("""
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
            INNER JOIN paper_summary
                ON paper.id = paper_summary.id
            LEFT JOIN paper_post
                ON paper.id = paper_post.id
                AND paper_summary.lang = paper_post.lang
        WHERE
            paper_summary.lang = '{lang}'
            AND paper_post.post_time IS NULL
    """)
        .strip()
        .format(lang=lang)
    )

    with sqlite3.connect("/workspace/db/papers.db") as conn:
        df = pl.read_database(query, conn)

    return [Paper(**d) for d in df.sample(n=1, shuffle=True).to_dicts()] if df.height > 0 else []
