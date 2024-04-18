from enum import Enum, auto
from requests import get


class ExamKind(Enum):
    OGE = auto()
    EGE = auto()
    VPR = auto()


def get_page_content(url: str) -> str:
    return get(url).content
