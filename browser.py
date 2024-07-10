import os
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from logger import *

class Browser:
    __options = Options()

    def __init__(self, headless: bool = False):
        if headless:
            self._enable_headless()
        self._driver = self.__initialize_driver()

    def __initialize_driver(self):
        self.__options.add_argument("--no-sandbox")
        self.__options.add_argument('--disable-dev-shm-usage')
        self.__options.add_argument("--nogpu")
        self.__options.add_argument("--disable-gpu")
        self.__options.add_argument("--window-size=1920,1000")
        self.__options.add_argument("--enable-javascript")
        self.__options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.__options.add_experimental_option('useAutomationExtension', False)
        self.__options.add_argument('--disable-blink-features=AutomationControlled')
        self.__options.binary_location = "/opt/google/chrome/google-chrome"
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                options=self.__options)

    def _enable_headless(self):
        self.__options.headless = True

    def _validation(self, username):
        try:
            WebDriverWait(self._driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//input[@autocomplete="on"]'))).send_keys(username)
            self._driver.find_elements(By.XPATH, value='//div[@role="button"]')[1].click()
        finally:
            return


class MyTwitter(Browser):

    def __init__(self):
        super().__init__()
        self.sign_in()

    def sign_in(self):
        logging.info(f'Попытка авторизации...')
        try:
            account_email, account_password, account_username = get_account_data()
        except Exception:
            logging.critical(f'Данные аккаунта не были получены.')
            raise ValueError
        try:
            self._driver.get('https://twitter.com/i/flow/login')
        except Exception as ex:
            logging.error(msg=f'Нет соединения с сайтом. Возможно, из Вашей страны нельзя выйти в Twitter.')
        sleep(2)
        WebDriverWait(self._driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@autocomplete="username"]'))).send_keys(account_email)
        self._driver.find_elements(By.XPATH, value='//div[@role="button"]')[2].click()

        sleep(2)
        self._validation(username=account_username)
        sleep(3)
        WebDriverWait(self._driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@autocomplete="current-password"]'))).send_keys(
            account_password)

        self._driver.find_elements(By.XPATH, value='//div[@role="button"]')[2].click()
        sleep(4)
        logging.info(f'Авторизация успешно завершена!')
        sleep(5)

    def get_following(self):
        username = get_account_data()[2]
        self._driver.get(f'https://twitter.com/{username}/following')
        WebDriverWait(self._driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@aria-label="Timeline: Following"]')))
        following_list = self._driver.find_elements(By.XPATH,
                                                   value='//div[@aria-label="Timeline: Following"]/*//div[@dir="ltr"]')
        for i in range(len(following_list)):
            following_list[i] = following_list[i].text[1:]

        return following_list

def get_account_data():
    env = os.environ
    account_email = env['TW_EMAIL']
    account_password = env['TW_PASSWORD']
    account_username = env['TW_USERNAME']
    return (account_email, account_password, account_username)