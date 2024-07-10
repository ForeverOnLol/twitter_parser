import sqlite3

from typing import List, Optional

conn = sqlite3.connect('sqlite_db/subscriptions.db', check_same_thread=False)
cursor = conn.cursor()


def _init_db():
    """Инициализирует БД"""
    with open("sqlite_db/createdb.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет - инициализирует"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table'")
    table_exists = cursor.fetchall()
    if table_exists:
        returnarser
    _init_db()


def update_subscriptions(subscriptions: tuple):
    """ Обновляет список подписок в БД"""
    try:
        cursor.execute('DELETE FROM subscription WHERE subscription.title NOT IN {}'.format(subscriptions))
    except sqlite3.OperationalError:
        pass
    subscriptions = [(sub,) for sub in subscriptions]
    cursor.executemany(f'INSERT OR IGNORE INTO subscription (title) VALUES (?)', subscriptions)
    conn.commit()


def get_subscription_data(subscription_title: Optional[str] = None, subscription_rowid: Optional[int] = None) -> dict:
    """ Получение данных из БД по имени подписки или по id записи"""
    if subscription_title is not None:
        search_by = 'title'
        search_by_value = subscription_title
        cursor.execute("SELECT id, title, visible, last_update from subscription"
                       " WHERE {}='{}'".format(search_by, search_by_value))
    elif subscription_rowid is not None:
        search_by = 'ROWID'
        search_by_value = subscription_rowid
        cursor.execute("SELECT id, title, visible, last_update from subscription"
                       " LIMIT 1 OFFSET {}".format(search_by_value))
    else:
        raise TypeError(f'Введите параметр, по которому искать подписку')

    data = cursor.fetchone()
    if data:
        data = {
            'rowid': data[0],
            'title': data[1],
            'visible': bool(data[2]),
            'last_update': str(data[3]),
        }
        return data
    else:
        raise IndexError(f'Подписки {"под ID" if search_by == "id" else "под названием"} {search_by_value} не существует!')


def update_last_dt(subscription_title: str):
    cursor.execute(
        "UPDATE subscription SET last_update=(datetime('now','localtime')) WHERE title='{}'".format(subscription_title))
    conn.commit()


def get_visible_subscriptions() -> List[str]:
    """ Возвращает список названий ОТОБРАЖАЕМЫХ твиттов, на которые подписан аккаунт"""
    cursor.execute("SELECT title FROM subscription WHERE visible=1")
    data = cursor.fetchall()
    data = [title[0] for title in data]
    return data

def get_invisible_subscriptions() -> List[str]:
    """ Возвращает список названий НЕВИДИМЫХ твиттов, на которые подписан аккаунт"""
    cursor.execute("SELECT title FROM subscription WHERE visible=0")
    data = cursor.fetchall()
    data = [title[0] for title in data]
    return data

def get_count_subscriptions():
    cursor.execute("SELECT COUNT(*) FROM subscription")
    data = cursor.fetchone()
    return int(data[0])

def change_visible_of_subscription(subscription_rowid: int):
    sub = get_subscription_data(subscription_rowid=subscription_rowid)
    if sub['visible']:
        set_value = 0
    else:
        set_value = 1
    cursor.execute("UPDATE subscription SET visible={} WHERE title='{}'".format(set_value, sub['title']))
    conn.commit()



check_db_exists()

