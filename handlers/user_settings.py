from datetime import datetime

import pytz
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message
from pytz import UnknownTimeZoneError
from sqlalchemy import select

from db.models import User
from keyboards.common_keybaords import get_main_keyboard
import re


class SettingsForm(StatesGroup):
    timezone = State()
    alarm_time = State()


async def start_register_user(message: Message, state: FSMContext, session):
    await message.answer('бла бла бла. Введи свое местоположение в виде: America/New_York, вместо пробела знак "_"')
    await state.set_state(SettingsForm.timezone.state)


async def set_user_timezone(message: Message, state: FSMContext, session):
    user_input = message.text.strip()
    try:
        user_timezone = datetime.now(pytz.timezone(user_input))
    except UnknownTimeZoneError as err:
        await message.answer(
            'Твое местоположение не найдено :( Проверь правильно ли ты ввел свой город или введи свою столицу')
        return
    await state.update_data(timezone=user_timezone)
    await message.answer(f'Твое местоположение найдено: {user_timezone}. Теперь введем время подьема')

    # TODO тут надо выводить текущее дефолтное время сообщения
    # Сделать дивайдер времени - Пробел
    await message.answer('Введите время в 24h формате hh:mm')
    await state.set_state(SettingsForm.alarm_time.state)


async def set_user_alarm_time(message: Message, state: FSMContext, session):
    pattern = re.compile("^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")
    time = message.text.lower().strip()
    if not pattern.match(time):
        await message.answer('Время введено неверно ')
        return
    await state.update_data(default_time=time)
    data = await state.get_data()
    await message.answer(f"{data['default_time']}, {data['timezone']}")

    async with session() as s:
        query = await s.execute(select(User).filter_by(id=message.from_user.id))
        user = query.scalar()
        if not user:
            s.add(User(id=message.from_user.id, timezone=data['timezone']))
            await s.commit()

    await state.finish()
    await message.answer('Все молодец иди нахуй без негатива) ')


def register_handlers_settings(dp):
    dp.register_message_handler(start_register_user, commands='register', state="*")
    dp.register_message_handler(set_user_timezone, state=SettingsForm.timezone)
    dp.register_message_handler(set_user_alarm_time, state=SettingsForm.alarm_time)
