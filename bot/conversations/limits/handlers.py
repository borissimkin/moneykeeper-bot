import datetime

import telegram
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, CallbackContext, MessageHandler, Filters

from bot import config, bot, session
from bot.buttons import Buttons
from bot.conversations.limits.keyboards import get_keyboard_main_menu, keyboard_choose_type_limit, text_button_daily, \
    text_button_weekly, text_button_monthly, get_keyboard_category_limit, text_button_general_category
from bot.conversations.limits.messages import text_timeout, text_exit_point, text_main_menu, text_choose_type_limit, \
    text_choose_category, text_to_write_money, text_error_write_money, text_success_add_limit
from bot.conversations.limits.states import States
from bot.models import Limit, User, TypeLimit, CategoryConsumption
from bot.utils import log_handler, update_username, update_activity, clear_user_data, exit_dialog, back, add_button_back


@log_handler
@update_username
@update_activity
def entry_point(update: Update, context: CallbackContext):
    context.user_data['exit_func'] = exit_point
    return to_main_menu(update, context)


def to_main_menu(update, context):
    user = User.get_user_by_telegram_user_id(session, update.message.from_user.id)
    limits = session.query(Limit).filter(Limit.user_id == user.id).all()
    update.message.reply_text(text=text_main_menu(session, limits, datetime.datetime.now()),
                              reply_markup=get_keyboard_main_menu(limits),
                              parse_mode=telegram.ParseMode.HTML)
    return States.TO_MAIN_MENU


@exit_dialog
def handler_main_menu(update, context):
    if update.message.text == Buttons.add:
        return to_add_limit(update, context)
    elif update.message.text == Buttons.edit:
        ...
    elif update.message.text == Buttons.delete:
        ...


def to_add_limit(update: Update, context: CallbackContext):
    context.user_data['back_func'] = to_main_menu
    update.message.reply_text(text=text_choose_type_limit(),
                              reply_markup=keyboard_choose_type_limit,
                              parse_mode=telegram.ParseMode.HTML)
    return States.TO_CHOOSE_ADD_TYPE_LIMIT


@exit_dialog
@back
def handler_add_type_limit(update: Update, context: CallbackContext):
    if update.message.text == text_button_daily:
        context.user_data['type_limit'] = TypeLimit.DAILY
        return to_add_category(update, context)
    elif update.message.text == text_button_weekly:
        context.user_data['type_limit'] = TypeLimit.WEEKLY
        return to_add_category(update, context)
    elif update.message.text == text_button_monthly:
        context.user_data['type_limit'] = TypeLimit.MONTHLY
        return to_add_category(update, context)


def to_add_category(update: Update, context: CallbackContext):
    context.user_data['back_func'] = to_add_limit
    user = User.get_user_by_telegram_user_id(session, update.message.from_user.id)
    categories = CategoryConsumption.get_all_categories(session, user.id)
    update.message.reply_text(text=text_choose_category(),
                              reply_markup=get_keyboard_category_limit(categories),
                              parse_mode=telegram.ParseMode.HTML)
    return States.TO_CHOOSE_ADD_CATEGORY_LIMIT


@exit_dialog
@back
def handler_add_category(update: Update, context: CallbackContext):
    user = session.query(User).filter(User.telegram_user_id == update.message.from_user.id).first()
    if update.message.text == text_button_general_category:
        context.user_data['category_limit'] = None
        return to_add_amount_money(update, context)
    elif update.message.text in CategoryConsumption.get_all_categories_by_text(session, user.id):
        context.user_data['category_limit'] = update.message.text
        return to_add_amount_money(update, context)


def to_add_amount_money(update: Update, context: CallbackContext):
    context.user_data['back_func'] = to_add_category
    update.message.reply_text(text=text_to_write_money(),
                              reply_markup=ReplyKeyboardMarkup(add_button_back([]),
                                                               resize_keyboard=True),
                              parse_mode=telegram.ParseMode.HTML)
    return States.TO_ADD_WRITE_AMOUNT_MONEY


@exit_dialog
@back
def handler_add_write_money(update: Update, context: CallbackContext):
    text = update.message.text
    try:
        context.user_data['amount_money'] = float(text)
    except ValueError:
        update.message.reply_text(text=text_error_write_money())
        return States.TO_ADD_WRITE_AMOUNT_MONEY
    return add_limit_to_database(update, context)


def add_limit_to_database(update, context):
    user = User.get_user_by_telegram_user_id(session, update.message.from_user.id)
    type_limit = context.user_data['type_limit']
    if context.user_data['category_limit'] is None:
        category_limit = None
    else:
        category = session.query(CategoryConsumption).filter(
            CategoryConsumption.category == context.user_data['category_limit'],
            CategoryConsumption.user_id == user.id
        ).first()
        category_limit = category.id
    amount_money = context.user_data['amount_money']
    Limit.add(session, user_id=user.id, type_limit=type_limit.value, category_id=category_limit,
              amount_money=amount_money)
    update.message.reply_text(text=text_success_add_limit())
    return to_main_menu(update, context)


@clear_user_data
def handler_timeout(update: Update, context: CallbackContext):
    user_id = context.effective_user['id']
    bot.send_message(chat_id=user_id,
                     text=text_timeout(),
                     reply_markup=ReplyKeyboardRemove(),
                     parse_mode=telegram.ParseMode.HTML)


@clear_user_data
def exit_point(update: Update, context: CallbackContext):
    bot.send_message(chat_id=update.message.from_user.id,
                     text=text_exit_point(),
                     parse_mode=telegram.ParseMode.HTML,
                     reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


limits_conversation_handler = ConversationHandler(
    entry_points=[
        CommandHandler('limits',
                       entry_point,
                       pass_user_data=True)],
    states={
        ConversationHandler.TIMEOUT: [MessageHandler(Filters.all,
                                                     handler_timeout)],
        States.TO_MAIN_MENU: [MessageHandler(Filters.text,
                                             handler_main_menu,
                                             pass_user_data=True)],

        States.TO_CHOOSE_ADD_TYPE_LIMIT: [MessageHandler(Filters.text,
                                                         handler_add_type_limit,
                                                         pass_user_data=True)],

        States.TO_CHOOSE_ADD_CATEGORY_LIMIT: [MessageHandler(Filters.text,
                                                             handler_add_category,
                                                             pass_user_data=True)],

        States.TO_ADD_WRITE_AMOUNT_MONEY: [MessageHandler(Filters.text,
                                                          handler_add_write_money,
                                                          pass_user_data=True)]

    },
    conversation_timeout=config['conversations']['timeout'],
    fallbacks=[CommandHandler('cancel_limits', exit_point)],
    allow_reentry=True,

    name="limits",
)
