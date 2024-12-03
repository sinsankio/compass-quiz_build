import secrets
import string
import uuid

from pydantic import BaseModel, Field

from entities.blooms_taxonomy_level import McqBloomsTaxonomyLevel, EssayBloomsTaxonomyLevel
from entities.difficulty_level import DifficultyLevel
from entities.prompt_number import PromptNumber
from entities.question.essay.question_type import EssayQuestionType
from utils.datetime import get_iso_datetime, add_iso_datetime


def id_generator() -> str:
    return str(uuid.uuid4())


def key_generator(length=25) -> str:
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def username_generator(length=25) -> str:
    key = ''.join(secrets.choice(string.ascii_letters) for _ in range(length))
    return f'compass-user-{key}'


def api_key_generator(length=50) -> str:
    return f'compass-api-{key_generator(length=length)}'


def quiz_plan_name_generator(length=10) -> str:
    return f'compass-qp-{key_generator(length=length)}'


class Topic(BaseModel):
    id: str = Field(default_factory=id_generator, alias="_id")
    description: str | None = Field(default=None)
    summarized_content: str | None = Field(default=None, alias='summarizedContent')


class Knowledge(BaseModel):
    id: str = Field(alias='_id')
    subject_description: str = Field(alias='subjectDescription')
    topics: list[Topic] = Field(default=[])
    topic_modeling_coherence_score: float | None = Field(default=None, alias='topicModelingCoherenceScore')


class McqQuestionStructure(BaseModel):
    id: str = Field(default_factory=id_generator, alias='_id')
    topic: str | Topic = Field()
    blooms_taxonomy_level: McqBloomsTaxonomyLevel = Field(
        default=McqBloomsTaxonomyLevel.KNOWLEDGE,
        alias='bloomsTaxonomyLevel'
    )
    difficulty_level: DifficultyLevel = Field(default=DifficultyLevel.EASY, alias='difficultyLevel')
    num_questions: int = Field(default=1, le=20, ge=0, alias='numQuestions')
    num_distractors: PromptNumber = Field(alias='numDistractors', default=PromptNumber.FIVE)


class EssayQuestionStructure(BaseModel):
    id: str = Field(default_factory=id_generator, alias='_id')
    topic: str | Topic = Field()
    question_type: EssayQuestionType = Field(alias='questionType', default=EssayQuestionType.RESTRICTED_RESPONSE)
    blooms_taxonomy_level: EssayBloomsTaxonomyLevel = Field(
        default=EssayBloomsTaxonomyLevel.APPLICATION,
        alias='bloomsTaxonomyLevel'
    )
    difficulty_level: DifficultyLevel = Field(default=DifficultyLevel.EASY, alias='difficultyLevel')
    num_questions: int = Field(default=1, le=20, ge=0, alias='numQuestions')
    min_word_count: int = Field(default=100, le=1000, ge=0, alias='minWordCount')
    max_word_count: int = Field(default=200, le=1000, ge=0, alias='maxWordCount')


class MCQ(BaseModel):
    id: str = Field(default_factory=id_generator, alias='_id')
    stem: str = Field()
    key: str = Field()
    alternatives: list[str] = Field()


class Essay(BaseModel):
    id: str = Field(default_factory=id_generator, alias='_id')
    question: str = Field()
    answer: str = Field()
    type: EssayQuestionType = Field(default=EssayQuestionType.RESTRICTED_RESPONSE)


class TimeDuration(BaseModel):
    hours: int = Field()
    minutes: int = Field()
    seconds: int = Field()


class Quiz(BaseModel):
    id: str = Field(default_factory=id_generator, alias='_id')
    mcqs: list[MCQ] = Field(default=[])
    essays: list[Essay] = Field(default=[])
    build_time: TimeDuration = Field(alias='buildTime')


class QuizPlan(BaseModel):
    id: str = Field(default_factory=id_generator, alias='_id')
    name: str = Field(default_factory=quiz_plan_name_generator)
    description: str | None = Field(default=None)
    created_on: str | None = Field(default_factory=get_iso_datetime, alias='createdOn')
    expired_on: str | None = Field(default=add_iso_datetime(days=30), alias='expiredOn')
    knowledge_base_id: str = Field(alias='knowledgeBaseId')
    question_structures: list[McqQuestionStructure | EssayQuestionStructure] = Field(default=[],
                                                                                     alias='questionStructures')
    quizzes: list[Quiz] = Field(default=[])


class QuizPlanForQuizBuild(BaseModel):
    id: str = Field(default_factory=id_generator, alias='_id')
    name: str = Field(default_factory=quiz_plan_name_generator)
    subject_description: str = Field(alias='subjectDescription')
    description: str | None = Field(default=None)
    created_on: str | None = Field(default_factory=get_iso_datetime, alias='createdOn')
    expired_on: str | None = Field(default=add_iso_datetime(days=30), alias='expiredOn')
    knowledge_base_id: str = Field(alias='knowledgeBaseId')
    question_structures: list[McqQuestionStructure | EssayQuestionStructure] = Field(
        default=[],
        alias='questionStructures'
    )
    quizzes: list[Quiz] = Field(default=[])


class UpdatableQuizPlan(BaseModel):
    name: str = Field()
    description: str | None = Field(default=None)
    # expired_on: str = Field(default=None, alias='expiredOn')
    question_structures: list[McqQuestionStructure | EssayQuestionStructure] = Field(default=[],
                                                                                     alias='questionStructures')
    knowledge_base_id: str = Field(alias='knowledgeBaseId')


class KnowledgeInit(BaseModel):
    id: str = Field(default_factory=id_generator, alias='_id')


class User(BaseModel):
    username: str = Field(default_factory=username_generator)
    api_key: str = Field(default_factory=api_key_generator, alias='apiKey')
    knowledge_bases: list[Knowledge] = Field(default=[], alias='knowledgeBases')
    quiz_plans: list[QuizPlan] = Field(default=[], alias='quizPlans')


class Authentication(BaseModel):
    api_key: str = Field(alias='apiKey')


class AllowedFileNames(BaseModel):
    file_names: list[str] = Field(default=[], alias='fileNames')
