import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

load_dotenv()


# Get database URL from environment variable
database_url = os.getenv("DATABASE_URL")

# Convert URLs for both sync and async connections
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

# Create async URL
async_database_url = database_url.replace(
    "postgresql://", "postgresql+asyncpg://", 1
)

DATABASE_URL = async_database_url
DATABASE_URL_SYNC = database_url


# Create database engines
engine = create_async_engine(DATABASE_URL, echo=False)

# DB connection for sync operations (like populate.py)
engine_sync = create_engine(
    DATABASE_URL_SYNC,
    echo=False,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Create session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

SessionLocal = sessionmaker(
    bind=engine_sync, autocommit=False, autoflush=False
)


# Dependency to get the database session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
