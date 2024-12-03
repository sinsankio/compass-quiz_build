from enum import Enum


class QuestionType(str, Enum):
    MCQ = "MCQ (Multiple Choice Question)"
    ESSAY = "ESSAY"
