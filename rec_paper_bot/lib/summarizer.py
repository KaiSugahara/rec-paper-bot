import textwrap

from google import genai

from rec_paper_bot.schemas import Summary


class AbstractSummarizer:
    def __init__(self, api_key: str):
        # Gemini client
        self.client = genai.Client(api_key=api_key)

        self.prompts: dict[str, str] = {
            "en": textwrap.dedent("""
                Please provide a brief summary of the objective, methodology, and finding from the abstract of the given paper.
                Note that mathematical formulas should be avoided.

                Input Abstract:
                {abstract}
            """).strip(),
            "ja": textwrap.dedent("""
                Abstract から objective, methodology, finding を日本語で端的に要約してください。
                ただし、数式は避けてください。

                Input Abstract:
                {abstract}
            """).strip(),
        }

    def summarize(self, abstract: str, lang: str) -> Summary:
        """Summarize the abstract

        Args:
            abstract (str): The abstract
            lang (str): The language used for summary

        Returns:
            Summary: The summary
        """

        # Get Prompt
        if lang == "en":
            prompt = self.prompts["en"].format(abstract=abstract)
        elif lang == "ja":
            prompt = self.prompts["ja"].format(abstract=abstract)
        else:
            raise Exception()

        # Get response from Gemini
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": Summary,
            },
        )

        # Parse response
        summary: Summary = response.parsed  # type: ignore

        return summary
