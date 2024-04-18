from meta import Subject
from utils import ExamKind


class Math(Subject):
    ID = "math"
    KIND = ExamKind.EGE


class MathBase(Subject):
    ID = "mathb"
    KIND = ExamKind.EGE


class Biology(Subject):
    ID = "bio"
    KIND = ExamKind.OGE
