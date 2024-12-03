from abc import ABC, abstractmethod


class ExportService(ABC):
    @abstractmethod
    def generate_export(self, *args):
        pass
