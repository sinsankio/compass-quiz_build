from crewai import Agent, Task
from dotenv import dotenv_values
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from configs.question.mcq.distractor_construct import (
    DISTRACTOR_CONSTRUCT_AGENT_LLM_NAME,
    DISTRACTOR_EVALUATE_AGENT_LLM_NAME,
    DISTRACTOR_CONSTRUCT_AGENT_METADATA,
    DISTRACTOR_EVALUATE_AGENT_METADATA,
    DISTRACTOR_CONSTRUCT_TASK_METADATA,
    DISTRACTOR_EVALUATE_TASK_METADATA
)
from entities.question.mcq.output_format import DistractorConstructOutput, DistractorEvaluateOutput

DISTRACTOR_CONSTRUCT_AGENT: Agent | None = None
DISTRACTOR_EVALUATE_AGENT: Agent | None = None
DISTRACTOR_CONSTRUCT_TASK: Task | None = None
DISTRACTOR_EVALUATE_TASK: Task | None = None
DISTRACTOR_CONSTRUCT_AGENT_LLM: ChatGoogleGenerativeAI | None = None
DISTRACTOR_EVALUATE_AGENT_LLM: ChatGroq | None = None


def load_distractor_construct_agent_llm(secret_env_file_path: str = 'secrets.env') -> ChatGoogleGenerativeAI:
    global DISTRACTOR_CONSTRUCT_AGENT_LLM

    if not DISTRACTOR_CONSTRUCT_AGENT_LLM:
        secrets = dotenv_values(secret_env_file_path)
        DISTRACTOR_CONSTRUCT_AGENT_LLM = ChatGoogleGenerativeAI(
            model=DISTRACTOR_CONSTRUCT_AGENT_LLM_NAME,
            google_api_key=secrets.get('GOOGLE_API_KEY')
        )
    return DISTRACTOR_CONSTRUCT_AGENT_LLM


def load_distractor_evaluate_agent_llm(secret_env_file_path: str = 'secrets.env') -> ChatGroq:
    global DISTRACTOR_EVALUATE_AGENT_LLM

    if not DISTRACTOR_EVALUATE_AGENT_LLM:
        secrets = dotenv_values(secret_env_file_path)
        DISTRACTOR_EVALUATE_AGENT_LLM = ChatGroq(
            model_name=DISTRACTOR_EVALUATE_AGENT_LLM_NAME,
            groq_api_key=secrets.get('GROQ_API_KEY')
        )
    return DISTRACTOR_EVALUATE_AGENT_LLM


def init_distractor_construct_agent() -> Agent:
    global DISTRACTOR_CONSTRUCT_AGENT

    if not DISTRACTOR_CONSTRUCT_AGENT:
        DISTRACTOR_CONSTRUCT_AGENT = Agent(
            role=DISTRACTOR_CONSTRUCT_AGENT_METADATA['role'],
            goal=DISTRACTOR_CONSTRUCT_AGENT_METADATA['goal'],
            backstory=DISTRACTOR_CONSTRUCT_AGENT_METADATA['backstory'],
            llm=load_distractor_construct_agent_llm(),
            verbose=True,
            allow_delegation=False
        )
    return DISTRACTOR_CONSTRUCT_AGENT


def init_distractor_evaluate_agent() -> Agent:
    global DISTRACTOR_EVALUATE_AGENT

    if not DISTRACTOR_EVALUATE_AGENT:
        DISTRACTOR_EVALUATE_AGENT = Agent(
            role=DISTRACTOR_EVALUATE_AGENT_METADATA['role'],
            goal=DISTRACTOR_EVALUATE_AGENT_METADATA['goal'],
            backstory=DISTRACTOR_EVALUATE_AGENT_METADATA['backstory'],
            llm=load_distractor_evaluate_agent_llm(),
            verbose=True,
            allow_delegation=False
        )
    return DISTRACTOR_EVALUATE_AGENT


def init_distractor_construct_task() -> Task:
    global DISTRACTOR_CONSTRUCT_TASK

    if not DISTRACTOR_CONSTRUCT_TASK:
        DISTRACTOR_CONSTRUCT_TASK = Task(
            description=DISTRACTOR_CONSTRUCT_TASK_METADATA['description'],
            agent=init_distractor_construct_agent(),
            expected_output=DISTRACTOR_CONSTRUCT_TASK_METADATA['expected_output'],
            output_pydantic=DistractorConstructOutput
        )
    return DISTRACTOR_CONSTRUCT_TASK


def init_distractor_evaluate_task() -> Task:
    global DISTRACTOR_EVALUATE_TASK

    if not DISTRACTOR_EVALUATE_TASK:
        DISTRACTOR_EVALUATE_TASK = Task(
            description=DISTRACTOR_EVALUATE_TASK_METADATA['description'],
            agent=init_distractor_evaluate_agent(),
            expected_output=DISTRACTOR_EVALUATE_TASK_METADATA['expected_output'],
            output_pydantic=DistractorEvaluateOutput,
            context=[init_distractor_construct_task()]
        )
    return DISTRACTOR_EVALUATE_TASK
