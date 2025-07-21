import textwrap

from google import genai


class Classifier:
    def __init__(self, api_key: str):
        # Gemini client
        self.client = genai.Client(api_key=api_key)

        self.prompt = """
            Is the following paper about research on recommender systems?

            Title: {title}
            Abstract:
            {abstract}
        """

    def classify(self, title: str, abstract: str) -> bool:
        """Classify the paper based on its title and abstract

        Args:
            title (str): The title
            abstract (str): The abstract

        Returns:
            bool: Indicate whether or not the paper is about recommender systems
        """

        # Get response from Gemini
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=textwrap.dedent(self.prompt).strip().format(title=title, abstract=abstract),
            config={
                "response_mime_type": "application/json",
                "response_schema": bool,
            },
        )

        # Parse response
        result = response.parsed
        assert isinstance(result, bool)

        return result
