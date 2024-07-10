import asyncio
import collections
import twint
from time import sleep

from dotenv import load_dotenv
from twint.token import RefreshTokenException
import os
import db
from logger import *


class PostsParse:
    def __init__(self, tg_bot, tg_event_loop):
        self.queue = collections.deque()
        self.tg_bot = tg_bot
        self.tg_event_loop = tg_event_loop
        self.channel_id = get_channel_id()

    @staticmethod
    def wait_for_token(func):
        def inner(*a, **kw):
            try:
                result = func(*a, **kw)
                inner.wait = 30
                return result
            except RefreshTokenException:
                logging.error(
                    f'Ошибка при получении постов. Попытка обновления гостевого токена. Задержка {inner.wait}с.')
                sleep(inner.wait)
                inner.wait *= 2
                return inner(*a, **kw)

        inner.wait = 30
        return inner

    @staticmethod
    @wait_for_token.__get__(0)
    def _load_posts(username: str, last_update: str):
        ''' Парсинг постов через Twint'''
        c = twint.Config()
        c.Username = username
        c.Since = last_update
        c.Hide_output = True
        c.Store_object = True
        # Поиск твиттов
        twint.run.Search(c)
        # Поиск ретвиттов
        c.Native_retweets = True
        twint.run.Search(c)

        # Удаление реплаев и сортировка по дате
        posts = twint.output.tweets_list.copy()
        for p in posts[:]:
            if (len(p.reply_to) > 0) and (p.retweet == False):
                posts.remove(p)
        posts = sorted(posts[:], key=lambda x: x.datetime, reverse=True)

        twint.output.tweets_list.clear()
        return posts

    def handle_queue(self):
        while self.queue:
            username = self.queue.popleft()
            following_info = db.get_subscription_data(subscription_title=username)
            posts = PostsParse._load_posts(username=username, last_update=following_info['last_update'])

            if posts:
                db.update_last_dt(username)
                for p in posts:
                    logging.info(f'Новый пост от @{p.name}\nТекст:{p.tweet}')
                    asyncio.run_coroutine_threadsafe(self.tg_bot.send_message(chat_id=self.channel_id,
                                                                      parse_mode='html',
                                                                      disable_web_page_preview=True,
                                                                      text=f"<u><b><i>{p.name}</i></b></u>\n"
                                                                           f"{'Retweet' if p.retweet else 'Tweet'}\n\n"
                                                                           f"<a href=\"{p.link}\">{p.tweet}</a>"
                                                                      ), loop=self.tg_event_loop)

    def add_in_queue(self):
        following = db.get_visible_subscriptions()
        for f in following:
            if f not in self.queue:
                self.queue.append(f)

def get_channel_id():
    load_dotenv()
    env = os.environ
    channel_id = env['PRIVATE_CHANNEL_ID']
    return channel_id
