import pytest

from tests.storage.fake_storage import FakeStorage


@pytest.fixture
def fake_storage() -> FakeStorage:
    return FakeStorage()
