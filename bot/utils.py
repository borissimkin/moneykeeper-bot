import datetime

import sqlalchemy

from bot.models import session, User


def update_activity(func):
    def wrapped(update, context, *args, **kwargs):
        user = session.query(User).filter(
            User.telegram_user_id == update.message.from_user.id).first()
        user.update_activity(datetime.datetime.now())
        return func(update, context, *args, **kwargs)
    return wrapped


def update_username(func):
    def wrapped(update, context, *args, **kwargs):
        telegram_user = update.message.from_user
        user = session.query(User).filter(User.telegram_user_id == update.message.from_user.id).first()
        username = getattr(telegram_user, 'username', sqlalchemy.null())
        user.update_username(username)
        return func(update, context, *args, **kwargs)
    return wrapped


