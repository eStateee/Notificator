from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from sqlalchemy import select
from db.models import User
from keyboards.common_keybaords import get_register_inline_keyboard
from services.schedule_services import setup_and_start_schedule


async def start(message: Message, state: FSMContext, session):
    await state.finish()
    async with session() as s:
        query = await s.execute(select(User).filter_by(id=message.from_user.id))
        user = query.scalar()
        if not user:
            await message.answer(f'Очень угарное приветствие реяльно). Но тебе надо пройти регистрацию',
                                 reply_markup=get_register_inline_keyboard())
        else:
            await message.answer('Ебать так ты зарегестрирован. Ну если не не работают уведомления щас починим')
            async with session() as s:
                query = await s.execute(select(User).filter_by(id=message.from_user.id))
                user = query.scalar()
                setup_and_start_schedule(timezone=user.timezone, alarm_time=user.alarm_time, session=session,
                                         message=message)


async def cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=ReplyKeyboardRemove())


# общая ф-ция для регистрации всех common обработчиков
def register_handlers_common(dp):
    dp.register_message_handler(start, commands="start", state="*", )
    dp.register_message_handler(cancel, commands="cancel", state="*")
