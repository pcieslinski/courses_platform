import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


DEV_DB_PATH = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.getenv('DATABASE_URL', f'sqlite:////{DEV_DB_PATH}/test.db')

engine = create_engine(DB_PATH, convert_unicode=True)
Session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))


@contextmanager
def session():
    sess = Session()

    try:
        yield sess
        sess.commit()
    except Exception:
        sess.rollback()
        raise
