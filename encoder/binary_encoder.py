import logging
from typing import List
from encoder.encoder import Encoder
from unique_id import get_next_unique_id
from types_ import Email, BinaryEmailChunkHeader, EmailChunk

_logger = logging.Logger(__name__)

class BinaryEncoder(Encoder):
    MESSAGE_SEGMENT_INTERSTITIAL = 0b0 << 15
    MESSAGE_SEGMENT_TERMINAL = 0b1 << 15

    """
    Message format:
    Each message begins with a header chunk and then proceeds with message body chunks.

    Header chunk format:
    X YYYYYYY ZZZZZZZZ

    X: A bit indicating whether this is the beginning/end of a message. If it is, a 1 is present. Otherwise, a 0.
    Every message begins and ends with a chunk that has this value set to 1.
    Y: Seven bits indicating the unique identifier of this message. If multiple messages are received from an API
    in interleaved order, this can separate them.
    Z: Eight bits indicating the segment number of the message. Reconstruct the message by ordering these and checking
    for gaps.
    """


    def encode_email(self,
        email: Email,
    ) -> List[str]:
        """
        Given a message, encode into a series of UTF-8 chunks. Return the hex string representation
        of these chunks.
        """
        recipient = email.sender_or_recipient
        subject = email.subject
        message = email.message
        if "," in recipient:
            recipient = recipient.replace(",", "")
        if "," in subject:
            subject = subject.replace(",", "")

        message_as_hex = ",".join([recipient, subject, message]).encode().hex()
        chunks = []
        unique_id = get_next_unique_id()
        while message_as_hex:
            next_chunk = message_as_hex[0:268]
            chunks.append(
                self.encode_chunk_header(
                    BinaryEmailChunkHeader(
                        unique_id,
                        len(chunks),
                        len(chunks) == 0 or len(next_chunk) < 268,
                    )
                )
                + next_chunk
            )
            message_as_hex = message_as_hex[268:]
        return chunks
    def encode_chunk_header(self, header: BinaryEmailChunkHeader) -> str:
        return (
            (
                (
                    self.MESSAGE_SEGMENT_TERMINAL
                    if header.is_end
                    else self.MESSAGE_SEGMENT_INTERSTITIAL
                )
                + (header.unique_id << 8)
                + header.chunk_num
            )
            .to_bytes(2, byteorder="big")
            .hex()
            .rjust(4, "0")
        )

    def decode_chunk_header(self,header: str) -> BinaryEmailChunkHeader:
        control_bytes = bytes.fromhex(header)[0:2]
        return BinaryEmailChunkHeader(
            int(control_bytes[0]) & 0b1111111,
            int(control_bytes[1]),
            bool(int(control_bytes[0]) & 0b10000000),
        )


    def decode_email_chunk(self,chunk: str) -> EmailChunk:
        header = self.decode_chunk_header(chunk)
        if header.is_end and header.chunk_num == 0:
            email_chunks = bytes.fromhex(chunk[4:]).decode("UTF-8").split(",", 2)
            return EmailChunk(header, email_chunks[0], email_chunks[1], email_chunks[2])
        else:
            email_body = bytes.fromhex(chunk[4:]).decode("UTF-8")
            return EmailChunk(header, message=email_body)
