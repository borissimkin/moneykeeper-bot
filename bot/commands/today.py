import datetime

import telegram
from telegram import Update
from telegram.ext import CallbackContext

from bot import bot

from bot.models import User, session_scope, CategoryEarning, CategoryConsumption
from bot.statistics.utils import get_earnings_today, get_consumptions_today, total_amount_money
from bot.utils import update_activity, update_username, to_text_weekday, text_goodbye, log_handler

text_command = 'today'


@update_activity
@update_username
@log_handler
def handler(update: Update, context: CallbackContext):
    with session_scope() as session:
        user = User.get_user_by_telegram_user_id(session, update.message.from_user.id)
        text = make_text_today(session, datetime.datetime.now(), user)
    bot.send_message(chat_id=update.message.from_user.id,
                     text=text,
                     parse_mode=telegram.ParseMode.HTML,
                     )


def make_text_today(session, now, user: User):
    return f'{head_message(now)}\n\n' \
        f'{make_text_consumptions(session, now, user)}\n' \
        f'{make_text_earnings(session, now, user)}\n' \
        f'{make_text_total(session, now, user)}\n' \
        f'{text_goodbye(now)}'


def make_text_earnings(session, now, user):
    earnings = get_earnings_today(session, now, user)
    if not earnings:
        return 'Доходов сегодня нет.\n'
    text = '<b>Доходы:</b>\n'
    for e in earnings:
        category = session.query(CategoryEarning).get(e.category_id)
        text += f'{category.category} - {e.amount_money} р.\n'
    return text


def make_text_consumptions(session, now, user):
    consumptions = get_consumptions_today(session, now, user)
    if not consumptions:
        return 'Расходов сегодня нет!\n'
    text = '<b>Расходы:</b>\n'
    for c in consumptions:
        category = session.query(CategoryConsumption).get(c.category_id)
        text += f'{category.category} - {c.amount_money} р.\n'
    return text


def head_message(now):
    return f"Информация на {now.strftime('%d.%m.%Y')} {now.strftime('%H:%M')}, {to_text_weekday(now.weekday())}"


def make_text_total(session, now, user: User):
    consumptions = get_consumptions_today(session, now, user)
    earnings = get_earnings_today(session, now, user)
    return f'<b>Всего:</b>\n' \
        f'Доход: {total_amount_money(earnings)}\n' \
        f'Расход: {total_amount_money(consumptions)}\n'

