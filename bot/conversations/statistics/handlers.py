import datetime

from telegram import Update, InputMediaPhoto
from telegram.ext import CallbackContext

from bot import bot, session
from bot.conversations.statistics import prefix_query_statistics
from bot.conversations.statistics.graph_controller import GraphController
from bot.conversations.statistics.graphs import make_pie_graph, make_stack_histogram_average
from bot.conversations.statistics.keyboards import reply_main_keyboard, reply_keyboard_choose_time_period
from bot.conversations.statistics.type_transacation_graph import TypeTransaction
from bot.conversations.statistics.utils import get_lifetime_user, get_yesterday, \
    get_today, get_current_week, \
    get_transactions_for_graph_by_type, get_current_month
from bot.models import User
from bot.utils import update_username, update_activity, log_handler


@update_username
@update_activity
@log_handler
def entry_point_statistics(update: Update, context: CallbackContext):
    user = session.query(User).filter(User.telegram_user_id == update.message.from_user.id).first()
    # path_to_graph = make_default_graph(user)
    path_to_graph = make_stack_histogram_average(session, user)
    graph_controller = GraphController(path_to_graph, get_lifetime_user(user, now=datetime.datetime.now()),
                                       TypeTransaction.CONSUMPTION)
    context.user_data['statistics'] = graph_controller
    bot.send_photo(chat_id=update.message.from_user.id,
                   photo=open(path_to_graph, 'rb'),
                   reply_markup=reply_main_keyboard)


def make_default_graph(user):
    time_period = get_lifetime_user(user, now=datetime.datetime.now())
    data, labels = get_transactions_for_graph_by_type(session, user, TypeTransaction.CONSUMPTION, time_period)
    path_to_graph = make_pie_graph(data, labels, time_period,
                                   TypeTransaction.CONSUMPTION)
    return path_to_graph


def handler_statistics(update: Update, context: CallbackContext):
    query = update.callback_query
    request = query.data
    user = session.query(User).filter(User.telegram_user_id == update.effective_user.id).first()
    graph_controller = context.user_data.get('statistics')
    if not graph_controller:
        graph_controller = GraphController(make_default_graph(user),
                                           get_lifetime_user(user,
                                                             datetime.datetime.now()),
                                           TypeTransaction.CONSUMPTION)
        context.user_data['statistics'] = graph_controller
    if request == '{}earnings'.format(prefix_query_statistics):
        graph_controller.update_type_transactions(TypeTransaction.EARNING)
        handler_button_choose_type_transactions(update, context, user)
    elif request == '{}consumptions'.format(prefix_query_statistics):
        graph_controller.update_type_transactions(TypeTransaction.CONSUMPTION)
        handler_button_choose_type_transactions(update, context, user)
    elif request == '{}time_period'.format(prefix_query_statistics):
        media_object = InputMediaPhoto(open(graph_controller.path_to_current_graph, 'rb'))
        bot.edit_message_media(chat_id=query.message.chat_id,
                               message_id=query.message.message_id,
                               media=media_object,
                               reply_markup=reply_keyboard_choose_time_period)
    elif request == '{}yesterday'.format(prefix_query_statistics):
        graph_controller.update_time_period(get_yesterday(datetime.datetime.now()))
        handler_button_choose_time_period(update, context, user)
    elif request == '{}today'.format(prefix_query_statistics):
        graph_controller.update_time_period(get_today(datetime.datetime.now()))
        handler_button_choose_time_period(update, context, user)
    elif request == '{}current_week'.format(prefix_query_statistics):
        graph_controller.update_time_period(get_current_week(datetime.datetime.now()))
        handler_button_choose_time_period(update, context, user)
    elif request == '{}current_month'.format(prefix_query_statistics):
        graph_controller.update_time_period(get_current_month(datetime.datetime.now()))
        handler_button_choose_time_period(update, context, user)
    elif request == '{}all_time'.format(prefix_query_statistics):
        graph_controller.update_time_period(get_lifetime_user(user, datetime.datetime.now()))
        handler_button_choose_time_period(update, context, user)
    elif request == '{}back'.format(prefix_query_statistics):
        media_object = InputMediaPhoto(open(graph_controller.path_to_current_graph, 'rb'))
        bot.edit_message_media(chat_id=update.callback_query.message.chat_id,
                               message_id=update.callback_query.message.message_id,
                               media=media_object,
                               reply_markup=reply_main_keyboard)


def handler_button_choose_time_period(update, context, user):
    graph_controller = context.user_data['statistics']
    type_transactions = graph_controller.type_transactions
    data, labels = get_transactions_for_graph_by_type(session, user, type_transactions, graph_controller.time_period)
    path_to_graph = make_pie_graph(data, labels, graph_controller.time_period,
                                   graph_controller.type_transactions)
    media_object = InputMediaPhoto(open(path_to_graph, 'rb'))
    graph_controller.update_path_to_current_graph(path_to_graph)
    bot.edit_message_media(chat_id=update.callback_query.message.chat_id,
                           message_id=update.callback_query.message.message_id,
                           media=media_object,
                           reply_markup=reply_keyboard_choose_time_period)


def handler_button_choose_type_transactions(update, context, user):
    graph_controller = context.user_data['statistics']
    type_transactions = graph_controller.type_transactions
    data, labels = get_transactions_for_graph_by_type(session, user, type_transactions, graph_controller.time_period)
    path_to_graph = make_pie_graph(data, labels, graph_controller.time_period,
                                   graph_controller.type_transactions)
    graph_controller.update_path_to_current_graph(path_to_graph)
    media_object = InputMediaPhoto(open(path_to_graph, 'rb'))
    bot.edit_message_media(chat_id=update.callback_query.message.chat_id,
                           message_id=update.callback_query.message.message_id,
                           media=media_object,
                           reply_markup=reply_main_keyboard)
