from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from sqlalchemy import select

from db.models import Task


async def get_all_user_tasks(message: Message, session):
    async with session() as session:
        sql = select(Task.title).filter_by(user_id=message.from_user.id)
        user_tasks = await session.execute(sql)
        user_tasks = user_tasks.fetchall()
    await message.answer('Ваши таски:')
    for i in user_tasks:
        await message.answer(f'Название: {i.title}\n\n')


def register_handlers_get_tasks(dp):
    dp.register_message_handler(get_all_user_tasks, commands="list", state="*", )
