from encoder.default_encoder import DefaultEncoder
from types_ import DefaultEmailChunkHeader, Email, EmailChunk
from typing import List
from unittest.mock import patch
import pytest


@pytest.mark.parametrize(
    "from_,subject,message,expected",
    [
        (
            "tester@gmail.com",
            "test subject",
            "test message",
            ["312c74657374207375626a6563742028312f31292c74657374206d657373616765"],
        ),
        (
            "tester@gmail.com",
            "test subject",
            "test message 2 that is veeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeery long",
            [
                "312c74657374207375626a6563742028312f32292c74657374206d65737361676520322074686174206973207665656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565657279206c6f6e",
                "312c74657374207375626a6563742028322f32292c67",
            ],
        ),
    ],
)
def test__encode_email(from_: str, subject: str, message: str, expected: List[str]):
    with patch(
        "cloud_loop_api.Config.get_whitelist", return_value={"1": "tester@gmail.com"}
    ):
        email = Email(
            sender_or_recipient=from_,
            subject=subject,
            message=message,
        )
        encoded = DefaultEncoder().encode_email(email)
        assert encoded == expected

@pytest.mark.parametrize(
    "chunk,expected",
    [
        (
            "312c74657374207375626a6563742028312f31292c74657374206d657373616765",
            EmailChunk(
                DefaultEmailChunkHeader(
                    1,
                    1
                ),
                "1",
                "test subject (1/1)",
                "test message"
            ),
        ),
        (
            "312c74657374207375626a6563742028312f32292c74657374206d65737361676520322074686174206973207665656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565656565657279206c6f6e",
            EmailChunk(
                DefaultEmailChunkHeader(
                    1,
                    2
                ),
                "1",
                "test subject (1/2)",
                "test message 2 that is veeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeery lon"
            ),
        ),
        (
            "312c74657374207375626a6563742028322f32292c67",
            EmailChunk(
                DefaultEmailChunkHeader(
                    2,
                    2
                ),
                "1",
                "test subject (2/2)",
                "g"
            ),
        )
    ],
)
def test__decode_email(chunk: str, expected: EmailChunk):
    assert DefaultEncoder().decode_email_chunk(chunk) == expected