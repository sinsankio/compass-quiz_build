from abc import ABC, abstractmethod
from typing import Any


class DB(ABC):
    @abstractmethod
    def init_db_setup(self):
        pass

    @abstractmethod
    def insert(self, **kwargs):
        pass

    @abstractmethod
    def search(self, **kwargs):
        pass

    @abstractmethod
    def update(self, **kwargs):
        pass

    @abstractmethod
    def delete(self, **kwargs):
        pass
