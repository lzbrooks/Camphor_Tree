import os
from unittest.mock import patch
from storage import Storage

from unique_id import get_next_unique_id


def test_get_next_unique_id(fake_storage: Storage):
    # Test that the fake ID generator wraps around
    with patch("storage.read_file", fake_storage.read_file), patch(
        "storage.write_file", fake_storage.write_file
    ):
        for n in range(0, 0b1111111):
            assert n == get_next_unique_id()
        assert 0 == get_next_unique_id()
