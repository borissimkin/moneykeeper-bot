import telegram
from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler

from bot import bot
from bot.conversations.view_transactions.keyboards import \
    choose_and_add_next_previous_keyboard, prefix_command, reply_main_keyboard
from bot.conversations.view_transactions.messages import make_text_list_transactions
from bot.conversations.view_transactions.utils import make_list_transactions, make_list_consumptions, make_list_earnings
from bot.models import session
from bot.utils import update_username, update_activity


@update_username
@update_activity
def view_transactions(update: Update, context: CallbackContext):
    transactions = make_list_transactions(session, update.message.from_user.id)
    text = make_text_list_transactions(session, transactions)
    bot.send_message(chat_id=update.message.from_user.id,
                     text=text,
                     parse_mode=telegram.ParseMode.HTML,
                     reply_markup=reply_main_keyboard)


def handler_view_transactions(update: Update, context: CallbackContext):
    query = update.callback_query
    request = query.data
    if request == '{}all'.format(prefix_command):
        transactions = make_list_transactions(session, update.effective_user.id)
        text = make_text_list_transactions(session, transactions)
    elif request == '{}earnings'.format(prefix_command):
        transactions = make_list_earnings(session, update.effective_user.id)
        text = make_text_list_transactions(session, transactions)
    else:
        transactions = make_list_consumptions(session, update.effective_user.id)
        text = make_text_list_transactions(session, transactions)
    query.edit_message_text(text=text,
                            reply_markup=reply_main_keyboard)


