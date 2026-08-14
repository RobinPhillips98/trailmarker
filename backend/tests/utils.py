from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy_utils import create_database, database_exists, drop_database

from api.auth_helpers import get_password_hash
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


def terminate_test_db_connections(db_url: str, db_name: str):
    admin_url = db_url.rsplit("/", 1)[0] + "/postgres"
    engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")
    try:
        with engine.connect() as conn:
            conn.execute(
                text(
                    """
                    SELECT pg_terminate_backend(pid)
                    FROM pg_stat_activity
                    WHERE datname = :db_name
                      AND pid <> pg_backend_pid()
                    """
                ),
                {"db_name": db_name},
            )
    finally:
        engine.dispose()


def initialize_test_database():
    global database_initialized
    if database_initialized:
        return

    terminate_test_db_connections(
        TEST_DATABASE_URL, TEST_DATABASE_URL.rsplit("/", 1)[-1]
    )
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
        # Create base test users used by the auth fixtures and reset logic.
        test_user = User(
            username="testuser",
            hashed_password=get_password_hash("testpassword"),
        )
        shared_test_user = User(
            username="shared_test_user",
            hashed_password=get_password_hash("testpassword"),
        )
        self.session.add_all([test_user, shared_test_user])

        # Create all enemies
        enemies = [
            Enemy(**test_enemy),
            Enemy(**test_enemy_2),
            Enemy(**test_enemy_3),
        ]

        self.session.add_all(enemies)
        self.session.commit()


async def override_get_db():
    db = AsyncSessionLocal()
    try:
        await db.begin()
        yield db
    finally:
        await db.rollback()
        await db.close()
