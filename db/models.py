from db.config import Base

from sqlalchemy import Column, Integer, String, BigInteger


class Task(Base):
    __tablename__ = 'task'
    user_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    title = Column(String, default='', nullable=False)
    description = Column(String, default='')


async def init_database(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_database(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
