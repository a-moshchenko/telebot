from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

next_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Начать")
        ]
    ],
    resize_keyboard=True
)


screenshot_button = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Получить скриншот")
        ]
    ],
    resize_keyboard=True
)

