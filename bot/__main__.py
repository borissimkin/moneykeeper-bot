from telegram.ext import CommandHandler

from bot import dispatcher, updater
from bot.commands.start import StartHandler
from bot.conversations.add_consumption.handlers import add_consumption
from bot.conversations.add_earning.handlers import add_earning
from bot.conversations.edit_categories.handlers import edit_categories
from bot.conversations.delete_transaction.handlers import delete_transaction


def start_handlers():
    dispatcher.add_handler(CommandHandler(StartHandler.text_command, StartHandler.start))

    dispatcher.add_handler(add_consumption)

    dispatcher.add_handler(add_earning)

    dispatcher.add_handler(edit_categories)

    dispatcher.add_handler(delete_transaction)


if __name__ == '__main__':
    start_handlers()
    updater.start_polling()
    updater.idle()
