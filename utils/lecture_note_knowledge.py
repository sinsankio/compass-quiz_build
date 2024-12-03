import os
from typing import Any, Optional

from dotenv import dotenv_values
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
from ragatouille import RAGPretrainedModel

from configs.lecture_note_knowledge import *

TEXT_SPLITTER: RecursiveCharacterTextSplitter | None = None
EMBEDDING_MODEL: NVIDIAEmbeddings | None = None


def load_text_splitter(chunk_size: int = CHUNK_SIZE) -> Any:
    global TEXT_SPLITTER

    if not TEXT_SPLITTER:
        TEXT_SPLITTER = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=int((1 / 10) * chunk_size),
            add_start_index=True,
            strip_whitespace=True,
            separators=SEPARATORS
        )
    return TEXT_SPLITTER


def load_nvidia_api_key() -> None:
    if not "NVIDIA_API_KEY" in os.environ:
        secrets = dotenv_values('secrets.env')
        os.environ['NVIDIA_API_KEY'] = secrets.get('NVIDIA_API_KEY')


def process_docs(lecture_page_docs: list[Document]) -> list[Document]:
    processed_docs = []
    seen_doc_contents = []
    for doc in lecture_page_docs:
        split_texts = load_text_splitter().split_text(doc.page_content)
        for text in split_texts:
            if text not in seen_doc_contents:
                split_doc = Document(page_content=text, metadata={
                    'source': f"uri: {doc.metadata['source']}, page: {doc.metadata['page']}"
                })
                processed_docs.append(split_doc)
                seen_doc_contents.append(text)
    return processed_docs


def load_embedding_model(embedding_model_name: str = EMBEDDING_MODEL_NAME, chunk_size: int = CHUNK_SIZE) -> Any:
    global EMBEDDING_MODEL

    if not EMBEDDING_MODEL:
        load_nvidia_api_key()
        EMBEDDING_MODEL = NVIDIAEmbeddings(
            model=embedding_model_name,
            max_length=chunk_size
        )
    return EMBEDDING_MODEL


def generate_knowledge_vector_db(docs_processed: list[Document]) -> Any:
    return FAISS.from_documents(
        docs_processed,
        embedding=load_embedding_model()
    )


def extract_topic_knowledge(
        knowledge_vector_db: Any,
        topic: str,
        num_docs: int = 5,
        reranker: Optional[RAGPretrainedModel] = None
) -> Any | None:
    if knowledge_vector_db:
        relevant_docs = knowledge_vector_db.similarity_search(query=topic, k=num_docs)
        relevant_docs = [doc.page_content for doc in relevant_docs]
        if reranker:
            relevant_docs = reranker.rerank(topic, relevant_docs, k=num_docs)
            relevant_docs = [doc['content'] for doc in relevant_docs]
        return relevant_docs[:num_docs]
