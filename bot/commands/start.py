import sqlalchemy
import telegram
from telegram import Update
from telegram.ext import CallbackContext

from bot import bot
from bot.models import session, User


class StartHandler:
    text_command = 'start'

    @classmethod
    def start(cls, update: Update, context: CallbackContext):
        if not cls.check_user_in_db(update.message.from_user.id):
            cls.add_user_in_db(update)
            cls.send_welcome_text(update.message.from_user.id)

    @staticmethod
    def add_user_in_db(update):
        user = update.message.from_user
        username = getattr(user, 'username', sqlalchemy.null())
        session.add(User(telegram_username=username, telegram_user_id=user.id,
                         first_name=user.first_name, last_name=user.last_name))
        session.commit()

    @staticmethod
    def check_user_in_db(user_id):
        user = session.query(User.telegram_user_id == user_id).first()
        return True if user else False

    @staticmethod
    def send_welcome_text(user_id):
        user = session.query(User).filter(User.telegram_user_id == user_id).first()
        text = 'Привет <b>{}</b>!'.format(user.get_username())
        bot.send_message(chat_id=user_id,
                         text=text,
                         parse_mode=telegram.ParseMode.HTML)

