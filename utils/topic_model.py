import os
from typing import Any

import gensim.corpora as corpora
import nltk
from dotenv import dotenv_values
from gensim.models import CoherenceModel
from gensim.models import LdaModel
from gensim.utils import simple_preprocess
from langchain.chains import LLMChain
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from nltk.corpus import stopwords

from configs.topic_model import *

nltk.download('stopwords')

READER_MODEL_API_KEY: str | None = None
READER_MODEL: ChatGoogleGenerativeAI | None = None
TOPIC_CONSTRUCT_PROMPT_TEMPLATE: str | None = None
TOPIC_CONSTRUCT_PROMPT: PromptTemplate | None = None
TOPIC_CONSTRUCT_CHAIN: LLMChain | None = None
TOPIC_CONSTRUCT_OUTPUT_PARSER: JsonOutputParser | None = None


class Topic(BaseModel):
    topic: str = Field()


def load_reader_model_api_key() -> str:
    global READER_MODEL_API_KEY

    if not READER_MODEL_API_KEY:
        secrets = dotenv_values('secrets.env')
        READER_MODEL_API_KEY = secrets.get('GOOGLE_API_KEY')
        os.environ['GOOGLE_API_KEY'] = READER_MODEL_API_KEY
    return READER_MODEL_API_KEY


def load_reader_model() -> ChatGoogleGenerativeAI:
    global READER_MODEL

    if not READER_MODEL:
        load_reader_model_api_key()
        READER_MODEL = ChatGoogleGenerativeAI(model=READER_MODEL_NAME)
    return READER_MODEL


def load_topic_construct_output_parser() -> JsonOutputParser:
    global TOPIC_CONSTRUCT_OUTPUT_PARSER

    if not TOPIC_CONSTRUCT_OUTPUT_PARSER:
        TOPIC_CONSTRUCT_OUTPUT_PARSER = JsonOutputParser(pydantic_object=Topic)
    return TOPIC_CONSTRUCT_OUTPUT_PARSER


def load_topic_construct_prompt_template() -> str | None:
    global TOPIC_CONSTRUCT_PROMPT_TEMPLATE

    if not TOPIC_CONSTRUCT_PROMPT_TEMPLATE:
        file_dir, file_name = TOPIC_CONSTRUCT_PROMPT_FILE_DATA['dir'], TOPIC_CONSTRUCT_PROMPT_FILE_DATA['filename']
        prompt_file_path = f"prompts/{file_dir}/{file_name}"
        with open(prompt_file_path) as file:
            TOPIC_CONSTRUCT_PROMPT_TEMPLATE = file.read()
    return TOPIC_CONSTRUCT_PROMPT_TEMPLATE


def load_topic_construct_prompt() -> PromptTemplate:
    global TOPIC_CONSTRUCT_PROMPT

    if not TOPIC_CONSTRUCT_PROMPT:
        TOPIC_CONSTRUCT_PROMPT = PromptTemplate(
            input_variables=['topic_modeling_output', 'context'],
            template=load_topic_construct_prompt_template(),
            template_format="jinja2",
            partial_variables={
                "format_instructions": load_topic_construct_output_parser().get_format_instructions()
            }
        )
    return TOPIC_CONSTRUCT_PROMPT


def load_topic_construct_chain() -> LLMChain:
    global TOPIC_CONSTRUCT_CHAIN

    if not TOPIC_CONSTRUCT_CHAIN:
        TOPIC_CONSTRUCT_CHAIN = (
                load_topic_construct_prompt() |
                load_reader_model() |
                load_topic_construct_output_parser()
        )
    return TOPIC_CONSTRUCT_CHAIN


def preprocess_data(documents: list[str], lang='english') -> list:
    lang_stopwords = stopwords.words(lang)
    return [
        [word for word in simple_preprocess(doc) if word not in lang_stopwords]
        for doc in documents
    ]


def generate_id2word_mapping(processed_texts: list[str]) -> Any:
    return corpora.Dictionary(processed_texts)


def generate_corpus(processed_texts: list[str], id2word: Any) -> Any:
    return [id2word.doc2bow(text) for text in processed_texts]


def train_lda_model(
        corpus: Any,
        num_topics: int,
        id2word: Any,
        passes: int = 10,
        alpha: str = 'auto',
        per_word_topics: bool = True
) -> Any:
    return LdaModel(
        corpus=corpus,
        num_topics=num_topics,
        id2word=id2word,
        passes=passes,
        alpha=alpha,
        per_word_topics=per_word_topics
    )


def eval_lda_model_on_coherence_score(
        lda_model: Any,
        processed_texts: list[str],
        id2word: Any,
        coherence: str = 'c_v'
) -> float:
    coherence_model_lda = CoherenceModel(
        model=lda_model,
        texts=processed_texts,
        dictionary=id2word,
        coherence=coherence
    )
    return coherence_model_lda.get_coherence()


def generate_topics(lda: LdaModel) -> list:
    extracted_topics = []
    topics = lda.print_topics()
    for topic in topics:
        extracted_topics.append(topic[1])
    return extracted_topics


def generate_meaningful_topic(lda_topic: str, context: str) -> dict:
    topic_construct_chain = load_topic_construct_chain()
    return topic_construct_chain.invoke({
        'topic_modeling_output': lda_topic,
        'context': context
    })
