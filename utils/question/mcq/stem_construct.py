from crewai import Agent, Task
from dotenv import dotenv_values
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from configs.question.mcq.stem_construct import (
    STEM_CONSTRUCT_FORMAT_AGENT_LLM_NAME,
    STEM_EVALUATE_AGENT_LLM_NAME,
    STEM_CONSTRUCT_FORMAT_AGENT_METADATA,
    STEM_EVALUATE_AGENT_METADATA,
    STEM_CONSTRUCT_TASK_METADATA,
    STEM_FORMAT_TASK_METADATA,
    STEM_EVALUATE_TASK_METADATA
)
from entities.question.mcq.output_format import StemConstructFormatOutput, StemEvaluateOutput

STEM_CONSTRUCT_FORMAT_AGENT: Agent | None = None
STEM_EVALUATE_AGENT: Agent | None = None
STEM_CONSTRUCT_TASK: Task | None = None
STEM_FORMAT_TASK: Task | None = None
STEM_EVALUATE_TASK: Task | None = None
STEM_CONSTRUCT_FORMAT_AGENT_LLM: ChatGoogleGenerativeAI | None = None
STEM_EVALUATE_AGENT_LLM: ChatGroq | None = None


def load_stem_construct_format_agent_llm(secret_env_file_path: str = 'secrets.env') -> ChatGoogleGenerativeAI:
    global STEM_CONSTRUCT_FORMAT_AGENT_LLM

    if not STEM_CONSTRUCT_FORMAT_AGENT_LLM:
        secrets = dotenv_values(secret_env_file_path)
        STEM_CONSTRUCT_FORMAT_AGENT_LLM = ChatGoogleGenerativeAI(
            model=STEM_CONSTRUCT_FORMAT_AGENT_LLM_NAME,
            google_api_key=secrets.get('GOOGLE_API_KEY')
        )
    return STEM_CONSTRUCT_FORMAT_AGENT_LLM


def load_stem_evaluate_agent_llm(secret_env_file_path: str = 'secrets.env') -> ChatGroq:
    global STEM_EVALUATE_AGENT_LLM

    if not STEM_EVALUATE_AGENT_LLM:
        secrets = dotenv_values(secret_env_file_path)
        STEM_EVALUATE_AGENT_LLM = ChatGroq(
            model_name=STEM_EVALUATE_AGENT_LLM_NAME,
            groq_api_key=secrets.get('GROQ_API_KEY')
        )
    return STEM_EVALUATE_AGENT_LLM


def init_stem_construct_format_agent() -> Agent:
    global STEM_CONSTRUCT_FORMAT_AGENT

    if not STEM_CONSTRUCT_FORMAT_AGENT:
        STEM_CONSTRUCT_FORMAT_AGENT = Agent(
            role=STEM_CONSTRUCT_FORMAT_AGENT_METADATA['role'],
            goal=STEM_CONSTRUCT_FORMAT_AGENT_METADATA['goal'],
            backstory=STEM_CONSTRUCT_FORMAT_AGENT_METADATA['backstory'],
            llm=load_stem_construct_format_agent_llm(),
            verbose=True,
            allow_delegation=False
        )
    return STEM_CONSTRUCT_FORMAT_AGENT


def init_stem_evaluate_agent() -> Agent:
    global STEM_EVALUATE_AGENT

    if not STEM_EVALUATE_AGENT:
        STEM_EVALUATE_AGENT = Agent(
            role=STEM_EVALUATE_AGENT_METADATA['role'],
            goal=STEM_EVALUATE_AGENT_METADATA['goal'],
            backstory=STEM_EVALUATE_AGENT_METADATA['backstory'],
            llm=load_stem_evaluate_agent_llm(),
            verbose=True,
            allow_delegation=False
        )
    return STEM_EVALUATE_AGENT


def init_stem_construct_task() -> Task:
    global STEM_CONSTRUCT_TASK

    if not STEM_CONSTRUCT_TASK:
        STEM_CONSTRUCT_TASK = Task(
            description=STEM_CONSTRUCT_TASK_METADATA['description'],
            agent=init_stem_construct_format_agent(),
            expected_output=STEM_CONSTRUCT_TASK_METADATA['expected_output'],
            output_pydantic=StemConstructFormatOutput
        )
    return STEM_CONSTRUCT_TASK


def init_stem_format_task() -> Task:
    global STEM_FORMAT_TASK

    if not STEM_FORMAT_TASK:
        STEM_FORMAT_TASK = Task(
            description=STEM_FORMAT_TASK_METADATA['description'],
            agent=init_stem_construct_format_agent(),
            expected_output=STEM_FORMAT_TASK_METADATA['expected_output'],
            output_pydantic=StemConstructFormatOutput,
            context=[init_stem_construct_task()]
        )
    return STEM_FORMAT_TASK


def init_stem_evaluate_task():
    global STEM_EVALUATE_TASK

    if not STEM_EVALUATE_TASK:
        STEM_EVALUATE_TASK = Task(
            description=STEM_EVALUATE_TASK_METADATA['description'],
            agent=init_stem_evaluate_agent(),
            expected_output=STEM_EVALUATE_TASK_METADATA['expected_output'],
            output_pydantic=StemEvaluateOutput,
            context=[init_stem_construct_task(), init_stem_format_task()]
        )
    return STEM_EVALUATE_TASK


def str_cast_pool_mcq_stems(pool_mcq_stems: list) -> str:
    str_pool_mcq_stems = ''
    for i, stem in enumerate(pool_mcq_stems):
        str_pool_mcq_stems += f"{i + 1}. {stem}\n"
    return str_pool_mcq_stems
