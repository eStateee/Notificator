import pytz
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message
from magic_filter import F
from pytz import UnknownTimeZoneError
from db.models import User
from keyboards.common_keybaords import get_main_keyboard, get_register_inline_keyboard
from services.user_service import get_user_by_id, update_user_alarm_time_by_id, check_user_input_time


class SettingsForm(StatesGroup):
    timezone = State()
    alarm_time = State()


class UpdateSettingForm(StatesGroup):
    check_user = State()


async def start_register_user(callback, state: FSMContext):
    await callback.message.answer(
        'Введи свое местоположение в виде: America/New_York, вместо пробела знак "_"')
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
    await message.answer(f'Твое местоположение найдено.')
    await message.answer('Теперь введи время для уведомления в 24h формате hh:mm')
    await state.set_state(SettingsForm.alarm_time.state)


async def set_user_alarm_time(message: Message, state: FSMContext, session, schedule):
    time = message.text.lower().strip()
    if not check_user_input_time(time=time):
        await message.answer('Время введено неверно ')
        return
    await state.update_data(alarm_time=time)
    data = await state.get_data()
    await message.answer(f"{data['alarm_time']}, {data['timezone']}")

    async with session() as s:
        s.add(User(id=message.from_user.id, timezone=data['timezone'], alarm_time=data['alarm_time']))
        await s.commit()
    schedule.set_user_settings(timezone=data['timezone'], user_id=message.from_user.id)
    schedule.setup_and_start_schedule(alarm_time=data['alarm_time'], message=message, session=session)
    await state.finish()
    await message.answer('Время уведомления было установлено успешно', reply_markup=get_main_keyboard())


async def start_update_user_alarm_time(message: Message, session, state: FSMContext):
    user = await get_user_by_id(user_id=message.from_user.id, session=session)
    if not user:
        await message.answer(f'Что бы обновить данные сначала пройдите регистрацию',
                             reply_markup=get_register_inline_keyboard())
    else:
        await message.answer("Введи новое время подъема: ")
        await state.set_state(UpdateSettingForm.check_user.state)


async def update_user_alarm_time(message: Message, session, schedule, state: FSMContext):
    time = message.text.lower().strip()
    if not check_user_input_time(time=time):
        await message.answer('Время введено неверно ')
        return
    await state.update_data(alarm_time=time)
    data = await state.get_data()
    await update_user_alarm_time_by_id(user_id=message.from_user.id, alarm_time=data['alarm_time'], session=session)
    user = await get_user_by_id(user_id=message.from_user.id, session=session)
    schedule.set_user_settings(timezone=user.timezone, user_id=user.id)
    schedule.setup_and_start_schedule(alarm_time=user.alarm_time, session=session, message=message)
    schedule.update_user_schedule(data['alarm_time'])
    await message.answer('Время успешно изменено')
    await state.finish()


def register_handlers_settings(dp):
    dp.register_message_handler(set_user_timezone, state=SettingsForm.timezone)
    dp.register_message_handler(set_user_alarm_time, state=SettingsForm.alarm_time)
    dp.register_callback_query_handler(start_register_user, F.data == 'register')
    dp.register_message_handler(start_update_user_alarm_time, commands='update', state='*')
    dp.register_message_handler(update_user_alarm_time, state=UpdateSettingForm.check_user)
