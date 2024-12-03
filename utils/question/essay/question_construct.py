from crewai import Agent, Task
from dotenv import dotenv_values
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from configs.question.essay.question_construct import (
    QUESTION_CONSTRUCT_FORMAT_AGENT_LLM_NAME,
    QUESTION_EVALUATE_AGENT_LLM_NAME,
    QUESTION_CONSTRUCT_FORMAT_AGENT_METADATA,
    QUESTION_EVALUATE_AGENT_METADATA,
    QUESTION_CONSTRUCT_TASK_METADATA,
    QUESTION_FORMAT_TASK_METADATA,
    QUESTION_EVALUATE_TASK_METADATA
)
from entities.question.essay.output_format import EssayQuestionConstructFormatOutput, EssayQuestionEvaluateOutput

QUESTION_CONSTRUCT_FORMAT_AGENT: Agent | None = None
QUESTION_EVALUATE_AGENT: Agent | None = None
QUESTION_CONSTRUCT_TASK: Task | None = None
QUESTION_FORMAT_TASK: Task | None = None
QUESTION_EVALUATE_TASK: Task | None = None
QUESTION_CONSTRUCT_FORMAT_AGENT_LLM: ChatGoogleGenerativeAI | None = None
QUESTION_EVALUATE_AGENT_LLM: ChatGroq | None = None


def load_question_construct_format_agent_llm(secret_env_file_path: str = 'secrets.env') -> ChatGoogleGenerativeAI:
    global QUESTION_CONSTRUCT_FORMAT_AGENT_LLM

    if not QUESTION_CONSTRUCT_FORMAT_AGENT_LLM:
        secrets = dotenv_values(secret_env_file_path)
        QUESTION_CONSTRUCT_FORMAT_AGENT_LLM = ChatGoogleGenerativeAI(
            model=QUESTION_CONSTRUCT_FORMAT_AGENT_LLM_NAME,
            google_api_key=secrets.get('GOOGLE_API_KEY')
        )
    return QUESTION_CONSTRUCT_FORMAT_AGENT_LLM


def load_question_evaluate_agent_llm(secret_env_file_path: str = 'secrets.env') -> ChatGroq:
    global QUESTION_EVALUATE_AGENT_LLM

    if not QUESTION_EVALUATE_AGENT_LLM:
        secrets = dotenv_values(secret_env_file_path)
        QUESTION_EVALUATE_AGENT_LLM = ChatGroq(
            model_name=QUESTION_EVALUATE_AGENT_LLM_NAME,
            groq_api_key=secrets.get('GROQ_API_KEY')
        )
    return QUESTION_EVALUATE_AGENT_LLM


def init_question_construct_format_agent() -> Agent:
    global QUESTION_CONSTRUCT_FORMAT_AGENT

    if not QUESTION_CONSTRUCT_FORMAT_AGENT:
        QUESTION_CONSTRUCT_FORMAT_AGENT = Agent(
            role=QUESTION_CONSTRUCT_FORMAT_AGENT_METADATA['role'],
            goal=QUESTION_CONSTRUCT_FORMAT_AGENT_METADATA['goal'],
            backstory=QUESTION_CONSTRUCT_FORMAT_AGENT_METADATA['backstory'],
            llm=load_question_construct_format_agent_llm(),
            verbose=True,
            allow_delegation=False
        )
    return QUESTION_CONSTRUCT_FORMAT_AGENT


def init_question_evaluate_agent() -> Agent:
    global QUESTION_EVALUATE_AGENT

    if not QUESTION_EVALUATE_AGENT:
        QUESTION_EVALUATE_AGENT = Agent(
            role=QUESTION_EVALUATE_AGENT_METADATA['role'],
            goal=QUESTION_EVALUATE_AGENT_METADATA['goal'],
            backstory=QUESTION_EVALUATE_AGENT_METADATA['backstory'],
            llm=load_question_evaluate_agent_llm(),
            verbose=True,
            allow_delegation=False
        )
    return QUESTION_EVALUATE_AGENT


def init_question_construct_task() -> Task:
    global QUESTION_CONSTRUCT_TASK

    if not QUESTION_CONSTRUCT_TASK:
        QUESTION_CONSTRUCT_TASK = Task(
            description=QUESTION_CONSTRUCT_TASK_METADATA['description'],
            agent=init_question_construct_format_agent(),
            expected_output=QUESTION_CONSTRUCT_TASK_METADATA['expected_output'],
            output_pydantic=EssayQuestionConstructFormatOutput
        )
    return QUESTION_CONSTRUCT_TASK


def init_question_format_task() -> Task:
    global QUESTION_FORMAT_TASK

    if not QUESTION_FORMAT_TASK:
        QUESTION_FORMAT_TASK = Task(
            description=QUESTION_FORMAT_TASK_METADATA['description'],
            agent=init_question_construct_format_agent(),
            expected_output=QUESTION_FORMAT_TASK_METADATA['expected_output'],
            output_pydantic=EssayQuestionConstructFormatOutput,
            context=[init_question_construct_task()]
        )
    return QUESTION_FORMAT_TASK


def init_question_evaluate_task():
    global QUESTION_EVALUATE_TASK

    if not QUESTION_EVALUATE_TASK:
        QUESTION_EVALUATE_TASK = Task(
            description=QUESTION_EVALUATE_TASK_METADATA['description'],
            agent=init_question_evaluate_agent(),
            expected_output=QUESTION_EVALUATE_TASK_METADATA['expected_output'],
            output_pydantic=EssayQuestionEvaluateOutput,
            context=[init_question_construct_task(), init_question_format_task()]
        )
    return QUESTION_EVALUATE_TASK


def str_cast_pool_essay_questions(pool_essay_questions: list) -> str:
    str_pool_essay_questions = ''
    for i, question in enumerate(pool_essay_questions):
        str_pool_essay_questions += f"{i + 1}. {question}\n"
    return str_pool_essay_questions
