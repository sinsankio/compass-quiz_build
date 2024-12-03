from crewai import Agent, Task
from dotenv import dotenv_values
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from configs.question.essay.answer_construct import (
    ANSWER_CONSTRUCT_FORMAT_AGENT_LLM_NAME,
    ANSWER_EVALUATE_AGENT_LLM_NAME,
    ANSWER_CONSTRUCT_FORMAT_AGENT_METADATA,
    ANSWER_EVALUATE_AGENT_METADATA,
    ANSWER_CONSTRUCT_TASK_METADATA,
    ANSWER_FORMAT_TASK_METADATA,
    ANSWER_EVALUATE_TASK_METADATA
)
from entities.question.essay.output_format import EssayAnswerConstructFormatOutput, EssayAnswerEvaluateOutput

ANSWER_CONSTRUCT_FORMAT_AGENT: Agent | None = None
ANSWER_EVALUATE_AGENT: Agent | None = None
ANSWER_CONSTRUCT_TASK: Task | None = None
ANSWER_FORMAT_TASK: Task | None = None
ANSWER_EVALUATE_TASK: Task | None = None
ANSWER_CONSTRUCT_FORMAT_AGENT_LLM: ChatGoogleGenerativeAI | None = None
ANSWER_EVALUATE_AGENT_LLM: ChatGroq | None = None


def load_answer_construct_format_agent_llm(secret_env_file_path: str = 'secrets.env') -> ChatGoogleGenerativeAI:
    global ANSWER_CONSTRUCT_FORMAT_AGENT_LLM

    if not ANSWER_CONSTRUCT_FORMAT_AGENT_LLM:
        secrets = dotenv_values(secret_env_file_path)
        ANSWER_CONSTRUCT_FORMAT_AGENT_LLM = ChatGoogleGenerativeAI(
            model=ANSWER_CONSTRUCT_FORMAT_AGENT_LLM_NAME,
            google_api_key=secrets.get('GOOGLE_API_KEY')
        )
    return ANSWER_CONSTRUCT_FORMAT_AGENT_LLM


def load_answer_evaluate_agent_llm(secret_env_file_path: str = 'secrets.env') -> ChatGroq:
    global ANSWER_EVALUATE_AGENT_LLM

    if not ANSWER_EVALUATE_AGENT_LLM:
        secrets = dotenv_values(secret_env_file_path)
        ANSWER_EVALUATE_AGENT_LLM = ChatGroq(
            model_name=ANSWER_EVALUATE_AGENT_LLM_NAME,
            groq_api_key=secrets.get('GROQ_API_KEY')
        )
    return ANSWER_EVALUATE_AGENT_LLM


def init_answer_construct_format_agent() -> Agent:
    global ANSWER_CONSTRUCT_FORMAT_AGENT

    if not ANSWER_CONSTRUCT_FORMAT_AGENT:
        ANSWER_CONSTRUCT_FORMAT_AGENT = Agent(
            role=ANSWER_CONSTRUCT_FORMAT_AGENT_METADATA['role'],
            goal=ANSWER_CONSTRUCT_FORMAT_AGENT_METADATA['goal'],
            backstory=ANSWER_CONSTRUCT_FORMAT_AGENT_METADATA['backstory'],
            llm=load_answer_construct_format_agent_llm(),
            verbose=True,
            allow_delegation=False
        )
    return ANSWER_CONSTRUCT_FORMAT_AGENT


def init_answer_evaluate_agent() -> Agent:
    global ANSWER_EVALUATE_AGENT

    if not ANSWER_EVALUATE_AGENT:
        ANSWER_EVALUATE_AGENT = Agent(
            role=ANSWER_EVALUATE_AGENT_METADATA['role'],
            goal=ANSWER_EVALUATE_AGENT_METADATA['goal'],
            backstory=ANSWER_EVALUATE_AGENT_METADATA['backstory'],
            llm=load_answer_evaluate_agent_llm(),
            verbose=True,
            allow_delegation=False
        )
    return ANSWER_EVALUATE_AGENT


def init_answer_construct_task() -> Task:
    global ANSWER_CONSTRUCT_TASK

    if not ANSWER_CONSTRUCT_TASK:
        ANSWER_CONSTRUCT_TASK = Task(
            description=ANSWER_CONSTRUCT_TASK_METADATA['description'],
            agent=init_answer_construct_format_agent(),
            expected_output=ANSWER_CONSTRUCT_TASK_METADATA['expected_output'],
            output_pydantic=EssayAnswerConstructFormatOutput
        )
    return ANSWER_CONSTRUCT_TASK


def init_answer_format_task() -> Task:
    global ANSWER_FORMAT_TASK

    if not ANSWER_FORMAT_TASK:
        ANSWER_FORMAT_TASK = Task(
            description=ANSWER_FORMAT_TASK_METADATA['description'],
            agent=init_answer_construct_format_agent(),
            expected_output=ANSWER_FORMAT_TASK_METADATA['expected_output'],
            output_pydantic=EssayAnswerConstructFormatOutput,
            context=[init_answer_construct_task()]
        )
    return ANSWER_FORMAT_TASK


def init_answer_evaluate_task():
    global ANSWER_EVALUATE_TASK

    if not ANSWER_EVALUATE_TASK:
        ANSWER_EVALUATE_TASK = Task(
            description=ANSWER_EVALUATE_TASK_METADATA['description'],
            agent=init_answer_evaluate_agent(),
            expected_output=ANSWER_EVALUATE_TASK_METADATA['expected_output'],
            output_pydantic=EssayAnswerEvaluateOutput,
            context=[init_answer_construct_task(), init_answer_format_task()]
        )
    return ANSWER_EVALUATE_TASK
