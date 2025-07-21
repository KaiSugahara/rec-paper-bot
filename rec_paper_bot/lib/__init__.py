from twitter_text import parse_tweet

from .classifier import Classifier as Classifier
from .poster import Poster as Poster
from .summarizer import AbstractSummarizer as AbstractSummarizer


def validate_post_text(text: str) -> str:
    """Validate the text for X post

    Args:
        text (str): The text

    Returns:
        str: The validated text
    """

    if parse_tweet(text).valid:
        return text

    if text.endswith("..."):
        return validate_post_text(text[:-4] + "...")

    return validate_post_text(text[:-1] + "...")
