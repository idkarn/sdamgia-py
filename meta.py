from abc import ABC
from typing import TypedDict

from utils import ExamKind, Page

BASE_URL = "https://{}-{}.sdamgia.ru"


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

    def __repr__(self) -> str:
        return f"<Category id={self.id} name='{self.name}'>"

    def get_problems_list(self, limit: int = 0) -> list[Problem]: ...


class TopicType(TypedDict):
    id: int
    name: str
    categories: list[Category]


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
        page = Page(URL)
        topics: list[TopicType] = []

        topic_elems = page.get("div.cat_category:not(.cat_header):has(.cat_children)")

        for topic_elem in topic_elems:
            cat_name_elem = topic_elem.select_one(".cat_name")
            # print([x for x in cat_name_elem.children if x.text != "Т"])
            # if cat_name_elem.find(".theory") is not None:
            #     continue
            # if (content := cat_name_elem.contents)[-2].text != "Т":
            #     print(content)
            #     continue

            elems = [
                x for x in cat_name_elem.contents if x.text != "Т" and x.text != " "
            ]
            if len(elems) <= 1:
                continue

            id, name = elems[-2:]

            topic = {
                "id": int(id.text),
                "name": name.text[2:].strip(),
                "categories": [
                    Category(elem["data-id"], elem.select_one(".cat_name").text)
                    for elem in topic_elem.select(".cat_children > .cat_category")
                ],
            }

            topics.append(topic)

        return topics
