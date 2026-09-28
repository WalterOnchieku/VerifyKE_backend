"""
Alembic configuration for VerifyKE.

This file connects Alembic to our SQLAlchemy models and
database configuration so that database migrations can
be generated and applied.
"""

from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from app.core.config import settings
from app.db.models import Base


# Alembic Config object.
config = context.config


# Configure Python logging using the alembic.ini settings.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Tell Alembic about our SQLAlchemy models.
#
# Alembic compares this metadata against the actual database
# to determine what changes need to be migrated.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations without creating a database connection.

    This generates SQL statements that can be reviewed
    or executed separately.
    """

    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named"
        },
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """
    Run migrations using an active database connection.
    """

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    Create an asynchronous database engine and
    run the migrations.
    """

    configuration = config.get_section(
        config.config_ini_section,
        {},
    )

    # Use our database URL from the application settings.
    configuration["sqlalchemy.url"] = settings.DATABASE_URL

    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:

        await connection.run_sync(
            do_run_migrations
        )

    await connectable.dispose()


def run_migrations_online() -> None:
    """
    Run migrations while connected to the database.
    """

    import asyncio

    asyncio.run(
        run_async_migrations()
    )


if context.is_offline_mode():

    run_migrations_offline()

else:

    run_migrations_online()