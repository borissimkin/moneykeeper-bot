from telegram import Update
from telegram.ext import CallbackContext

from bot import bot


class StartHandler:
    text_command = 'start'

    @classmethod
    def start(cls, update: Update, context: CallbackContext):
        bot.send_message(chat_id=update.message.from_user.id,
                         text='Hello world')
