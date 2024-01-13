from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.common_keybaords import get_register_inline_keyboard


async def start(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(f'Очень угарное приветствие реяльно). Но тебе надо пройти регистрацию', reply_markup=get_register_inline_keyboard())


async def cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=ReplyKeyboardRemove())


# общая ф-ция для регистрации всех common обработчиков
def register_handlers_common(dp):
    dp.register_message_handler(start, commands="start", state="*", )
    dp.register_message_handler(cancel, commands="cancel", state="*")
