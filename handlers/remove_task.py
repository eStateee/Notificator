from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message
from sqlalchemy import select

from db.models import Task
from handlers.user_settings import start_register_user


class RemoveTaskGroup(StatesGroup):
    task_chosen = State()


async def start_remove_task(message: Message, state: FSMContext, session):
    await message.answer('Что бы удалить задачу, тебе надо написать ее номер в списке твоих задач')
    async with session() as session:
        sql = select(Task.title, Task.id).filter_by(user_id=message.from_user.id)
        user_tasks = await session.execute(sql)
        user_tasks = user_tasks.fetchall()
    await message.answer('Ваши таски:')
    for i in user_tasks:
        await message.answer(f'Номер: {i.id}\nНазвание: {i.title}\n\n')
    await state.set_state(RemoveTaskGroup.task_chosen.state)


async def task_to_delete_chosen(message: Message, state: FSMContext, session):
    task_id = message.text.lower().strip()

    async with session() as s:
        sql = select(Task).filter_by(id=task_id)
        query = await s.execute(sql)
        task_to_delete = query.scalar_one()
        await s.delete(task_to_delete)
        await s.commit()
    await message.answer('Задача успешно удалена')
    await state.finish()


def register_handlers_remove_tasks(dp):
    dp.register_message_handler(start_remove_task, commands='remove', state="*")
    dp.register_message_handler(task_to_delete_chosen, state=RemoveTaskGroup.task_chosen)
