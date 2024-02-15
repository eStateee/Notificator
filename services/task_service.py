from typing import List
from sqlalchemy import select
from db.models import Task


async def get_user_task_list(session, user_id) -> List[Task]:
    async with session() as session:
        sql = select(Task.title, Task.id).filter_by(user_id=user_id)
        user_tasks = await session.execute(sql)
        user_tasks = user_tasks.fetchall()
    return user_tasks


async def delete_task_by_id(task_id, session):
    async with session() as s:
        sql = select(Task).filter_by(id=task_id)
        query = await s.execute(sql)
        task_to_delete = query.scalar_one()
        await s.delete(task_to_delete)
        await s.commit()
