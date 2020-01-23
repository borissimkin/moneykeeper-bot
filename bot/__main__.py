from telegram.ext import CommandHandler, CallbackQueryHandler

from bot import dispatcher, updater
from bot.commands.start import StartHandler
from bot.commands import today
from bot.conversations.add_consumption.handlers import add_consumption
from bot.conversations.add_earning.handlers import add_earning
from bot.conversations.edit_categories.handlers import edit_categories
from bot.conversations.delete_transaction.handlers import delete_transaction
from bot.conversations.view_transactions.query_handlers import view_transactions, handler_view_transactions


def start_handlers():
    dispatcher.add_handler(CommandHandler(StartHandler.text_command, StartHandler.handler))

    dispatcher.add_handler(CommandHandler('view_transactions', view_transactions))

    dispatcher.add_handler(CommandHandler(today.text_command, today.handler))

    dispatcher.add_handler(add_consumption)

    dispatcher.add_handler(add_earning)

    dispatcher.add_handler(edit_categories)

    dispatcher.add_handler(delete_transaction)

    dispatcher.add_handler(CallbackQueryHandler(handler_view_transactions,
                                                pass_user_data=True))




if __name__ == '__main__':
    start_handlers()
    updater.start_polling()
    updater.idle()
