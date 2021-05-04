import configparser
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from logging_seting import logger

config = configparser.ConfigParser()
config.read('config.ini')
TOKEN = config.get("Telegram","TOKEN")
CHROMADRIVER_PATH = config.get("Chromedriver","PATH")

bot = Bot(TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

if __name__ == '__main__':
    logger.info('bot is running...')
    from handlers import dp
    executor.start_polling(dp)
