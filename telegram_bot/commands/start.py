from aiogram import types
from dotenv import find_dotenv

from envconfig import EnvConfig
from logger import *
from telegram_bot.constants import dp

@dp.my_chat_member_handler(is_needed_channel=EnvConfig.PRIVATE_CHANNEL_TITLE)
async def bot_add_private_channel(message: types.message):
    logging.info('Бот успешно добавлен в приватный канал!')
    channel_id = message.chat.id
    with open(find_dotenv(), "a") as f:
        f.write(f"\nPRIVATE_CHANNEL_ID={channel_id}")


def register_pre_handlers(tgbot):
    tgbot.dp.register_my_chat_member_handler(bot_add_private_channel, is_needed_channel=tgbot)
