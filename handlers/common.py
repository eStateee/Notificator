from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.main_keybaord import get_main_keyboard
import re


async def start(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("Дарова епта бандиты !)))!№!№)", reply_markup=get_main_keyboard())


async def cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=ReplyKeyboardRemove())


# общая ф-ция для регистрации всех common обработчиков
def register_handlers_common(dp):
    dp.register_message_handler(start, commands="start", state="*")
    dp.register_message_handler(cancel, commands="cancel", state="*")
