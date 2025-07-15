import json
from tempfile import NamedTemporaryFile

import arxiv

from airflow.sdk import task
from rec_paper_bot.schemas import Paper


@task
def search_for_papers(query: str) -> str:
    """Search for papers on arXiv

    Args:
        query (str): The search query

    Returns:
        str: The path to the JSON file for the papers
    """

    papers: list[Paper] = [
        Paper(
            id=paper.entry_id,
            title=paper.title,
            url=paper.links[0].href,
            published_time=paper.published.strftime("%Y/%m/%d %H:%M"),
            updated_time=paper.updated.strftime("%Y/%m/%d %H:%M"),
            authors=", ".join([author.name for author in paper.authors]),
            abstract=paper.summary,
        )
        for paper in arxiv.Client().results(
            arxiv.Search(
                query=query,
                sort_by=arxiv.SortCriterion.SubmittedDate,
                sort_order=arxiv.SortOrder.Descending,
                max_results=None,
            )
        )
    ]

    f = NamedTemporaryFile("w", delete=False)
    json.dump(papers, f)
    f.close()

    return f.name
