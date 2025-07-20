import json
import os
import sqlite3

from airflow.sdk import task

from rec_paper_bot.schemas import Paper


@task
def save_papers_to_database(papers_json_path: str):
    """Save the papers to the database

    Args:
        papers_json_path (str): The path to the JSON file for the papers
    """

    # Load papers
    with open(papers_json_path, "rb") as f:
        papers: list[Paper] = json.load(f)
        os.unlink(papers_json_path)
    print("# of papers:", len(papers))

    # Save papers to the database
    with sqlite3.connect("/db/papers.db") as conn:
        c = conn.cursor()

        c.execute(
            """
                CREATE TABLE IF NOT EXISTS paper (
                    id text primary key
                    , title text
                    , url text
                    , published_time text
                    , updated_time text
                    , authors text
                    , abstract text
                )
            """
        )

        c.execute(
            """
                CREATE TABLE IF NOT EXISTS paper_summary (
                    id text
                    , lang text
                    , objective text
                    , methodology text
                    , finding text
                    , foreign key (id) references paper(id)
                )
            """
        )

        c.execute(
            """
                CREATE TABLE IF NOT EXISTS paper_post (
                    id text
                    , lang text
                    , post_time text
                    , foreign key (id) references paper(id)
                )
            """
        )

        c.execute("PRAGMA foreign_keys = ON")

        c.executemany(
            """
                INSERT INTO paper (id, title, url, published_time, updated_time, authors, abstract) VALUES (:id, :title, :url, :published_time, :updated_time, :authors, :abstract)
                ON CONFLICT (id)
                DO UPDATE SET id=:id, title=:title, url=:url, published_time=:published_time, updated_time=:updated_time, authors=:authors, abstract=:abstract
            """,
            papers,
        )

        conn.commit()
