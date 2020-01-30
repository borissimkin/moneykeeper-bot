import sqlalchemy
import telegram
from telegram import Update
from telegram.ext import CallbackContext

from bot import bot
from bot.commands.help import make_text_help
from bot.models import User, CategoryEarning, CategoryConsumption, session_scope
from bot.utils import log_handler


text_command = 'start'


@log_handler
def handler(update: Update, context: CallbackContext):
    with session_scope() as session:
        if not check_user_in_db(update.message.from_user.id, session):
            add_user_in_db(update, session)
            create_default_categories_for_earning_and_consumption(update.message.from_user.id)
            send_welcome_text(update.message.from_user.id)


def add_user_in_db(update, session):
    user = update.message.from_user
    username = getattr(user, 'username', sqlalchemy.null())
    session.add(User(telegram_username=username, telegram_user_id=user.id,
                     first_name=user.first_name, last_name=user.last_name))
    session.commit()


def create_default_categories_for_earning_and_consumption(telegram_user_id):
    with session_scope() as session:
        user = session.query(User).filter(User.telegram_user_id == telegram_user_id).first()
        CategoryEarning.create_default_categories(session, user.id)
        CategoryConsumption.create_default_categories(session, user.id)


def check_user_in_db(user_id, session):
    user = session.query(User.telegram_user_id == user_id).first()
    return True if user else False


def send_welcome_text(telegram_user_id):
    bot.send_message(chat_id=telegram_user_id,
                     text=make_text_help(telegram_user_id),
                     parse_mode=telegram.ParseMode.HTML)