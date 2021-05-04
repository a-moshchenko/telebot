from typing import List
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

next_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Сделать скриншот")
        ],
        [
            KeyboardButton("История скриншотов")
        ]
    ],
    resize_keyboard=True
)


def get_button_list(lst: List):
    """ функция принимает на вход список имен и возвращает набор
    кнопок с этими именами для отображения в боте"""
    my_buttons = ReplyKeyboardMarkup(
       keyboard=[
           [
            KeyboardButton(f"{i}")
           ] for i in lst
       ]
    )
    my_buttons.add("Ok")

    return my_buttons
