from telegram.ext import CommandHandler

from bot import dispatcher, updater
from bot.commands.start import StartHandler
from bot.conversations.consumption.handlers import add_consumption
from bot.conversations.earning.handlers import add_earning


def start_handlers():
    dispatcher.add_handler(CommandHandler(StartHandler.text_command, StartHandler.start))

    dispatcher.add_handler(add_consumption)

    dispatcher.add_handler(add_earning)


if __name__ == '__main__':
    start_handlers()
    updater.start_polling()
    updater.idle()
