from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from envconfig import EnvConfig

bot = Bot(EnvConfig().TG_BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())