import asyncio

from logger import *
from threading import Thread
from time import sleep

from browser import MyTwitter
from postparser import PostsParse
import db
from telegram_bot import TgBot


class ThreadingManager:
    """
     Создание 3х потоков и реализация бизнес логики
    """
    th_sharing_storage = dict()

    def __init__(self):
        self.set_storage_empty()
        self.run_threads()

    def set_storage_empty(self):
        self.th_sharing_storage['status_channel_id'] = False

    def run_threads(self):
        self.threads = [
            Thread(target=self.run_bot, kwargs={'th_sharing_storage': self.th_sharing_storage}, name='tg_bot'),
            # Thread(target=self.run_parse_own_subscription, kwargs={'wait_for': 10}, name='parse_own_following'),
            # Thread(target=self.run_parse_posts, kwargs={'wait_for': 30}, name='PostParser')

        ]
        for th in self.threads: th.start()

    @staticmethod
    def run_bot(th_sharing_storage: dict):
        """
        Запуск потока с ботом
        :param th_sharing_storage: ссылка на хранилище обмена между потоками
        :return:
        """
        global tg_event_loop
        tg_event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(tg_event_loop)
        tg_bot = TgBot(threads_storage=th_sharing_storage)
        tg_bot.start(tg_event_loop=tg_event_loop)

    @staticmethod
    def run_parse_own_subscription(wait_for: int = 0):
        """
        Запуск потока с браузером, который парсит подписки аккаунта
        :param wait_for:
        :return:
        """
        own_twitter_page = MyTwitter()
        while True:
            following_list = own_twitter_page.get_following()
            db.update_subscriptions(following_list)
            sleep(wait_for)

    @staticmethod
    def run_parse_posts(wait_for: int, tg_bot: TgBot, th_sharing_storage: dict):
        """
        Запуск потока, который парсит посты твиттеров из базы данных
        :param wait_for:
        :param tg_bot:
        :return:
        """
        while th_sharing_storage['status_channel_id'] == False:
            logging.info('Добавьте бота в канал!')
            sleep(20)
        pp = PostsParse(tg_bot=tg_bot, tg_event_loop=tg_event_loop)
        while True:
            pp.add_in_queue()
            pp.handle_queue()
            sleep(wait_for)
