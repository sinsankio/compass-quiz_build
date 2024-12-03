from abc import ABC, abstractmethod


class QuestionService(ABC):
    @abstractmethod
    def construct(self, **kwargs):
        pass

    @abstractmethod
    def evaluate(self, **kwargs):
        pass

    @abstractmethod
    def backup(self, **kwargs):
        pass
