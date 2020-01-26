import os

from telegram import Update
from telegram.ext import CallbackContext

from bot import bot
from bot.utils import restricted

text_command = 'database'


@restricted
def handler(update: Update, context: CallbackContext):
    send_database(update.message.from_user.id)


def send_database(telegram_user_id):
    bot.send_document(chat_id=telegram_user_id,
                      document=open(os.path.join(os.getcwd(), 'database.db'), 'rb'))