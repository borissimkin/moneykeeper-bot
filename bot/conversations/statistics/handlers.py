import datetime

import telegram
from telegram import Update, InputMediaPhoto
from telegram.ext import CallbackContext

from bot import bot, session
from bot.conversations.statistics import prefix_query_statistics
from bot.conversations.statistics.graphs import make_pie_graph
from bot.conversations.statistics.keyboards import reply_main_keyboard
from bot.conversations.statistics.type_transacation_graph import TypeTransaction
from bot.conversations.statistics.utils import get_consumptions_for_graph_user_all_time, from_datetime_to_str, \
    get_lifetime_user, get_earnings_for_graph_user_all_time
from bot.models import User
from bot.utils import update_username, update_activity, log_handler


@update_username
@update_activity
@log_handler
def main_menu_statistics(update: Update, context: CallbackContext):
    user = session.query(User).filter(User.telegram_user_id == update.message.from_user.id).first()
    data, labels = get_consumptions_for_graph_user_all_time(session, user)
    path_to_graph = make_pie_graph(data, labels, get_lifetime_user(user, now=datetime.datetime.now()),
                                   TypeTransaction.CONSUMPTION)
    bot.send_photo(chat_id=update.message.from_user.id,
                   photo=open(path_to_graph, 'rb'),
                   reply_markup=reply_main_keyboard)


def handler_statistics(update: Update, context: CallbackContext):
    query = update.callback_query
    request = query.data
    user = session.query(User).filter(User.telegram_user_id == update.effective_user.id).first()
    if request == '{}earnings'.format(prefix_query_statistics):
        data, labels = get_earnings_for_graph_user_all_time(session, user)
        path_to_graph = make_pie_graph(data, labels, get_lifetime_user(user, now=datetime.datetime.now()),
                                       TypeTransaction.EARNING)
        media_object = InputMediaPhoto(open(path_to_graph, 'rb'))
        bot.edit_message_media(chat_id=query.message.chat_id,
                               message_id=query.message.message_id,
                               media=media_object,
                               reply_markup=reply_main_keyboard)

    elif request == '{}consumptions'.format(prefix_query_statistics):
        data, labels = get_consumptions_for_graph_user_all_time(session, user)
        path_to_graph = make_pie_graph(data, labels, get_lifetime_user(user, now=datetime.datetime.now()),
                                       TypeTransaction.CONSUMPTION)
        media_object = InputMediaPhoto(open(path_to_graph, 'rb'))
        bot.edit_message_media(chat_id=query.message.chat_id,
                               message_id=query.message.message_id,
                               media=media_object,
                               reply_markup=reply_main_keyboard)
