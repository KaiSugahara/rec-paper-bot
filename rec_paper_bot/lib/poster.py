import os

import tweepy
from tweepy.client import Response


class Poster:
    def __init__(self, lang: str):
        """Initialize

        Args:
            lang (str): The language used for summary
        """

        LANG = lang.upper()

        # Tweepy client
        self.client = tweepy.Client(
            consumer_key=os.environ.get(f"X_API_KEY_{LANG}"),
            consumer_secret=os.environ.get(f"X_API_KEY_SECRET_{LANG}"),
            access_token=os.environ.get(f"X_ACCESS_TOKEN_{LANG}"),
            access_token_secret=os.environ.get(f"X_ACCESS_TOKEN_SECRET_{LANG}"),
        )

    def post(self, text: str, in_reply_to_post_id: str | None = None) -> str:
        """Post the text

        Args:
            text (str): The text
            in_reply_to_post_id (str | None, optional): The post ID of the post being replied to. Defaults to None

        Returns:
            str: The post id
        """

        response = self.client.create_tweet(text=text, in_reply_to_tweet_id=in_reply_to_post_id)
        assert isinstance(response, Response)

        return response.data["id"]
