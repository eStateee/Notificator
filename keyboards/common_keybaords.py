from aiogram import types
from aiogram.types import KeyboardButton

from config import COMMANDS


def get_main_keyboard():
    main_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,
                                              input_field_placeholder="Что будем делать?)")
    btn_list = []
    for i in COMMANDS:
        btn_list.append(KeyboardButton(f'/{i[0]}'))
    main_keyboard.row(*btn_list)
    return main_keyboard


def get_register_inline_keyboard():
    register_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True).row(
        KeyboardButton('/register'))
    return register_keyboard
