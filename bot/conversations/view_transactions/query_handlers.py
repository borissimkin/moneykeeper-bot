import telegram
from telegram import Update
from telegram.ext import CallbackContext, CallbackQueryHandler

from bot import bot
from bot.conversations.view_transactions.keyboards import make_buttons_view_transaction
from bot.conversations.view_transactions.messages import make_text_list_transactions
from bot.conversations.view_transactions.utils import make_list_transactions
from bot.models import session
from bot.utils import update_username, update_activity


@update_username
@update_activity
def view_transactions(update: Update, context: CallbackContext):
    bot.send_message(chat_id=update.message.from_user.id,
                     text=make_text_list_transactions(session, make_list_transactions(session,
                                                                                      update.message.from_user.id)),
                     parse_mode=telegram.ParseMode.HTML,
                     reply_markup=make_buttons_view_transaction())


def handler_view_transactions(update: Update, context: CallbackContext):
    query = update.callback_query

    query.edit_message_text(text="Selected option: {}".format(query.data))

