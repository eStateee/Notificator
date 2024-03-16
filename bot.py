import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.bot_command import BotCommand
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


from handlers.common import register_handlers_common

from handlers.add_task import register_handlers_task_add
from handlers.get_tasks import register_handlers_get_tasks
from handlers.remove_task import register_handlers_remove_tasks
from handlers.user_settings import register_handlers_settings

from config import COMMANDS

from db.models import init_database, drop_database
from middlewares.db import DbSessionMiddleware
from middlewares.bot import BotMiddleware


load_dotenv()
API_TOKEN = os.getenv("TOKEN")

storage = MemoryStorage()

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
logger = logging.getLogger(__name__)

# Регистрация команд для отображения в меню телеграмма
async def set_commands(dp):
    commands = []
    for i in COMMANDS:
        commands.append(BotCommand(command=f'/{i[0]}', description=i[1]))
    await dp.bot.set_my_commands(commands)


# Ф-ция при запуске бота
async def on_startup(dp):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    engine = create_async_engine(url=os.getenv('DB_URL'), echo=True)
    # TODO тут для теста каждый раз дропаются все таблицы
    # await drop_database(engine)
    await init_database(engine)

    async_session = async_sessionmaker(
        engine, expire_on_commit=False,
    )

    dp.middleware.setup(DbSessionMiddleware(session_pool=async_session))
    dp.middleware.setup(BotMiddleware(bot=bot))

    # регистрация обработчиков
    register_handlers_common(dp)
    register_handlers_task_add(dp)
    register_handlers_settings(dp)
    register_handlers_get_tasks(dp)
    register_handlers_remove_tasks(dp)
    # установка команд в меню тг бота
    await set_commands(dp)



if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
