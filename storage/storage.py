from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def read_file(self, filename: str) -> str:
        ...

    @abstractmethod
    def write_file(self, filename: str, content: str):
        ...

    @abstractmethod
    def delete_file(self, filename: str):
        ...

    @abstractmethod
    def exists(self, filename: str) -> bool:
        ...
