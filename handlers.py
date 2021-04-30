import asyncio

from aiogram.utils.exceptions import PhotoDimensions
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove
from multiprocessing import Process
from selenium.common.exceptions import InvalidArgumentException

from main import dp, bot
from logging_seting import logger
from keyboards import (next_button,
                       screenshot_button
                       )
from FSM import SiteStates
from  screenshot import Browser


custom_name = None

@dp.message_handler(commands=["start"])
async def start_bot(msg: types.Message):
    await msg.answer("Привет! Вас приветсвует SCREENSHOT_BOT. "
                     "Принцип моей работы прост -"
                     "Вы мне ссылку на сайт я Вам скриншот сайта",
                     reply_markup=next_button)
    
    
# вводим url
@dp.message_handler(Text(equals="Начать"))
async def write_url(msg: types.Message):
    await msg.answer("Введите URL Вашего сайта:",
                     reply_markup=ReplyKeyboardRemove())

    await SiteStates.write_site.set()  # FSM.py
    
    
# вводим имя
@dp.message_handler(state=SiteStates.write_site)
async def write_name(msg: types.Message, state: FSMContext):
    await msg.answer("Теперь придумайте краткое название, "
                     "Оно будет использоваться названии скриншота")

    await state.update_data(
        {"url": msg.text}
    )
    await SiteStates.write_name.set()  # FSM.py


# сохраняем url и имя
@dp.message_handler(state=SiteStates.write_name)
async def save_name_and_url(msg: types.Message, state: FSMContext):
    global custom_name
    await state.update_data(
        {"name": msg.text}
    )
    screenshot_detail = await state.get_data()
    await state.finish()
    await msg.answer("Отлично! Вот данные, которые вы ввели:\n\n"
                     f"Имя: {screenshot_detail['name']}\n\n"
                     f"Url: {screenshot_detail['url']}\n",
                     reply_markup=ReplyKeyboardRemove())
    await msg.answer("Подождите делаем скриншот!")
    url, name = screenshot_detail['url'], screenshot_detail['name']
    logger.info(msg.chat.id)
    browser = Browser(url, name)
    try:
        browser.get_sreenshot()
    except InvalidArgumentException:
        await msg.answer("Упс похоже Вы ввели неправильный адресс!",
                         reply_markup=next_button)
    else:
        custom_name = name
        await msg.answer("Ваш скриншот готов:\n",
                         reply_markup=screenshot_button)
    

# отсылаем полученый скриншот
@dp.message_handler(Text(equals="Получить скриншот"))
async def screenshot_or_history(msg: types.Message):
    await msg.answer("Подождите:")
    global custom_name
    await types.ChatActions.upload_photo()
    media = types.MediaGroup()
    media.attach_document(types.InputFile(f'./media/{custom_name}.png'), f'{custom_name}')        
    await msg.reply_media_group(media=media)
    await msg.answer("Выберите:",
                     reply_markup=next_button)
    
    