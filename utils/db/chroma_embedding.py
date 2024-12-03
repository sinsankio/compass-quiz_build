import uuid
from typing import Any

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from configs.db.chroma_embedding import (
    CHROMA_DB_PATH,
    CHROMA_COLLECTION_NAME,
    CHROMA_SENTENCE_TRANSFORMER_MODEL_NAME
)
from utils.db.template import DB


class ChromaEmbedding(DB):
    def __init__(self, db_path: str = CHROMA_DB_PATH, collection_name: str = CHROMA_COLLECTION_NAME):
        self.__db_path = db_path
        self.__collection_name = collection_name
        self.__client: chromadb.api.ClientAPI | None = None
        self.__collection = chromadb.api.models.Collection = None

    def init_db_setup(self) -> None:
        self.__client = chromadb.PersistentClient(path=self.__db_path)
        self.__collection = self.__client.get_or_create_collection(
            name=self.__collection_name,
            metadata={'hnsw:space': 'cosine'},
            embedding_function=SentenceTransformerEmbeddingFunction(
                model_name=CHROMA_SENTENCE_TRANSFORMER_MODEL_NAME
            )
        )

    def insert(self, documents: list) -> None:
        self.__collection.add(
            documents=documents,
            ids=[str(uuid.uuid4()) for _ in range(len(documents))]
        )

    def search(self, queries: list, n_results: int) -> Any:
        return self.__collection.query(
            query_texts=queries,
            n_results=n_results
        )

    def update(self, documents: list, ids: list) -> None:
        self.__collection.update(
            documents=documents,
            ids=ids
        )

    def delete(self, ids: list, where: str) -> None:
        self.__collection.delete(
            ids=ids,
            where=where
        )
