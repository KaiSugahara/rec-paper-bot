from datetime import datetime

from airflow.sdk import task
from rec_paper_bot.lib import Poster, validate_post_text
from rec_paper_bot.schemas import Paper, PaperSummary


@task
def post_paper_summary(paper: Paper, summary: PaperSummary) -> str:
    """Post the paper summary

    Args:
        paper (Paper): The paper meta
        summary (PaperSummary): The summary

    Returns:
        str: The post time
    """

    lang = summary["lang"]

    poster = Poster(lang=lang)

    # Post Title and URL of the paper
    text = validate_post_text(paper["title"] + "\n" + paper["url"])
    post_id = poster.post(text)

    # Post Objectives/Methodology/Findings of the paper
    lang = summary["lang"]
    for key in ["objective", "methodology", "finding"]:
        text = validate_post_text(f"[{lang}] {summary[key]}")
        post_id = poster.post(text, in_reply_to_post_id=post_id)

    # Post Credit
    text = validate_post_text("Summarized by gemini-1.5-flash")
    poster.post(text, in_reply_to_post_id=post_id)

    # Get the post time
    post_time = datetime.now().isoformat(timespec="seconds")

    return post_time
