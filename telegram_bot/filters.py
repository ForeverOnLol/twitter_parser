from aiogram.dispatcher.filters import BoundFilter
from aiogram import types

from envconfig import EnvConfig
from telegram_bot.constants import dp


class IsNeededChannelFilter(BoundFilter):
    """
    Проверка, что данный канал является нужным
    """
    key = 'is_needed_channel'

    def __init__(self, is_needed_channel):
        """
        :param is_needed_channel: экземпляр класса TgBot
        """
        self.tg_bot = is_needed_channel

    async def check(self, chat: types.Chat):
        chat_title: str = chat['chat']['title']
        status: str = chat['new_chat_member']['status']
        if chat_title == self.tg_bot.channel_title and status == 'administrator':
            self.tg_bot.enable_new_functions()
            return True
        else:
            return False


class IsChannelAdminFilter(BoundFilter):
    """
    Проверка, что данный участник является администратором канала
    """
    key = 'is_channel_admin'

    def __init__(self, is_channel_admin: bool):
        self.is_channel_admin = is_channel_admin

    async def check(self, message: types.Message):
        channel_id = EnvConfig.PRIVATE_CHANNEL_ID
        if channel_id:
            member = await message.bot.get_chat_member(channel_id, message.from_user.id)
            return member.is_chat_admin()
        else:
            return False

dp.filters_factory.bind(IsNeededChannelFilter)
dp.filters_factory.bind(IsChannelAdminFilter)
