from dataclasses import dataclass
from typing import List, Optional, Union



@dataclass
class BinaryEmailChunkHeader:
    unique_id: int
    chunk_num: int
    is_end: bool

@dataclass
class DefaultEmailChunkHeader:
    email_part: int
    total_parts: int

@dataclass
class EmailChunk:
    header: Union[BinaryEmailChunkHeader,DefaultEmailChunkHeader] #This is wild but helpful for backwards compatibility
    sender_or_recipient: Optional[str]
    subject: Optional[str]
    message: str

@dataclass
class Email:
    sender_or_recipient: str
    subject: str
    message: str