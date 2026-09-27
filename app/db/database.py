"""
VerifyKE database connection and session management.

This file creates the asynchronous connection between the application
and PostgreSQL using SQLAlchemy. It also provides database sessions
that routes and services will use to read and write data.
"""

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

# Create the SQLAlchemy database engine.
# The engine manages the underlying connection to PostgreSQL.

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
)

# Session factory for every time we need to interact with the DB
AsyncSessionLocal = async_sessionmaker(
    bind = engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    """
    Provide a database session to FastAPI routes.

    The session is opened when a request needs the database and
    automatically closed when the request is finished.
    """
    async with AsyncSessionLocal() as session:
        yield session