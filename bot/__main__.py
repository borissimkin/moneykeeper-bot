from telegram.ext import CommandHandler, ConversationHandler, Filters

from bot import dispatcher, updater
from bot.conversations.consumption.handlers import add_consumption
from bot.start import StartHandler


def start_handlers():
    dispatcher.add_handler(CommandHandler(StartHandler.text_command, StartHandler.start))

    dispatcher.add_handler(add_consumption)


if __name__ == '__main__':
    start_handlers()
    updater.start_polling()
    updater.idle()
