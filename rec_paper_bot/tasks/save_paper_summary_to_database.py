import sqlite3
import textwrap

from airflow.sdk import task
from rec_paper_bot.schemas import PaperSummary


@task
def save_paper_summary_to_database(paper_summary: PaperSummary):
    """Save the paper summary to the database

    Args:
        paper_summary (PaperSummary): The summary
    """

    with sqlite3.connect("/workspace/db/papers.db") as conn:
        c = conn.cursor()

        # Delete record if exists.
        query = textwrap.dedent("""
                DELETE
                FROM
                    paper_summary
                WHERE
                    id = :id
                    AND lang = :lang
            """).strip()
        c.execute(query, dict(id=paper_summary["id"], lang=paper_summary["lang"]))

        # Insert record
        query = textwrap.dedent("""
                INSERT INTO paper_summary (
                    id
                    , lang
                    , objective
                    , methodology
                    , finding
                )
                VALUES (
                    :id
                    , :lang
                    , :objective
                    , :methodology
                    , :finding
                )
            """).strip()
        c.execute(query, paper_summary)

        conn.commit()
