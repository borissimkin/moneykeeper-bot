import datetime

import pymorphy2
import sqlalchemy

from bot.buttons import Buttons
from bot.exceptions import BackIsNotDefined, ExitIsNotDefined
from bot.models import session, User


def update_activity(func):
    def wrapped(update, context, *args, **kwargs):
        user = session.query(User).filter(
            User.telegram_user_id == update.message.from_user.id).first()
        user.update_activity(session, datetime.datetime.now())
        return func(update, context, *args, **kwargs)
    return wrapped


def update_username(func):
    def wrapped(update, context, *args, **kwargs):
        telegram_user = update.message.from_user
        user = session.query(User).filter(User.telegram_user_id == update.message.from_user.id).first()
        username = getattr(telegram_user, 'username', sqlalchemy.null())
        user.update_username(session, username)
        return func(update, context, *args, **kwargs)
    return wrapped


def back(f):
    def wrapped(update, context, *args, **kwargs):
        if update.message.text == Buttons.back:
            try:
                back_func = context.user_data['back_func']
            except BackIsNotDefined as e:
                raise e
            return back_func(update, context, *args, **kwargs)
        return f(update, context, *args, **kwargs)
    return wrapped


def exit_dialog(f):
    def wrapped(update, context, *args, **kwargs):
        if update.message.text == Buttons.exit:
            try:
                exit_func = context.user_data['exit_func']
            except ExitIsNotDefined as e:
                raise e
            return exit_func(update, context, *args, **kwargs)
        return f(update, context, *args, **kwargs)
    return wrapped


def clear_user_data(f):
    def wrapped(update, context, *args, **kwargs):
        context.user_data.clear()
        return f(update, context, *args, **kwargs)
    return wrapped


def add_button_cancel(buttons):
    buttons.append([Buttons.cancel])
    return buttons


def add_buttons_exit_and_back(buttons):
    buttons.append([Buttons.back, Buttons.exit])
    return buttons


def add_button_exit(buttons):
    buttons.append([Buttons.exit])
    return buttons


def ruble_declension(count_ruble: int):
    morph = pymorphy2.MorphAnalyzer()
    money_morph = morph.parse('рубль')[0]
    return money_morph.make_agree_with_number(int(count_ruble)).word


def get_past_minutes_day(now):
    return now.hour * 60 + now.minute


def to_text_weekday(weekday: int):
    if weekday == 0:
        return 'Понедельник'
    elif weekday == 1:
        return 'Вторник'
    elif weekday == 2:
        return 'Среда'
    elif weekday == 3:
        return 'Четверг'
    elif weekday == 4:
        return 'Пятница'
    elif weekday == 5:
        return 'Суббота'
    elif weekday == 6:
        return 'Воскресенье'


def text_goodbye(now):
    if now.hour >= 19:
        return 'Доброй ночи!'
    return 'Хорошего дня!'
