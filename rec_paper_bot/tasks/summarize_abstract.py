import os

from airflow.sdk import task
from rec_paper_bot.lib.summarizer import AbstractSummarizer
from rec_paper_bot.schemas import Paper, PaperSummary


@task
def summarize_abstract(paper: Paper, lang: str) -> PaperSummary:
    """Summarize abstract

    Args:
        paper (Paper): The paper
        lang (str): The language used for summary

    Returns:
        PaperSummary: The summary
    """

    api_key = os.environ.get("GEMINI_API_KEY")
    assert api_key is not None

    summary = AbstractSummarizer(api_key).summarize(paper["abstract"], lang=lang)

    return PaperSummary(
        id=paper["id"], lang=lang, objective=summary.objective, methodology=summary.methodology, finding=summary.finding
    )
