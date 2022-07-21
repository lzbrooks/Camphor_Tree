from abc import ABC, abstractmethod
from typing import List

from types_ import Email, EmailChunk


class Encoder(ABC):
    @abstractmethod
    def encode_email(
        email: Email,
    ) -> List[str]:
        ...
    
    @abstractmethod
    def decode_email_chunk(
        chunks: List[str]
    ) -> EmailChunk:
        ...
