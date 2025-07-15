from typing import TypedDict

from pydantic import BaseModel


class Paper(TypedDict):
    id: str
    title: str
    url: str
    published_time: str
    updated_time: str
    authors: str
    abstract: str


class PaperSummary(TypedDict):
    id: str
    lang: str
    objective: str
    methodology: str
    finding: str


class Summary(BaseModel):
    objective: str
    methodology: str
    finding: str
