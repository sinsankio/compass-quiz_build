from abc import ABC, abstractmethod


class KnowledgeService(ABC):
    @abstractmethod
    def create_knowledge_base(self, **kwargs):
        pass

    @abstractmethod
    def get_knowledge_base(self, **kwargs):
        pass

    @abstractmethod
    def update_knowledge_base(self, **kwargs):
        pass

    @abstractmethod
    def delete_knowledge_base(self, **kwargs):
        pass
