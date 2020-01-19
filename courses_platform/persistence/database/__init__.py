import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_PATH = os.path.abspath(os.path.dirname(__file__))

engine = create_engine(f'sqlite:////{DB_PATH}/test.db', convert_unicode=True)
Session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))

Base = declarative_base()
Base.query = Session.query_property()


@contextmanager
def session() -> Session:
    sess = Session()

    try:
        yield sess
        sess.commit()
    except:
        sess.rollback()
        raise
    finally:
        Session.remove()


from courses_platform.persistence.database.user import User
from courses_platform.persistence.database.course import Course
from courses_platform.persistence.database.enrollment_table import enrollment


def init_db():
    from courses_platform.persistence.database.user import User
    from courses_platform.persistence.database.course import Course
    from courses_platform.persistence.database.enrollment_table import enrollment

    Base.metadata.create_all(bind=engine)
