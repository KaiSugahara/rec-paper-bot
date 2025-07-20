import os
import sqlite3


def init_db():
    os.makedirs("/workspace/db", exist_ok=True)
    with sqlite3.connect("/workspace/db/papers.db") as conn:
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

        conn.commit()


if __name__ == "__main__":
    init_db()
