from selenium import webdriver
import time

from selenium.webdriver.chrome.options import Options

from logging_seting import logger
from main import CHROMADRIVER_PATH


class Browser:
    """ Клас настройки веб драйвера """
    def __init__(self, url, name):
        self.name = name
        self.url = url
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        self.browser = webdriver.Chrome(executable_path=CHROMADRIVER_PATH,
                                        options=options)
        self.browser.set_window_size(1920, 1080)
        logger.info('browser is created')

    def scroll(self):  # прокручивает всю страницу, чтобы загрузить все элементы
        last_height = self.browser.execute_script("return document.body.scrollHeight")

        while True:
            # Прокручиваем в конец страницы
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Ждем загрузку страницы
            time.sleep(1)

            # Подсчитываем новую высоту и приравниваем к старой
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                return last_height
            last_height = new_height


    def get_sreenshot(self):  #  Получаем скриншот 1920 x full_height
        self.browser.get(self.url)
        height = self.scroll()
        self.browser.set_window_size(1920, height)
        time.sleep(3)
        logger.info('Browser get screenshot')
        self.browser.save_screenshot(f'./media/{self.name}.png')
        logger.info('Browser quit')
        self.browser.quit()
