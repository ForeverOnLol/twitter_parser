import os
from typing import Optional, Union

from dotenv import load_dotenv


class EnvConfig:
    TW_EMAIL: str
    TW_PASSWORD: str
    TW_USERNAME: str
    TG_BOT_TOKEN: str
    PRIVATE_CHANNEL_TITLE: str
    PRIVATE_CHANNEL_ID: Optional[Union[int, None]]

    @classmethod
    def load(cls):
        load_dotenv()
        cls.TW_EMAIL = os.environ['TW_EMAIL']
        cls.TW_PASSWORD = os.environ['TW_PASSWORD']
        cls.TW_USERNAME = os.environ['TW_USERNAME']
        cls.TG_BOT_TOKEN = os.environ['TG_BOT_TOKEN']
        cls.PRIVATE_CHANNEL_TITLE = os.environ['PRIVATE_CHANNEL_TITLE']
        cls.PRIVATE_CHANNEL_ID = cls.__load_private_channel_id()

    @classmethod
    def __load_private_channel_id(cls):
        try:
            return os.environ['PRIVATE_CHANNEL_ID']
        except Exception:
            return None

EnvConfig.load()