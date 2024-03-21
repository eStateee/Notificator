from aiogram.types import Message

from services.task_service import get_user_task_list


async def display_scheduled_tasks(message, session, job_id, bot):
    user_tasks = await get_user_task_list(user_id=job_id, session=session)
    await bot.send_message(chat_id=job_id, text='Ваши задачи:')
    response = ''
    for i in user_tasks:
        response += f'{i.title}\n\n'
    await bot.send_message(chat_id=job_id, text=response)


async def display_all_user_tasks(message: Message, session):
    user_tasks = await get_user_task_list(user_id=message.from_user.id, session=session)
    await message.answer('Ваши задачи:')
    response = ''
    for i in user_tasks:
        response += f'{i.title}\n\n'
    await message.answer(response)


def register_handlers_get_tasks(dp):
    dp.register_message_handler(display_all_user_tasks, commands="list", state="*", )
