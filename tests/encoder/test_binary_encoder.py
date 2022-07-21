from typing import List
from unittest.mock import patch
from encoder.binary_encoder import BinaryEncoder
import pytest

from types_ import Email, BinaryEmailChunkHeader, EmailChunk


@pytest.mark.parametrize(
    "header,expected",
    [
        (BinaryEmailChunkHeader(0, 0, False), "0000"),
        (
            BinaryEmailChunkHeader(6, 14, False),
            0b0000011000001110.to_bytes(2, byteorder="big").hex(),
        ),
        (
            BinaryEmailChunkHeader(3, 14, True),
            0b1000001100001110.to_bytes(2, byteorder="big").hex(),
        ),
    ],
)
def test__encode_chunk_header(
    header: BinaryEmailChunkHeader,
    expected: str,
):
    assert BinaryEncoder().encode_chunk_header(header) == expected


@pytest.mark.parametrize(
    "header,expected",
    [
        ("0000", BinaryEmailChunkHeader(0, 0, False)),
        (
            0b0000011000001110.to_bytes(2, byteorder="big").hex(),
            BinaryEmailChunkHeader(6, 14, False),
        ),
        (
            0b1000001100001110.to_bytes(2, byteorder="big").hex(),
            BinaryEmailChunkHeader(3, 14, True),
        ),
    ],
)
def test__decode_chunk_header(header: str, expected: BinaryEmailChunkHeader):
    assert BinaryEncoder().decode_chunk_header(header) == expected


@pytest.mark.parametrize(
    "email,expected",
    [
        (
            Email("4", "hello", "This is a small test email"),
            [
                "8100342c68656c6c6f2c54686973206973206120736d616c6c207465737420656d61696c"
            ],
        ),
        (
            Email(
                "4",
                "hello",
                (
                    "This is a large test email. It should have enough text in it to exceed the size of a single chunk."
                    "This will demonstrate how a message can span multiple chunks, and hopefully produce the right headers for each segment. "
                    "At this point, I'm just taking up sapce to try to produce a third chunk. Each of these lines is probably only half "
                    "a chunk, because I'm not using any special characters. Well, maybe I should: 写汉字吧。每个字是四位。"
                ),
            ),
            [
                "8100342c68656c6c6f2c546869732069732061206c61726765207465737420656d61696c2e2049742073686f756c64206861766520656e6f756768207465787420696e20697420746f20657863656564207468652073697a65206f6620612073696e676c65206368756e6b2e546869732077696c6c2064656d6f6e73747261746520686f77206120",
                "01016d6573736167652063616e207370616e206d756c7469706c65206368756e6b732c20616e6420686f706566756c6c792070726f6475636520746865207269676874206865616465727320666f722065616368207365676d656e742e204174207468697320706f696e742c2049276d206a7573742074616b696e6720757020736170636520746f",
                "01022074727920746f2070726f647563652061207468697264206368756e6b2e2045616368206f66207468657365206c696e65732069732070726f6261626c79206f6e6c792068616c662061206368756e6b2c20626563617573652049276d206e6f74207573696e6720616e79207370656369616c20636861726163746572732e2057656c6c2c20",
                "81036d6179626520492073686f756c643a20e58699e6b189e5ad97e590a7e38082e6af8fe4b8aae5ad97e698afe59b9be4bd8de38082",
            ],
        ),
    ],
)
def test__encode_email(email: Email, expected: List[str]):
    with patch("encoder.binary_encoder.get_next_unique_id", return_value=1):
        assert BinaryEncoder().encode_email(email) == expected


@pytest.mark.parametrize(
    "chunk,expected",
    [
        (
            "8100342c68656c6c6f2c54686973206973206120736d616c6c207465737420656d61696c",
            EmailChunk(BinaryEmailChunkHeader(0,0,True), "4", "hello", "This is a small test email"),
        ),
        (
            "8100342c68656c6c6f2c546869732069732061206c61726765207465737420656d61696c2e2049742073686f756c64206861766520656e6f756768207465787420696e20697420746f20657863656564207468652073697a65206f6620612073696e676c65206368756e6b2e546869732077696c6c2064656d6f6e73747261746520686f77206120",
            EmailChunk(BinaryEmailChunkHeader(1,0,True), "4", "hello", "This is a large test email. It should have enough text in it to exceed the size of a single chunk."),
        ),
        (
            "01016d6573736167652063616e207370616e206d756c7469706c65206368756e6b732c20616e6420686f706566756c6c792070726f6475636520746865207269676874206865616465727320666f722065616368207365676d656e742e204174207468697320706f696e742c2049276d206a7573742074616b696e6720757020736170636520746f",
            EmailChunk(BinaryEmailChunkHeader(1,1,False), "4", "hello", "This will demonstrate how a message can span multiple chunks, and hopefully produce the right headers for each segment. "),
        ),
        (
            "01022074727920746f2070726f647563652061207468697264206368756e6b2e2045616368206f66207468657365206c696e65732069732070726f6261626c79206f6e6c792068616c662061206368756e6b2c20626563617573652049276d206e6f74207573696e6720616e79207370656369616c20636861726163746572732e2057656c6c2c20",
            EmailChunk(BinaryEmailChunkHeader(1,2,False), "4", "hello", "At this point, I'm just taking up sapce to try to produce a third chunk. Each of these lines is probably only half "),
        ),
        (
            "81036d6179626520492073686f756c643a20e58699e6b189e5ad97e590a7e38082e6af8fe4b8aae5ad97e698afe59b9be4bd8de38082",
            EmailChunk(BinaryEmailChunkHeader(1,3,True), "4", "hello", "a chunk, because I'm not using any special characters. Well, maybe I should: 写汉字吧。每个字是四位。"),
        ),
    ],
)
def decode_email_chunk(chunk: str, expected: EmailChunk):
    assert BinaryEncoder().decode_email_chunk(chunk) == expected
