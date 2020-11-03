import pytest

from hash_api import HashApi


@pytest.fixture(scope="session")
def hash_api():
    return HashApi()
