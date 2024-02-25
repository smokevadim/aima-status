import os
from contextlib import contextmanager
from pathlib import Path

import alembic.command
import alembic.config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SESSION_MAKER = None


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
SESSION_MAKER = sessionmaker(bind=create_engine(get_url()))


def migrate_in_memory(revision: str = "head", root_directory: str = None):
    root_directory = Path(root_directory).parent
    config = alembic.config.Config(root_directory.joinpath('alembic.ini').__str__())
    config.set_main_option('script_location', root_directory.joinpath('alembic').__str__())

    alembic.command.upgrade(config, revision)


@contextmanager
def transactional(session_maker=SESSION_MAKER):
    """Provide a transactional scope around a series of operations."""
    if session_maker is None:
        yield None
    else:
        session = session_maker()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
