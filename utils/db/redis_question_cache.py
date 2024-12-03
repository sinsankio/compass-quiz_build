from typing import Any

import redis

from configs.db.redis_question_cache import *
from utils.db.template import DB


class RedisQuestionCache(DB):
    def __init__(self, host: str = None, port: str = None, password: str = None):
        self.__client: redis.Redis | None = None
        if not host:
            self.__host = REDIS_CLIENT_HOST_URI
        else:
            self.__host = host
        if not port:
            self.__port = REDIS_CLIENT_PORT
        else:
            self.__port = port
        if not password:
            self.__password = REDIS_CLIENT_PASSWORD
        else:
            self.__password = password

    def init_db_setup(self) -> None:
        self.__client = redis.Redis(
            host=self.__host,
            port=self.__port,
            password=self.__password
        )

    def insert(self, name: str, data: str | int | float | bool) -> None:
        self.__client.set(name, data)

    def search(self, name: str) -> Any:
        return self.__client.get(name).decode('utf-8')

    def update(self, name: str, data: str | int | float | bool) -> None:
        self.__client.set(name, data, xx=True)

    def delete(self, name: str) -> None:
        self.__client.delete(name)
