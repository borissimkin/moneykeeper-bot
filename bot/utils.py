import datetime

from bot.models import session, User


def update_activity(func):
    def wrapped(update, context, *args, **kwargs):
        user = session.query(User).filter(
            User.telegram_user_id == update.message.from_user.id).first()
        user.update_activity(datetime.datetime.now())
        return func(update, context, *args, **kwargs)
    return wrapped
