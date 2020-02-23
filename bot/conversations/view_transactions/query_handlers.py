import telegram
from telegram import Update
from telegram.ext import CallbackContext

from bot import bot
from bot.conversations.view_transactions import prefix_query
from bot.conversations.view_transactions.keyboards import \
    get_keyboard
from bot.conversations.view_transactions.messages import make_text_list_transactions
from bot.conversations.view_transactions.transactions_controller import TransactionsController
from bot.conversations.view_transactions.utils import make_list_transactions, make_list_consumptions, make_list_earnings
from bot.models import session_scope
from bot.utils import update_username, update_activity, log_handler


@update_username
@update_activity
@log_handler
def view_transactions(update: Update, context: CallbackContext):
    with session_scope() as session:
        transactions = make_list_transactions(session, update.message.from_user.id)
        transactions_controller = TransactionsController(transactions)
        text = make_text_list_transactions(session, transactions_controller.get_current_part())
        context.user_data['transactions_controller'] = transactions_controller
    bot.send_message(chat_id=update.message.from_user.id,
                     text=text,
                     parse_mode=telegram.ParseMode.HTML,
                     reply_markup=get_keyboard(context.user_data['transactions_controller']))


def handler_view_transactions(update: Update, context: CallbackContext):
    query = update.callback_query
    request = query.data
    text = None
    user_data = context.user_data
    with session_scope() as session:
        if request == '{}all'.format(prefix_query):
            transactions = make_list_transactions(session, update.effective_user.id)
            user_data['transactions_controller'] = TransactionsController(transactions)
            text = make_text_list_transactions(session, user_data['transactions_controller'].get_current_part())
        elif request == '{}earnings'.format(prefix_query):
            transactions = make_list_earnings(session, update.effective_user.id)
            user_data['transactions_controller'] = TransactionsController(transactions)
            text = make_text_list_transactions(session, user_data['transactions_controller'].get_current_part())
        elif request == '{}consumptions'.format(prefix_query):
            transactions = make_list_consumptions(session, update.effective_user.id)
            user_data['transactions_controller'] = TransactionsController(transactions)
            text = make_text_list_transactions(session, user_data['transactions_controller'].get_current_part())
        elif request == '{}next'.format(prefix_query):
            text = make_text_list_transactions(session, user_data['transactions_controller'].next())
        elif request == '{}previous'.format(prefix_query):
            text = make_text_list_transactions(session, user_data['transactions_controller'].previous())
    query.edit_message_text(text=text,
                            reply_markup=get_keyboard(context.user_data['transactions_controller']))


