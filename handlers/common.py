from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.common_keybaords import get_register_inline_keyboard
from services.user_service import get_user_by_id
from config import COMMANDS
from keyboards.common_keybaords import get_main_keyboard


async def start(message: Message, state: FSMContext, session):
    await state.finish()
    user = await get_user_by_id(user_id=message.from_user.id, session=session)
    if not user:
        await message.answer(f'Привет:)\nЭтот бот служит для напоминания тебе твоих важных и не очень дел.\n '
                             f'Что бы начать пользоваться ботом тебе необходимо пройти регистрацию',
                             reply_markup=get_register_inline_keyboard())
    else:
        cmds = ''
        for i in COMMANDS:
            cmds += f'/{i[0]} -- {i[1]}\n'
        await message.answer(f'И снова здравствуй!\nСписок команд:\n{cmds}', reply_markup=get_main_keyboard())


async def cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=ReplyKeyboardRemove())


# общая ф-ция для регистрации всех common обработчиков
def register_handlers_common(dp):
    dp.register_message_handler(start, commands="start", state="*", )
    dp.register_message_handler(cancel, commands="cancel", state="*")
