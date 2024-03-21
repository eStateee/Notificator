import re

from db.models import User
from sqlalchemy import select, update
from config import SCHEDULE_LIST


async def get_user_by_id(user_id, session) -> User:
    async with session() as s:
        query = await s.execute(select(User).filter_by(id=user_id))
        user = query.scalar()
    return user


async def update_user_alarm_time_by_id(session, alarm_time, user_id) -> None:
    async with session() as s:
        sql = update(User).where(User.id == user_id).values(alarm_time=alarm_time)
        await s.execute(sql)
        await s.commit()


def check_user_input_time(time):
    pattern = re.compile("^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")
    if not pattern.match(time):
        return False
    return True


async def get_all_users(session):
    async with session() as s:
        query = await s.execute(select(User.id, User.timezone, User.alarm_time, User.is_active))
        users = query.fetchall()
    return users


async def change_user_alarm_status(user_id, session):
    async with session() as s:
        query = await s.execute(select(User.is_active).where(User.id == user_id))
        current_user_is_active_status = query.scalar()
        opposite_is_active = not current_user_is_active_status
        await s.execute(update(User).where(User.id == user_id).values(is_active=opposite_is_active))
        await s.commit()

    user_schedule = SCHEDULE_LIST[user_id]
    if current_user_is_active_status:
        user_schedule.scheduler.pause()
    else:
        user_schedule.scheduler.resume()
    return opposite_is_active
