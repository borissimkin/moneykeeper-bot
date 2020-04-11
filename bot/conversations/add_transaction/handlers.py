import datetime

import telegram
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, MessageHandler, CommandHandler, ConversationHandler, Filters

from bot import bot, config, session
from bot.buttons import Buttons
from bot.conversations.add_transaction.consumption_adder import ConsumptionAdder
from bot.conversations.add_transaction.earning_adder import EarningAdder
from bot.conversations.add_transaction.keyboards import keyboard_choose_type_transaction, buttons_days
from bot.conversations.add_transaction.messages import text_timeout, text_exit_point, text_choose_type_transaction, \
    text_to_choose_date, text_error_choose_date
from bot.conversations.add_transaction.states import States
from bot.models import User
from bot.utils import log_handler, update_username, update_activity, clear_user_data, exit_dialog, \
    add_buttons_exit_and_back, back


@log_handler
@update_username
@update_activity
def entry_point(update: Update, context: CallbackContext):
    context.user_data['exit_func'] = exit_point
    return to_choose_type_transaction(update, context)


@clear_user_data
def exit_point(update: Update, context: CallbackContext):
    bot.send_message(chat_id=update.message.from_user.id,
                     text=text_exit_point(),
                     parse_mode=telegram.ParseMode.HTML,
                     reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


@clear_user_data
def handler_timeout(update: Update, context: CallbackContext):
    user_id = context.effective_user['id']
    bot.send_message(chat_id=user_id,
                     text=text_timeout(),
                     reply_markup=ReplyKeyboardRemove(),
                     parse_mode=telegram.ParseMode.HTML)


def to_choose_type_transaction(update: Update, context: CallbackContext):
    bot.send_message(chat_id=update.message.from_user.id,
                     text=text_choose_type_transaction(),
                     reply_markup=keyboard_choose_type_transaction,
                     parse_mode=telegram.ParseMode.HTML)
    return States.TO_CHOOSE_TYPE_TRANSACTION


@exit_dialog
def handler_choose_type_transaction(update: Update, context: CallbackContext):
    text = update.message.text
    user = session.query(User).filter(User.telegram_user_id == update.message.from_user.id).first()
    if text == Buttons.earning:
        context.user_data['transaction_adder'] = EarningAdder(user)
        return to_write_money(update, context)
    elif text == Buttons.consumption:
        context.user_data['transaction_adder'] = ConsumptionAdder(user)
        return to_write_money(update, context)


def to_write_money(update: Update, context: CallbackContext):
    context.user_data['back_func'] = to_choose_type_transaction
    transaction_adder = context.user_data['transaction_adder']
    bot.send_message(chat_id=update.message.from_user.id,
                     text=transaction_adder.text_to_write_money(),
                     reply_markup=ReplyKeyboardMarkup(add_buttons_exit_and_back([]),
                                                      resize_keyboard=True))
    return States.TO_WRITE_MONEY


@exit_dialog
@back
def handler_write_money(update: Update, context: CallbackContext):
    text = update.message.text
    try:
        context.user_data['amount_money'] = float(text)
    except ValueError:
        update.message.reply_text(text='Вы ошиблись в вводе, пожалуйста, попробуйте еще раз.')
        return to_write_money(update, context)
    return to_choose_category(update, context)


def to_choose_category(update: Update, context: CallbackContext):
    context.user_data['back_func'] = to_write_money
    transaction_adder = context.user_data['transaction_adder']
    keyboard = transaction_adder.get_keyboard_choose_categories(session)
    bot.send_message(chat_id=update.message.from_user.id,
                     text='Выберите категорию.',
                     reply_markup=keyboard,
                     parse_mode=telegram.ParseMode.HTML)
    return States.TO_CHOOSE_CATEGORY


@exit_dialog
@back
def handler_choose_category(update: Update, context: CallbackContext):
    text = update.message.text
    transaction_adder = context.user_data['transaction_adder']
    right_answers = transaction_adder.get_categories_by_text(session)
    if text in right_answers:
        context.user_data['category_transaction'] = text
        return to_choose_date(update, context)


def to_choose_date(update: Update, context: CallbackContext):
    context.user_data['back_func'] = to_choose_category
    bot.send_message(chat_id=update.message.from_user.id,
                     text=text_to_choose_date(),
                     reply_markup=ReplyKeyboardMarkup(add_buttons_exit_and_back([buttons_days]),
                                                      resize_keyboard=True),
                     parse_mode=telegram.ParseMode.HTML)
    return States.TO_CHOOSE_DATE


@exit_dialog
@back
def handler_choose_date(update: Update, context: CallbackContext):
    transaction_adder = context.user_data['transaction_adder']
    text = update.message.text
    text = text.replace(" ", "")
    if text in buttons_days:
        if text == Buttons.yesterday:
            date = datetime.datetime.now().date() - datetime.timedelta(days=1)
        else:
            date = datetime.datetime.now()
    else:
        try:
            date = datetime.datetime.strptime(text, "%d.%m.%Y")
        except ValueError:
            update.message.reply_text(text=text_error_choose_date(),
                                      parse_mode=telegram.ParseMode.HTML)
            return to_choose_date(update, context)
    transaction_adder.add_transaction(session,
                                      context.user_data['amount_money'],
                                      context.user_data['category_transaction'],
                                      date)
    bot.send_message(chat_id=update.message.from_user.id,
                     text=transaction_adder.text_success_add_transaction(),
                     parse_mode=telegram.ParseMode.HTML,)
    return to_choose_type_transaction(update, context)


add_transaction = ConversationHandler(
    entry_points=[
        CommandHandler('add_transaction',
                       entry_point,
                       pass_user_data=True)],
    states={
        ConversationHandler.TIMEOUT: [MessageHandler(Filters.all,
                                                     handler_timeout)],

        States.TO_CHOOSE_TYPE_TRANSACTION: [MessageHandler(Filters.text,
                                                           handler_choose_type_transaction,
                                                           pass_user_data=True)],

        States.TO_WRITE_MONEY: [MessageHandler(Filters.text,
                                               handler_write_money,
                                               pass_user_data=True)],

        States.TO_CHOOSE_CATEGORY: [MessageHandler(Filters.text,
                                                   handler_choose_category)],

        States.TO_CHOOSE_DATE: [MessageHandler(Filters.text,
                                               handler_choose_date)]

    },
    conversation_timeout=config['conversations']['timeout'],
    fallbacks=[CommandHandler('exit_point', exit_point)],

    name="add_transaction",
)
