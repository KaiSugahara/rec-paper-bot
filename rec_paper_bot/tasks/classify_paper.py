import os

from airflow.sdk import task
from rec_paper_bot.lib.classifier import Classifier
from rec_paper_bot.schemas import Paper


@task
def classify_paper(paper: Paper) -> bool:
    """Classify the paper

    Args:
        paper (Paper): The paper

    Returns:
        bool: Indicate whether or not the paper is about recommender systems
    """

    api_key = os.environ.get("GEMINI_API_KEY")
    assert api_key is not None

    return Classifier(api_key=api_key).classify(title=paper["title"], abstract=paper["abstract"])
