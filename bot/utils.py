import datetime

import sqlalchemy

from bot.buttons import text_button_cancel, text_button_back, text_button_exit
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
        if update.message.text == text_button_back:
            try:
                back_func = context.user_data['back_func']
            except BackIsNotDefined as e:
                raise e
            return back_func(update, context, *args, **kwargs)
        return f(update, context, *args, **kwargs)
    return wrapped


def exit_dialog(f):
    def wrapped(update, context, *args, **kwargs):
        if update.message.text == text_button_exit:
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
    buttons.append([text_button_cancel])
    return buttons


def add_buttons_exit_and_back(buttons):
    buttons.append([text_button_back, text_button_exit])
    return buttons


def add_button_exit(buttons):
    buttons.append([text_button_exit])
    return buttons
