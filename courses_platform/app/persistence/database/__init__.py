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


from app.persistence.database.user.user_model import User
from app.persistence.database.course.course_model import Course
from app.persistence.database.enrollment_table import enrollment


def init_db():
    from app.persistence.database.user.user_model import User
    from app.persistence.database.course.course_model import Course
    from app.persistence.database.enrollment_table import enrollment

    Base.metadata.create_all(bind=engine)