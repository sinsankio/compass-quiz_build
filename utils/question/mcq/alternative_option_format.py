from crewai import Agent, Task
from dotenv import dotenv_values
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from configs.question.mcq.alternative_option_format import (
    ALTERNATIVE_OPTION_FORMAT_AGENT_LLM_NAME,
    ALTERNATIVE_OPTION_EVALUATE_AGENT_LLM_NAME,
    ALTERNATIVE_OPTION_FORMAT_AGENT_METADATA,
    ALTERNATIVE_OPTION_EVALUATE_AGENT_METADATA,
    ALTERNATIVE_OPTION_FORMAT_TASK_METADATA,
    ALTERNATIVE_OPTION_EVALUATE_TASK_METADATA
)
from entities.question.mcq.output_format import AlternativeOptionFormatOutput, AlternativeOptionEvaluateOutput

ALTERNATIVE_OPTION_FORMAT_AGENT: Agent | None = None
ALTERNATIVE_OPTION_EVALUATE_AGENT: Agent | None = None
ALTERNATIVE_OPTION_FORMAT_TASK: Task | None = None
ALTERNATIVE_OPTION_EVALUATE_TASK: Task | None = None
ALTERNATIVE_OPTION_FORMAT_AGENT_LLM: ChatGoogleGenerativeAI | None = None
ALTERNATIVE_OPTION_EVALUATE_AGENT_LLM: ChatGroq | None = None


def load_alternative_option_format_agent_llm(secret_env_file_path: str = 'secrets.env') -> ChatGoogleGenerativeAI:
    global ALTERNATIVE_OPTION_FORMAT_AGENT_LLM

    if not ALTERNATIVE_OPTION_FORMAT_AGENT_LLM:
        secrets = dotenv_values(secret_env_file_path)
        ALTERNATIVE_OPTION_FORMAT_AGENT_LLM = ChatGoogleGenerativeAI(
            model=ALTERNATIVE_OPTION_FORMAT_AGENT_LLM_NAME,
            google_api_key=secrets.get('GOOGLE_API_KEY')
        )
    return ALTERNATIVE_OPTION_FORMAT_AGENT_LLM


def load_alternative_option_evaluate_agent_llm(secret_env_file_path: str = 'secrets.env') -> ChatGroq:
    global ALTERNATIVE_OPTION_EVALUATE_AGENT_LLM

    if not ALTERNATIVE_OPTION_EVALUATE_AGENT_LLM:
        secrets = dotenv_values(secret_env_file_path)
        ALTERNATIVE_OPTION_EVALUATE_AGENT_LLM = ChatGroq(
            model_name=ALTERNATIVE_OPTION_EVALUATE_AGENT_LLM_NAME,
            groq_api_key=secrets.get('GROQ_API_KEY')
        )
    return ALTERNATIVE_OPTION_EVALUATE_AGENT_LLM


def init_alternative_option_format_agent() -> Agent:
    global ALTERNATIVE_OPTION_FORMAT_AGENT

    if not ALTERNATIVE_OPTION_FORMAT_AGENT:
        ALTERNATIVE_OPTION_FORMAT_AGENT = Agent(
            role=ALTERNATIVE_OPTION_FORMAT_AGENT_METADATA['role'],
            goal=ALTERNATIVE_OPTION_FORMAT_AGENT_METADATA['goal'],
            backstory=ALTERNATIVE_OPTION_FORMAT_AGENT_METADATA['backstory'],
            llm=load_alternative_option_format_agent_llm(),
            verbose=True,
            allow_delegation=False
        )
    return ALTERNATIVE_OPTION_FORMAT_AGENT


def init_alternative_option_evaluate_agent() -> Agent:
    global ALTERNATIVE_OPTION_EVALUATE_AGENT

    if not ALTERNATIVE_OPTION_EVALUATE_AGENT:
        ALTERNATIVE_OPTION_EVALUATE_AGENT = Agent(
            role=ALTERNATIVE_OPTION_EVALUATE_AGENT_METADATA['role'],
            goal=ALTERNATIVE_OPTION_FORMAT_AGENT_METADATA['goal'],
            backstory=ALTERNATIVE_OPTION_FORMAT_AGENT_METADATA['backstory'],
            llm=load_alternative_option_evaluate_agent_llm(),
            verbose=True,
            allow_delegation=False
        )
    return ALTERNATIVE_OPTION_EVALUATE_AGENT


def init_alternative_option_format_task() -> Task:
    global ALTERNATIVE_OPTION_FORMAT_TASK

    if not ALTERNATIVE_OPTION_FORMAT_TASK:
        ALTERNATIVE_OPTION_FORMAT_TASK = Task(
            description=ALTERNATIVE_OPTION_FORMAT_TASK_METADATA['description'],
            agent=init_alternative_option_format_agent(),
            expected_output=ALTERNATIVE_OPTION_FORMAT_TASK_METADATA['expected_output'],
            output_pydantic=AlternativeOptionFormatOutput
        )
    return ALTERNATIVE_OPTION_FORMAT_TASK


def init_alternative_option_evaluate_task() -> Task:
    global ALTERNATIVE_OPTION_EVALUATE_TASK

    if not ALTERNATIVE_OPTION_EVALUATE_TASK:
        ALTERNATIVE_OPTION_EVALUATE_TASK = Task(
            description=ALTERNATIVE_OPTION_EVALUATE_TASK_METADATA['description'],
            agent=init_alternative_option_evaluate_agent(),
            expected_output=ALTERNATIVE_OPTION_EVALUATE_TASK_METADATA['expected_output'],
            output_pydantic=AlternativeOptionEvaluateOutput,
            context=[init_alternative_option_format_task()]
        )
    return ALTERNATIVE_OPTION_EVALUATE_TASK


def str_cast_non_formatted_alternative_options(alternatives: list) -> str:
    str_alternatives = ''
    for i, alternative in enumerate(alternatives):
        str_alternatives += f"{chr(ord('A') + i)}. {alternative}\n"
    return str_alternatives
