from typing import Dict

from aiogram.utils import executor
from .filters import *
from .constants import bot, Bot, Dispatcher
from .commands import *


class TgBot:
    threads_storage: Dict
    bot: Bot
    dp: Dispatcher
    channel_title: str
    channel_id: int

    def __init__(self, threads_storage):
        self.threads_storage = threads_storage
        self.bot = bot
        self.dp = dp
        self.channel_title = EnvConfig.PRIVATE_CHANNEL_TITLE
        self.channel_id = EnvConfig.PRIVATE_CHANNEL_ID
        if self.channel_id:
            self.set_status_active()

    def start(self, tg_event_loop):
        """
        Запуск бота
        :param tg_event_loop: содержит в себе ссылку на ивент луп телеграм бота
        :return:
        """
        executor.start_polling(self.dp, skip_updates=True, loop=tg_event_loop)

    def set_status_active(self):
        """
        Передаёт другим потокам через словарь, что ID закрытого канала получен
        :return:
        """
        self.threads_storage['status_channel_id'] = True

    def update_channel_id(self):
        EnvConfig.load()
        self.channel_id = EnvConfig.PRIVATE_CHANNEL_ID

    def enable_new_functions(self):
        self.update_channel_id()
