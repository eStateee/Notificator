import logging

from aiogram import Bot, Dispatcher, types, executor

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.bot_command import BotCommand

from config import COMMANDS
from handlers.common import register_handlers_common
from handlers.add_task import register_handlers_task_add
from handlers.test import register_handlers_food

API_TOKEN = ""

# тестовая БД
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
    # регистрация обработчиков для команд
    register_handlers_common(dp)
    register_handlers_task_add(dp)
    register_handlers_food(dp)
    # установка команд в меню тг бота
    await set_commands(dp)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
