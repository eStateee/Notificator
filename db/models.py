from db.config import Base

from sqlalchemy import Column, Integer, String, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=False, unique=True)
    # TODO убрать потом nullable и задавать default значение
    alarm_time = Column(DateTime(timezone=True), nullable=True)
    timezone = Column(String, nullable=True)
    tasks = relationship('Task', back_populates='user')

class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship('User',back_populates='tasks')
    title = Column(String, default='', nullable=False)
    description = Column(String, default='')
    # TODO добавить alarm_date (дата для уведомления)
    #  и alarm_time(default = User.alarm_time) -
    #  Если пользователь захочет для отдельной таски поставить свое время для аларма


async def init_database(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_database(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
