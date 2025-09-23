from typing import Literal, Optional

from airflow.sdk import task
from rec_paper_bot.lib import Poster, validate_post_text
from rec_paper_bot.schemas import Paper, PaperSummary


@task
def post_paper_summary(
    paper: Paper,
    summary: PaperSummary,
    key: Literal["title", "objective", "methodology", "finding"],
    in_reply_to_post_id: Optional[str] = None,
) -> str:
    """Post the paper summary

    Args:
        paper (Paper): The paper meta
        summary (PaperSummary): The summary
        key (Literal["title", "objective", "methodology", "finding"]): The key to post
        in_reply_to_post_id (Optional[str], optional): The post ID to reply to. Defaults to None.

    Returns:
        str: The post ID
    """

    lang = summary["lang"]

    poster = Poster(lang=lang)

    # Post Title and URL of the paper
    if key == "title":
        text = validate_post_text(paper["title"] + "\n" + paper["url"])
        post_id = poster.post(text)
        return post_id

    # Post Objectives/Methodology/Findings of the paper
    if key in ["objective", "methodology", "finding"]:
        text = validate_post_text(f"[{key.upper()}] {summary[key]}")
        post_id = poster.post(text, in_reply_to_post_id=in_reply_to_post_id)
        return post_id

    raise NotImplementedError(f"Unsupported key: {key}")
