from telegram.ext import CommandHandler

from bot import dispatcher, updater
from bot.start import StartHandler


def start_handlers():
    dispatcher.add_handler(CommandHandler(StartHandler.text_command, StartHandler.start))


if __name__ == '__main__':
    start_handlers()
    updater.start_polling()
    updater.idle()
