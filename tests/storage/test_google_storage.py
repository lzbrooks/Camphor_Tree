import pytest

from storage import GoogleCloudStorage


@pytest.mark.integration
def test_read_and_write():
    storage = GoogleCloudStorage("camphor-tree-development")
    if storage.exists("test.txt"):
        storage.delete_file("test.txt")
    storage.write_file("test.txt", "Hello World")
    assert True == storage.exists("test.txt")
    assert "Hello World" == storage.read_file("test.txt")
    storage.delete_file("test.txt")
