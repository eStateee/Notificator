from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.main_keybaord import get_main_keyboard
import re

class SettingsForm(StatesGroup):
    default_time = State()

# CHANGE DEFAULT ALARM TIME
async def start_default_time(message: Message, state: FSMContext):
    # TODO тут надо выводить текущее дефолтное время сообщения
    # Сделать дивайдер времени - Пробел
    await message.answer('Введите время в 24h формате hh:mm')
    await state.set_state(SettingsForm.default_time.state)


async def set_default_time(message: Message, state: FSMContext):
    pattern = re.compile("^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")
    time = message.text.lower().strip()
    if not pattern.match(time):
        await message.answer('Время введено неверно ')
        return
    await state.update_data(defualt_time=time)
    data = await state.get_data()
    await message.answer(data['defualt_time'])
    await state.finish()


def register_handlers_settings(dp):
    dp.register_message_handler(start_default_time, commands='time', state="*")
    dp.register_message_handler(set_default_time, state=SettingsForm.default_time)
