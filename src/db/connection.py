import os
from contextlib import asynccontextmanager
from pathlib import Path

import alembic.command
import alembic.config
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

load_dotenv()


def get_url():
    dialect = 'postgresql'
    driver = 'asyncpg'
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '5432')
    dbname = os.getenv('DB_NAME', 'aima_status')
    username = os.getenv('DB_USERNAME', 'aima_status')
    password = os.getenv('DB_PASSWORD')

    scheme = f'{dialect}+{driver}'
    authority = f'{username}:{password}@{host}:{port}'
    return f'{scheme}://{authority}/{dbname}'


# if os.getenv('ENV') != 'TEST':
SESSION_MAKER = async_sessionmaker(bind=create_async_engine(get_url()))


def migrate_in_memory(revision: str = "head", root_directory: str = None):
    root_directory = Path(root_directory).parent
    config = alembic.config.Config(root_directory.joinpath('alembic.ini').__str__())
    config.set_main_option('script_location', root_directory.joinpath('alembic').__str__())

    alembic.command.upgrade(config, revision)


@asynccontextmanager
async def get_session():
    try:
        async_session = SESSION_MAKER
        async with async_session() as session:
            yield session
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()
