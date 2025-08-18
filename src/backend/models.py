from sqlalchemy import String, Integer, Boolean, Column, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, index=True)
    name = Column(String)

    keywords = relationship('Keywords', back_populates='user')

class Keywords(Base):
    __tablename__ = 'keywords'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='keywords')

class Jobs(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)

    description = Column(String)

    price = Column(String)

    source = Column(String)

    additionally = Column(String)

    job_hash = Column(String, index=True)