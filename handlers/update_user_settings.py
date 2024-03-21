from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message

from keyboards.common_keybaords import get_register_inline_keyboard
from services.user_service import get_user_by_id, update_user_alarm_time_by_id, check_user_input_time, \
    change_user_alarm_status

from config import SCHEDULE_LIST


class UpdateSettingForm(StatesGroup):
    check_user = State()


async def start_update_user_alarm_time(message: Message, session, state: FSMContext):
    user = await get_user_by_id(user_id=message.from_user.id, session=session)
    if not user:
        await message.answer(f'Что бы обновить данные сначала пройдите регистрацию',
                             reply_markup=get_register_inline_keyboard())
    else:
        await message.answer("Введи новое время подъема: ")
        await state.set_state(UpdateSettingForm.check_user.state)


async def update_user_alarm_time(message: Message, session, state: FSMContext):
    time = message.text.lower().strip()
    if not check_user_input_time(time=time):
        await message.answer('Время введено неверно ')
        return
    await state.update_data(alarm_time=time)
    data = await state.get_data()
    schedule = SCHEDULE_LIST[int(message.from_user.id)]
    schedule.update_user_schedule(data['alarm_time'])
    await update_user_alarm_time_by_id(user_id=message.from_user.id, alarm_time=data['alarm_time'], session=session)
    await message.answer('Время успешно изменено')
    await state.finish()


async def change_user_alarm_status_handler(message, session):
    updated_user_status = await change_user_alarm_status(user_id=message.from_user.id, session=session)
    if updated_user_status:
        await message.answer('Теперь ваши уведомления снова работают')
    else:
        await message.answer('Отправка вам уведомлений приостановлена')


def register_handlers_settings(dp):
    dp.register_message_handler(start_update_user_alarm_time, commands='update', state='*')
    dp.register_message_handler(update_user_alarm_time, state=UpdateSettingForm.check_user)
    dp.register_message_handler(change_user_alarm_status_handler, commands='change', state="*")
