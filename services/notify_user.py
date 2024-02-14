from sqlalchemy import select

from db.models import Task


async def notify(message, session):
    async with session() as session:
        sql = select(Task.title).filter_by(user_id=message.from_user.id)
        user_tasks = await session.execute(sql)
        user_tasks = user_tasks.fetchall()
    await message.answer('Ваши таски:')
    for i in user_tasks:
        await message.answer(f'Название: {i.title}\n')
