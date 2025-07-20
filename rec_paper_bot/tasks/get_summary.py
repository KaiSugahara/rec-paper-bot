import sqlite3
import textwrap

import polars as pl

from airflow.sdk import task
from rec_paper_bot.schemas import Paper, PaperSummary


@task
def get_summary(paper: Paper, lang: str) -> PaperSummary:
    """Get summary

    Args:
        paper (Paper): The paper
        lang (str): The language used for summary

    Returns:
        PaperSummary: The summary
    """

    query = (
        textwrap.dedent("""
        SELECT
            id
            , lang
            , objective
            , methodology
            , finding
        FROM
            paper_summary
        WHERE
            id = '{id}'
            AND lang = '{lang}'
    """)
        .strip()
        .format(id=paper["id"], lang=lang)
    )

    with sqlite3.connect("/db/papers.db") as conn:
        df = pl.read_database(query, conn)

    if df.height != 1:
        raise ValueError()

    return PaperSummary(**df.to_dicts()[0])
