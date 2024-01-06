from aiogram.dispatcher import FSMContext
from aiogram.types import Message


async def get_all_user_tasks(message: Message, state: FSMContext):
    ...

def register_handlers_get_tasks(dp):
    dp.register_message_handler(get_all_user_tasks, commands="list", state="*", )
