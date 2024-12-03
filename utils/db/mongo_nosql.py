from typing import Any

from pymongo import MongoClient

from configs.db.mongo_nosql import *
from utils.db.template import DB


class MongoNoSQL(DB):
    def __init__(
            self,
            host: str = None,
            port: int = None
    ):
        self.__client: MongoClient | None = None
        self.__db: Any | None = None
        if not host:
            self.__host = MONGO_CLIENT_HOST_URI
        else:
            self.__host = host
        if not port:
            self.__port = MONGO_CLIENT_PORT
        else:
            self.__port = port

    def init_db_setup(self) -> None:
        self.__client = MongoClient(self.__host, self.__port)
        self.__db = self.__client[MONGO_DB_NAME]

    def insert(self, collection_name: str, data: dict) -> Any:
        collection = self.__db[collection_name]
        return collection.insert_one(data).inserted_id

    def search(self, collection_name: str, query: dict) -> dict:
        collection = self.__db[collection_name]
        return collection.find_one(query)

    def search_all(self, collection_name: str, query: dict) -> list[dict]:
        collection = self.__db[collection_name]
        return collection.find(query)

    def update(self, collection_name: str, query: dict, new_vals: dict) -> Any:
        collection = self.__db[collection_name]
        return collection.update_one(query, {'$set': new_vals})

    def delete(self, collection_name: str, query: dict) -> Any:
        collection = self.__db[collection_name]
        return collection.delete_one(query)

    def close(self) -> None:
        self.__client.close()
