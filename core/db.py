from contextlib import contextmanager
from functools import wraps
from typing import Type

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session as RawSession, sessionmaker

from core import settings


engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)
Model = declarative_base(bind=engine)
Session: Type[RawSession] = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def session_wrapper(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        with session_scope() as session:
            return f(*args, **kwargs, session=session)

    return wrapper
