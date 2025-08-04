from sqlalchemy import String, Integer, Boolean, Column, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, index=True)
    name = Column(String, index=True)
    is_active = Column(Boolean, index=True, default=True)

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

    title = Column(String, index=True)

    description = Column(String, index=True)

    price = Column(String, index=True)

    source = Column(String, index=True)

    additionally = Column(String, index=True)

    job_hash = Column(String, index=True)