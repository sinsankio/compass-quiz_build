from crewai import Agent, Task
from dotenv import dotenv_values
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from configs.question.mcq.key_construct import (
    KEY_CONSTRUCT_AGENT_LLM_NAME,
    KEY_EVALUATE_AGENT_LLM_NAME,
    KEY_CONSTRUCT_AGENT_METADATA,
    KEY_EVALUATE_AGENT_METADATA,
    KEY_CONSTRUCT_TASK_METADATA,
    KEY_EVALUATE_TASK_METADATA
)
from entities.question.mcq.output_format import KeyConstructOutput, KeyEvaluateOutput

KEY_CONSTRUCT_AGENT: Agent | None = None
KEY_EVALUATE_AGENT: Agent | None = None
KEY_CONSTRUCT_TASK: Task | None = None
KEY_EVALUATE_TASK: Task | None = None
KEY_CONSTRUCT_AGENT_LLM: ChatGoogleGenerativeAI | None = None
KEY_EVALUATE_AGENT_LLM: ChatGroq | None = None


def load_key_construct_agent_llm(secret_env_file_path: str = 'secrets.env') -> ChatGoogleGenerativeAI:
    global KEY_CONSTRUCT_AGENT_LLM

    if not KEY_CONSTRUCT_AGENT_LLM:
        secrets = dotenv_values(secret_env_file_path)
        KEY_CONSTRUCT_AGENT_LLM = ChatGoogleGenerativeAI(
            model=KEY_CONSTRUCT_AGENT_LLM_NAME,
            google_api_key=secrets.get('GOOGLE_API_KEY')
        )
    return KEY_CONSTRUCT_AGENT_LLM


def load_key_evaluate_agent_llm(secret_env_file_path: str = 'secrets.env') -> ChatGroq:
    global KEY_EVALUATE_AGENT_LLM

    if not KEY_EVALUATE_AGENT_LLM:
        secrets = dotenv_values(secret_env_file_path)
        KEY_EVALUATE_AGENT_LLM = ChatGroq(
            model_name=KEY_EVALUATE_AGENT_LLM_NAME,
            groq_api_key=secrets.get('GROQ_API_KEY')
        )
    return KEY_EVALUATE_AGENT_LLM


def init_key_construct_agent() -> Agent:
    global KEY_CONSTRUCT_AGENT

    if not KEY_CONSTRUCT_AGENT:
        KEY_CONSTRUCT_AGENT = Agent(
            role=KEY_CONSTRUCT_AGENT_METADATA['role'],
            goal=KEY_CONSTRUCT_AGENT_METADATA['goal'],
            backstory=KEY_CONSTRUCT_AGENT_METADATA['backstory'],
            llm=load_key_construct_agent_llm(),
            verbose=True,
            allow_delegation=False
        )
    return KEY_CONSTRUCT_AGENT


def init_key_evaluate_agent() -> Agent:
    global KEY_EVALUATE_AGENT

    if not KEY_EVALUATE_AGENT:
        KEY_EVALUATE_AGENT = Agent(
            role=KEY_EVALUATE_AGENT_METADATA['role'],
            goal=KEY_EVALUATE_AGENT_METADATA['goal'],
            backstory=KEY_EVALUATE_AGENT_METADATA['backstory'],
            llm=load_key_evaluate_agent_llm(),
            verbose=True,
            allow_delegation=False
        )
    return KEY_EVALUATE_AGENT


def init_key_construct_task() -> Task:
    global KEY_CONSTRUCT_TASK

    if not KEY_CONSTRUCT_TASK:
        KEY_CONSTRUCT_TASK = Task(
            description=KEY_CONSTRUCT_TASK_METADATA['description'],
            agent=init_key_construct_agent(),
            expected_output=KEY_CONSTRUCT_TASK_METADATA['expected_output'],
            output_pydantic=KeyConstructOutput
        )
    return KEY_CONSTRUCT_TASK


def init_key_evaluate_task() -> Task:
    global KEY_EVALUATE_TASK

    if not KEY_EVALUATE_TASK:
        KEY_EVALUATE_TASK = Task(
            description=KEY_EVALUATE_TASK_METADATA['description'],
            agent=init_key_evaluate_agent(),
            expected_output=KEY_EVALUATE_TASK_METADATA['expected_output'],
            output_pydantic=KeyEvaluateOutput,
            context=[init_key_construct_task()]
        )
    return KEY_EVALUATE_TASK
