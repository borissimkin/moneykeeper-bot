import datetime

from telegram.ext import CommandHandler, CallbackQueryHandler

from bot import dispatcher, updater, jobs, config, logger
from bot.commands import start
from bot.commands import today
from bot.commands import export_database
from bot.commands import help
from bot.commands.export_xls import handler_export
from bot.conversations.add_consumption.handlers import add_consumption
from bot.conversations.add_earning.handlers import add_earning
from bot.conversations.add_transaction.handlers import add_transaction
from bot.conversations.edit_categories.handlers import edit_categories
from bot.conversations.delete_transaction.handlers import delete_transaction
from bot.conversations.statistics import prefix_query_statistics
from bot.conversations.statistics.enter_time_period.handlers import time_period
from bot.conversations.statistics.handlers import entry_point_statistics, handler_statistics
from bot.conversations.view_transactions import prefix_query
from bot.conversations.view_transactions.query_handlers import view_transactions, handler_view_transactions
from bot.job_queue.handlers import job_results, job_backup_database


def start_handlers():
    dispatcher.add_handler(CommandHandler(start.text_command, start.handler))

    dispatcher.add_handler(CommandHandler('view_transactions', view_transactions))

    dispatcher.add_handler(CommandHandler('statistics', entry_point_statistics))

    dispatcher.add_handler(CommandHandler('export', handler_export))

    dispatcher.add_handler(CommandHandler(today.text_command, today.handler))

    dispatcher.add_handler(CommandHandler(export_database.text_command, export_database.handler))

    dispatcher.add_handler(CommandHandler(help.text_command, help.handler))

    dispatcher.add_handler(add_consumption)

    dispatcher.add_handler(add_earning)

    dispatcher.add_handler(edit_categories)

    dispatcher.add_handler(add_transaction)

    dispatcher.add_handler(delete_transaction)

    dispatcher.add_handler(time_period)

    dispatcher.add_handler(CallbackQueryHandler(handler_view_transactions,
                                                pass_user_data=True, pattern=prefix_query))

    dispatcher.add_handler(CallbackQueryHandler(handler_statistics,
                                                pass_user_data=True, pattern=prefix_query_statistics))

    jobs.run_daily(callback=job_results,
                   time=datetime.datetime.strptime(
                       config['jobs']['results_time'], '%H:%M:%S').time())

    jobs.run_daily(callback=job_backup_database,
                   time=datetime.datetime.strptime(
                       config['jobs']['backup_database'], '%H:%M:%S').time())
    logger.info("All handlers successfully launched!")


if __name__ == '__main__':
    start_handlers()
    updater.start_polling()
    updater.idle()
