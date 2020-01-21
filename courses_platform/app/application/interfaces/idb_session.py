from typing import NewType
from sqlalchemy.orm import session


DbSession = NewType('DbSession', session)
