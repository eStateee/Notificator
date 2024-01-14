
import pytz
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message
from magic_filter import F
from pytz import UnknownTimeZoneError
from db.models import User
from keyboards.common_keybaords import get_main_keyboard
import re
from services.schedule_services import setup_and_start_schedule


class SettingsForm(StatesGroup):
    timezone = State()
    alarm_time = State()


async def start_register_user(callback, state: FSMContext):
    await callback.message.answer(
        'бла бла бла. Введи свое местоположение в виде: America/New_York, вместо пробела знак "_"')
    await state.set_state(SettingsForm.timezone.state)


async def set_user_timezone(message: Message, state: FSMContext):
    user_input = message.text.strip()
    try:
        pytz.timezone(user_input)
    except UnknownTimeZoneError as err:
        await message.answer(
            'Твое местоположение не найдено :( Проверь правильно ли ты ввел свой город или введи свою столицу')
        return
    await state.update_data(timezone=user_input)
    await message.answer(f'Твое местоположение найдено. Теперь введем время уведомления')
    await message.answer('Введите время в 24h формате hh:mm')
    await state.set_state(SettingsForm.alarm_time.state)


async def set_user_alarm_time(message: Message, state: FSMContext, session):
    pattern = re.compile("^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")
    time = message.text.lower().strip()
    if not pattern.match(time):
        await message.answer('Время введено неверно ')
        return
    await state.update_data(alarm_time=time)
    data = await state.get_data()
    await message.answer(f"{data['alarm_time']}, {data['timezone']}")

    async with session() as s:
        s.add(User(id=message.from_user.id, timezone=data['timezone'], alarm_time=data['alarm_time']))
        await s.commit()
    setup_and_start_schedule(timezone=data['timezone'],alarm_time=data['alarm_time'], session=session, message=message)
    await state.finish()
    await message.answer('Все молодец иди нахуй без негатива) ', reply_markup=get_main_keyboard())


def register_handlers_settings(dp):
    dp.register_message_handler(set_user_timezone, state=SettingsForm.timezone)
    dp.register_message_handler(set_user_alarm_time, state=SettingsForm.alarm_time)
    dp.register_callback_query_handler(start_register_user, F.data == 'register')
