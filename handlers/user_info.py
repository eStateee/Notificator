from services.user_service import get_user_by_id


async def user_info(message, session):
    user = await get_user_by_id(user_id=message.from_user.id, session=session)

    is_active_msg = lambda x: 'Работают' if x else 'Не активны'

    await message.answer(
        f"Привет {message.from_user.first_name}\nВаши уведомления: {is_active_msg(user.is_active)}\n"
        f"Ваше время уведомления: {user.alarm_time}")


def register_handlers_user_info(dp):
    dp.register_message_handler(user_info, commands='me', state='*')
