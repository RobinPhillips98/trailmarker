from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy_utils import create_database, database_exists, drop_database

from models import Base, Character, Enemy, User
from tests.sample_data import (
    test_enemy,
    test_enemy_2,
    test_enemy_3,
    test_player,
    test_player_2,
    test_player_3,
    test_player_4,
)

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


def build_character_kwargs(character_data: dict, user_id: int) -> dict:
    payload = character_data.copy()
    payload.pop("user_id", None)
    payload["user_id"] = user_id
    if "class" in payload:
        payload["class_"] = payload.pop("class")
    return payload


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
        # Flush first so we can link characters by user_id.
        self.session.flush()

        # Create all enemies
        enemies = [
            Enemy(**test_enemy),
            Enemy(**test_enemy_2),
            Enemy(**test_enemy_3),
        ]

        # Create all characters with the test user
        characters = [
            Character(**build_character_kwargs(test_player, test_user.id)),
            Character(**build_character_kwargs(test_player_2, test_user.id)),
            Character(**build_character_kwargs(test_player_3, test_user.id)),
            Character(**build_character_kwargs(test_player_4, test_user.id)),
        ]

        self.session.add_all(enemies + characters)
        self.session.commit()


async def override_get_db():
    initialize_test_database()
    async with AsyncSessionLocal() as db:
        yield db
