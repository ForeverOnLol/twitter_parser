from aiogram.types import InlineKeyboardMarkup

import db
from .callbacks import select_twitter_callback, change_visible_callback



class AdminInlineKeyboards:
    """ Кнопки для инлайн клавиатуры в меню управления профилями твиттера
    Нужны для:
    - переключения между профилями
    - включения/выключения видимости профилей в ленте
    """
    @staticmethod
    async def following_update_keyboard(twitter_index, visible_of_tw):
        prev_i, next_i= await get_data_for_buttons(twitter_index)

        if visible_of_tw:
            visible_option = 'set_invisible'
            text_in_btn = 'заглушить'
        else:
            visible_option = 'set_visible'
            text_in_btn = 'показать'

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardMarkup(text="предыдущий",
                                         callback_data=select_twitter_callback.new(option_name="prev",
                                                                                   twitter_index=prev_i)),
                    InlineKeyboardMarkup(text="следующий",
                                         callback_data=select_twitter_callback.new(option_name="next",
                                                                                   twitter_index=next_i))

                ],
                [
                    InlineKeyboardMarkup(text=text_in_btn,
                                         callback_data=change_visible_callback.new(option_name=visible_option,
                                                                                   twitter_index=twitter_index))
                ]
            ])
        return keyboard

async def get_data_for_buttons(twitter_index: int) -> tuple:
    '''
    Получает данные для кнопок:
    - индексы предыдущего и следующего профиля твиттера
    :param twitter_index:
    :return:
    '''
    if type(twitter_index) != int:
        twitter_index = int(twitter_index)
    subscriptions_size = db.get_count_subscriptions()
    if twitter_index == 0:
        prev_index = subscriptions_size - 1
    else:
        prev_index = twitter_index - 1
    if twitter_index == subscriptions_size - 1:
        next_index = 0
    else:
        next_index = twitter_index + 1
    return (prev_index, next_index)

