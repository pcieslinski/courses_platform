from sqlalchemy import Column, String

from app.persistence.database import Base


class User(Base):
    __tablename__ = 'user'
    
    id = Column(String(36),
                nullable=False,
                primary_key=True)
    email = Column(String(72),
                   nullable=False,
                   unique=True,
                   index=True)

    def __repr__(self) -> str:
        return f'<User (id: {self.id}, email: {self.email})>'
