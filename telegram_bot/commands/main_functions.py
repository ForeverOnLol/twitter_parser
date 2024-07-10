from aiogram import types
from aiogram.types import CallbackQuery

from telegram_bot.keyboards import *
from telegram_bot.constants import dp


@dp.message_handler(commands=['vis'], is_channel_admin=True)
async def vis_command(message: types.Message):
    subscriptions = db.get_visible_subscriptions()
    subscriptions = ['@{}\n'.format(f) for f in subscriptions[:]]
    subscriptions = '\n'.join(subscriptions)
    await message.reply(f'Список видимых твиттеров: \n{subscriptions}')


@dp.message_handler(commands=['invis'], is_channel_admin=True)
async def unvis_command(message: types.Message):
    subscriptions = db.get_invisible_subscriptions()
    subscriptions = ['@{}\n'.format(f) for f in subscriptions[:]]
    subscriptions = '\n'.join(subscriptions)
    await message.reply(f'Список заглушенных твиттеров: \n{subscriptions}')


@dp.message_handler(commands=['edit'], is_channel_admin=True)
async def change_following(message: types.Message):
    try:
        index_elem = 0
        info_elem = db.get_subscription_data(subscription_rowid=index_elem)
        info = f"Название: @{info_elem['title']}\n" \
               f"Видимость: {'Да' if bool(info_elem['visible']) else 'Нет'}"
        await message.answer(text=info,
                             reply_markup=await AdminInlineKeyboards.following_update_keyboard(index_elem,
                                                                                               info_elem[
                                                                                                   'visible']))
    except IndexError:
        await message.answer(
            text='Вы не подписаны в твиттере ни на одну страницу. Подпишитесь хотя бы на одну страницу у себя '
                 'в профиле Твиттера и повторно введите команду.')


@dp.callback_query_handler(text_contains="select_twitter", is_channel_admin=True)
async def get_twitter_elem_info(call: CallbackQuery):
    data = call.data.split(':')
    index_elem = int(data[2])
    try:
        info_elem = db.get_subscription_data(subscription_rowid=index_elem)
        info = f"Название: @{info_elem['title']}\n" \
               f"Видимость: {'Да' if bool(info_elem['visible']) else 'Нет'}"
        await call.message.edit_text(text=info)
        await call.message.edit_reply_markup(
            reply_markup=await AdminInlineKeyboards.following_update_keyboard(index_elem, info_elem['visible']))
    except IndexError:
        await call.message.edit_text(
            text='Вы не подписаны в твиттере ни на одну страницу. Подпишитесь хотя бы на одну страницу у себя '
                 'в профиле Твиттера и повторно введите команду.')


@dp.callback_query_handler(text_contains="change_visible")
async def change_visible_elem(call: CallbackQuery):
    data = call.data.split(':')
    index_elem = int(data[2])
    db.change_visible_of_subscription(index_elem)
    await get_twitter_elem_info(call=call)
