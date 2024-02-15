from db.config import Base

from sqlalchemy import Column, Integer, String, BigInteger, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=False, unique=True)
    alarm_time = Column(String, nullable=False)
    timezone = Column(String, nullable=True)
    tasks = relationship('Task', back_populates='user')


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship('User', back_populates='tasks')
    title = Column(String, default='', nullable=False)
    


async def init_database(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_database(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
