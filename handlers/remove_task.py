from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message
from services.task_service import get_user_task_list, delete_task_by_id


class RemoveTaskGroup(StatesGroup):
    task_chosen = State()


async def start_remove_task(message: Message, state: FSMContext, session):
    await message.answer('Что бы удалить задачу, тебе надо написать ее номер в списке твоих задач')
    user_tasks = await get_user_task_list(user_id=message.from_user.id, session=session)
    await message.answer('Ваши задачи:')
    for i in user_tasks:
        await message.answer(f'Номер: {i.id}\nНазвание: {i.title}\n\n')
    await state.set_state(RemoveTaskGroup.task_chosen.state)


async def task_to_delete_chosen(message: Message, state: FSMContext, session):
    task_id = message.text.lower().strip()
    await delete_task_by_id(task_id=task_id, session=session)
    await message.answer('Задача успешно удалена')
    await state.finish()


def register_handlers_remove_tasks(dp):
    dp.register_message_handler(start_remove_task, commands='remove', state="*")
    dp.register_message_handler(task_to_delete_chosen, state=RemoveTaskGroup.task_chosen)
