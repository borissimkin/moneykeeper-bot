import sqlalchemy
import telegram
from telegram import Update
from telegram.ext import CallbackContext

from bot import bot
from bot.models import session, User, CategoryEarning, CategoryConsumption
from bot.utils import log_handler


class StartHandler:
    text_command = 'start'

    @classmethod
    @log_handler
    def handler(cls, update: Update, context: CallbackContext):
        if not cls.check_user_in_db(update.message.from_user.id, session):
            cls.add_user_in_db(update, session)
            cls.create_default_categories_for_earning_and_consumption(update.message.from_user.id)
            cls.send_welcome_text(update.message.from_user.id)

    @staticmethod
    def add_user_in_db(update, session):
        user = update.message.from_user
        username = getattr(user, 'username', sqlalchemy.null())
        session.add(User(telegram_username=username, telegram_user_id=user.id,
                         first_name=user.first_name, last_name=user.last_name))
        session.commit()

    @staticmethod
    def create_default_categories_for_earning_and_consumption(telegram_user_id):
        user = session.query(User).filter(User.telegram_user_id == telegram_user_id).first()
        CategoryEarning.create_default_categories(session, user.id)
        CategoryConsumption.create_default_categories(session, user.id)

    @staticmethod
    def check_user_in_db(user_id, session):
        user = session.query(User.telegram_user_id == user_id).first()
        return True if user else False

    @staticmethod
    def send_welcome_text(user_id):
        user = session.query(User).filter(User.telegram_user_id == user_id).first()
        text = 'Привет <b>{}</b>!'.format(user.get_username())
        bot.send_message(chat_id=user_id,
                         text=text,
                         parse_mode=telegram.ParseMode.HTML)

