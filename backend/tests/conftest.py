import asyncio

import pytest
from sqlalchemy.orm.session import close_all_sessions
from sqlalchemy_utils import drop_database

from tests.utils import (
    TEST_DATABASE_URL,
    dispose_test_engines,
    initialize_test_database,
)


@pytest.fixture(scope="session", autouse=True)
def create_and_delete_database():
    initialize_test_database()
    yield
    close_all_sessions()
    asyncio.run(dispose_test_engines())
    drop_database(TEST_DATABASE_URL)
