from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy_utils import create_database, database_exists, drop_database

from models import Base, Enemy, User
from tests.sample_data import test_enemy, test_enemy_2, test_enemy_3

TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/TEST"
TEST_DATABASE_URL_ASYNC = TEST_DATABASE_URL.replace(
    "postgresql://",
    "postgresql+asyncpg://",
    1,
)

test_engine = create_engine(TEST_DATABASE_URL)

test_async_engine = create_async_engine(
    TEST_DATABASE_URL_ASYNC, echo=False, poolclass=NullPool
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)

AsyncSessionLocal = async_sessionmaker(
    bind=test_async_engine,
    expire_on_commit=False,
)

database_initialized = False


def initialize_test_database():
    global database_initialized
    if database_initialized:
        return

    if database_exists(TEST_DATABASE_URL):
        drop_database(TEST_DATABASE_URL)
    create_database(TEST_DATABASE_URL)
    Base.metadata.create_all(bind=test_engine)

    with SessionLocal() as session:
        TestDatabase(session=session).populate_test_database()

    database_initialized = True


async def dispose_test_engines():
    await test_async_engine.dispose()
    test_engine.dispose()


class TestDatabase:
    def __init__(self, session: Session):
        self.session = session

    def populate_test_database(self):
        # Create a test user
        test_user = User(username="testuser", hashed_password="hashedpassword")
        self.session.add(test_user)

        # Create all enemies
        enemies = [
            Enemy(**test_enemy),
            Enemy(**test_enemy_2),
            Enemy(**test_enemy_3),
        ]

        self.session.add_all(enemies)
        self.session.commit()


def reset_test_database_state():
    with SessionLocal() as session:
        session.execute(
            text(
                "TRUNCATE TABLE encounters, characters, enemies, users "
                "RESTART IDENTITY CASCADE"
            )
        )
        TestDatabase(session=session).populate_test_database()


async def override_get_db():
    initialize_test_database()
    async with AsyncSessionLocal() as db:
        yield db
