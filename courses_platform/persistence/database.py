import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


db_path = os.path.abspath(os.path.dirname(__file__))

engine = create_engine(f'sqlite:////{db_path}/test.db', convert_unicode=True)
Session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))

Base = declarative_base()
Base.query = Session.query_property()


def init_db():
    from courses_platform.persistance.repositories.user_model import User

    Base.metadata.create_all(bind=engine)
