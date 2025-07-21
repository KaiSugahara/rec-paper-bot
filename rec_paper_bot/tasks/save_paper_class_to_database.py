import sqlite3
import textwrap

from airflow.sdk import task
from rec_paper_bot.schemas import Paper


@task
def save_paper_class_to_database(paper: Paper, is_recsys: bool):
    """Save the paper class to the database

    Args:
        paper (Paper): The paper meta
        is_recsys (bool): Indicate whether or not the paper is about recommender systems
    """

    with sqlite3.connect("/workspace/db/papers.db") as conn:
        c = conn.cursor()

        # Delete record if exists.
        query = """
            DELETE
            FROM
                paper_classification
            WHERE
                id = '{id}'
        """
        c.execute(textwrap.dedent(query).strip().format(id=paper["id"]))

        # Insert record
        query = """
            INSERT INTO paper_classification (
                id
                , is_recsys
            )
            VALUES (
                '{id}'
                , {is_recsys}
            )
        """
        c.execute(textwrap.dedent(query).strip().format(id=paper["id"], is_recsys=int(is_recsys)))

        conn.commit()
