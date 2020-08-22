import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


DEV_DB_PATH = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.getenv('DATABASE_URL', f'sqlite:////{DEV_DB_PATH}/test.db')

engine = create_engine(DB_PATH)
Session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)
