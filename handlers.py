from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove
from selenium.common.exceptions import InvalidArgumentException

from main import dp
from logging_seting import logger
from keyboards import next_button, get_button_list

from FSM import SiteStates
from screenshot import Browser
import database

show_screenshot = []
status = None


@dp.message_handler(commands=["start"])
async def start_bot(msg: types.Message):
    await msg.answer("Привет! Вас приветсвует SCREENSHOT_BOT. "
                     "Принцип моей работы прост -"
                     "Вы мне ссылку на сайт я Вам скриншот сайта",
                     reply_markup=next_button)


# вводим url
@dp.message_handler(Text(equals="Сделать скриншот"))
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


async def send_image(msg: types.Message, name: str):  # отправка документа
    await msg.answer("Подождите:")
    await types.ChatActions.upload_photo()
    media = types.MediaGroup()
    media.attach_document(types.InputFile(
        f'./media/{name}.png'),
        f'{name}'
    )
    await msg.reply_media_group(media=media)


# сохраняем url и имя
@dp.message_handler(state=SiteStates.write_name)
async def save_name_and_url(msg: types.Message, state: FSMContext):
    if msg.text  in [i['name'] for i in database.fetchall()]:
        await msg.answer(f"Имя {msg.text} занято придумайте другое")
        await SiteStates.write_name.set()  # FSM.py
    else:
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
        database.insert({'name': name, 'url': url})
        logger.info(msg.chat.id)
        browser = Browser(url, name)
        try:
            browser.get_sreenshot()
        except InvalidArgumentException:
            await msg.answer("Упс похоже Вы ввели неправильный адресс!",
                             reply_markup=next_button)
        else:
            await msg.answer("Ваш скриншот готов:\n")
            await send_image(msg, screenshot_detail['name'])
            await msg.answer("Выберите:",
                             reply_markup=next_button)


@dp.message_handler(Text(equals="История скриншотов"))  # выбираем скриншоты
async def history(msg: types.Message):
    global status
    all_screenshot = database.fetchall()
    all_names = [i['name'] for i in all_screenshot]
    status = True
    await msg.answer("Выберите скриншоты которые хотите посмотреть:",
                     reply_markup=get_button_list(all_names))


@dp.message_handler(Text(equals="Ok"))  # отображение скриншотов из истории
async def show(msg: types.Message):
    global status
    global show_screenshot
    for name in show_screenshot:
        await send_image(msg, name)
    await msg.answer("Выберите:",
                     reply_markup=next_button)


@dp.message_handler()  # отбираем названия скриншотов для показа
async def input_value(msg: types.Message):
    global show_screenshot
    global status
    if status is not None:
        show_screenshot.append(msg.text)
