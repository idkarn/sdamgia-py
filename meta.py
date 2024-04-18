from __future__ import annotations

from abc import ABC
from typing import TypedDict

from utils import ExamKind, get_page_content

BASE_URL = "https://{}-{}.sdamgia.ru"


class TopicType(TypedDict):
    id: int
    name: str
    categories: list[Category]


class Problem:
    id: int
    answer: str
    content: str
    solution: str

    def __init__(self, id: int) -> None:
        self.id = id


class Category:
    id: int
    name: str

    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name

    def get_problems_list(self, limit: int = 0) -> list[Problem]: ...


class Subject(ABC):
    ID: str
    KIND: ExamKind
    DOMAIN: str

    def __init__(self) -> None: ...

    def __init_subclass__(cls) -> None:
        match cls.KIND:
            case ExamKind.EGE:
                cls.DOMAIN = BASE_URL.format(cls.ID, "ege")
            case ExamKind.OGE:
                cls.DOMAIN = BASE_URL.format(cls.ID, "oge")
            case ExamKind.VPR:
                cls.DOMAIN = BASE_URL.format(cls.ID, "vpr")

    def get_topics(self) -> list[TopicType]:
        URL = f"{self.DOMAIN}/prob_catalog"
        page = get_page_content(URL)
        topics: list[TopicType] = []

        for topic_elem in page:
            topic = {
                "id": 0,
                "name": topic_elem.get("name"),
                "categories": [Category(id, name) for id, name in topic_elem],
            }
            topics.append(topic)

        return topics
