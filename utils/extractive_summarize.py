import os

from dotenv import dotenv_values
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_groq import ChatGroq

from configs.extractive_summarize import *

READER_MODEL_API_KEY: str | None = None
READER_MODEL: ChatGroq | None = None
EXTRACTIVE_SUMMARIZE_PROMPT_TEMPLATE: str | None = None
EXTRACTIVE_SUMMARIZE_PROMPT: PromptTemplate | None = None
EXTRACTIVE_SUMMARIZE_CHAIN: LLMChain | None = None


class ExtractiveSummarization(BaseModel):
    summarization: str = Field(description='The final extractive summarized content of provided document context')


def load_reader_model_api_key() -> str:
    global READER_MODEL_API_KEY

    if not READER_MODEL_API_KEY:
        secrets = dotenv_values('secrets.env')
        READER_MODEL_API_KEY = secrets.get('GROQ_API_KEY')
        os.environ['GROQ_API_KEY'] = READER_MODEL_API_KEY
    return READER_MODEL_API_KEY


def load_reader_model() -> ChatGroq:
    global READER_MODEL

    if not READER_MODEL:
        load_reader_model_api_key()
        READER_MODEL = ChatGroq(model_name=READER_MODEL_NAME)
    return READER_MODEL


def load_extractive_summarize_prompt_template() -> str | None:
    global EXTRACTIVE_SUMMARIZE_PROMPT_TEMPLATE

    if not EXTRACTIVE_SUMMARIZE_PROMPT_TEMPLATE:
        file_dir, file_name = (EXTRACTIVE_SUMMARIZE_PROMPT_FILE_DATA['dir'],
                               EXTRACTIVE_SUMMARIZE_PROMPT_FILE_DATA['filename'])
        prompt_file_path = f"prompts/{file_dir}/{file_name}"
        with open(prompt_file_path) as file:
            EXTRACTIVE_SUMMARIZE_PROMPT_TEMPLATE = file.read()
    return EXTRACTIVE_SUMMARIZE_PROMPT_TEMPLATE


def load_extractive_summarize_prompt() -> PromptTemplate:
    global EXTRACTIVE_SUMMARIZE_PROMPT

    if not EXTRACTIVE_SUMMARIZE_PROMPT:
        EXTRACTIVE_SUMMARIZE_PROMPT = PromptTemplate(
            input_variables=['subject_area', 'document_context'],
            template=load_extractive_summarize_prompt_template()
        )
    return EXTRACTIVE_SUMMARIZE_PROMPT


def load_extractive_summarize_chain() -> LLMChain:
    global EXTRACTIVE_SUMMARIZE_CHAIN

    if not EXTRACTIVE_SUMMARIZE_CHAIN:
        EXTRACTIVE_SUMMARIZE_CHAIN = (
                load_extractive_summarize_prompt() |
                load_reader_model().with_structured_output(ExtractiveSummarization)
        )
    return EXTRACTIVE_SUMMARIZE_CHAIN


def extractive_summarize(subject_area: str, document_context: str) -> str:
    extractive_summarize_chain = load_extractive_summarize_chain()
    return extractive_summarize_chain.invoke({
        'subject_area': subject_area,
        'document_context': document_context
    }).summarization
