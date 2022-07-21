import pytest
from storage.local_storage import LocalStorage


def test_read_and_write():
    storage = LocalStorage("testing")
    if storage.exists("test.txt"):
        storage.delete_file("test.txt")
    storage.write_file("test.txt", "Hello World")
    assert True == storage.exists("test.txt")
    assert "Hello World" == storage.read_file("test.txt")
    storage.delete_file("test.txt")


def test_bad_directory():
    with pytest.raises(ValueError):
        LocalStorage("tests/data/placeholder.txt")
