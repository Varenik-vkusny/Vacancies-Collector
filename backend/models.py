from sqlalchemy import String, Integer, Column, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, index=True)
    name = Column(String, index=True)

    keyword = relationship('Keywords', back_populates='user')

class Keywords(Base):
    __tablename__ = 'keywords'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='keyword')

class Jobs(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, index=True)

    description = Column(String, index=True)

    source = Column(String, index=True)

    url = Column(String, index=True, unique=True)