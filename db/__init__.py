"""
SQLAlchemy backend for storing contacts
"""
from contextlib import contextmanager

import sqlalchemy
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()


def configure_session(database_url):
    """
    Configures sessionmaker to have a database url.

    :param database_url: URL for SQLAlchemy
    """
    Session.configure(bind=sqlalchemy.create_engine(database_url))


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
