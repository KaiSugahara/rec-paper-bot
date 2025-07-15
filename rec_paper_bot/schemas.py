from typing import TypedDict


class Paper(TypedDict):
    id: str
    title: str
    url: str
    published_time: str
    updated_time: str
    authors: str
    abstract: str
