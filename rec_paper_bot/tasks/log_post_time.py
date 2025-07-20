import sqlite3
import textwrap

from airflow.sdk import task
from rec_paper_bot.schemas import Paper


@task
def log_post_time(paper: Paper, lang: str, post_time: str):
    """Log the post time

    Args:
        paper (Paper): The paper meta
        lang (str): The language used for summary
        post_time (str): The post time
    """

    query = (
        textwrap.dedent("""
        INSERT INTO paper_post (
            id
            , lang
            , post_time
        )
        VALUES (
            '{id}'
            , '{lang}'
            , '{post_time}'
        )
    """)
        .strip()
        .format(
            id=paper["id"],
            lang=lang,
            post_time=post_time,
        )
    )

    with sqlite3.connect("/workspace/db/papers.db") as conn:
        c = conn.cursor()
        c.execute(query)
        conn.commit()
