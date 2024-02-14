from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message
from aiogram import Dispatcher

from db.models import Task


class TaskForm(StatesGroup):
    title = State()
    # TODO Надо добавить: Дату(Сегодня\Завтра - хот кей, или ввод даты вручную
    #                     Время(либо дефолт, либо ввод пользователя)


async def task_start(message: Message, state: FSMContext):
    await message.answer('Напиши названия для таски')
    await state.set_state(TaskForm.title.state)


async def task_finish(message: Message, state: FSMContext, session):
    await state.update_data(title=message.text.lower().strip())
    data = await state.get_data()
    await message.answer(f'Название таски - {data["title"]}')

    async with session() as session:
        session.add(Task(user_id=message.from_user.id, title=data['title']))
        await session.commit()
        await message.answer("Данные записаны ")
    await state.finish()


def register_handlers_task_add(dp: Dispatcher) -> None:
    dp.register_message_handler(task_start, commands='add', state="*")
    dp.register_message_handler(task_finish, state=TaskForm.title)
