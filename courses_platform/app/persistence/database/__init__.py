import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta


DEV_DB_PATH = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.getenv('DATABASE_URL', f'sqlite:////{DEV_DB_PATH}/test.db')

engine = create_engine(DB_PATH, convert_unicode=True)
Session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))

Base: DeclarativeMeta = declarative_base()
Base.query = Session.query_property()


@contextmanager
def session():
    sess = Session()

    try:
        yield sess
        sess.commit()
    except Exception:
        sess.rollback()
        raise
    finally:
        Session.remove()


from app.persistence.database.user.user_model import User  # noqa: E402, F401
from app.persistence.database.course.course_model import Course  # noqa: E402, F401
from app.persistence.database.enrollment_table import enrollment  # noqa: E402, F401
