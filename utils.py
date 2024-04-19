from enum import Enum, auto
from requests import get
from bs4 import BeautifulSoup, ResultSet, Tag


class ExamKind(Enum):
    OGE = auto()
    EGE = auto()
    VPR = auto()


class Page:
    def __init__(self, url: str) -> None:
        page = get_page_content(url)
        self.html = BeautifulSoup(page, "html.parser")

    def get(self, seletor: str) -> ResultSet[Tag]:
        return self.html.select(seletor)


def get_page_content(url: str) -> str:
    return get(url).content
