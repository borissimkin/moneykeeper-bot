import telegram
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, MessageHandler, Filters, CallbackContext, CommandHandler

from bot import bot, config
from bot.keyboards import keyboard_confirm, keyboard_exit, make_buttons_for_choose_category
from bot.buttons import Buttons
from bot.conversations.add_consumption.messages import text_to_choose_category, text_exit_point, text_timeout, \
     text_success_add_consumption, text_error_enter_amount_money, text_to_write_money
from bot.messages import text_confirm_add_transaction
from bot.models import CategoryConsumption, session, User, Consumption
from bot.utils import exit_dialog, back, update_username, update_activity, add_button_cancel, add_buttons_exit_and_back, \
    clear_user_data, log_handler
from .states import States


@log_handler
@update_username
@update_activity
def entry_point(update: Update, context: CallbackContext):
    context.user_data['exit_func'] = exit_point
    return to_write_money(update, context)


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


@back
@exit_dialog
def handler_to_choose_category(update: Update, context: CallbackContext):
    text = update.message.text
    user = session.query(User).filter(User.telegram_user_id == update.message.from_user.id).first()
    right_answers = CategoryConsumption.get_all_categories_by_text(session, user.id)
    if text in right_answers:
        context.user_data['category_consumption'] = text
        return to_confirm_add_consumption(update, context)
    else:
        ...  # предложить создать категорию?


def to_confirm_add_consumption(update: Update, context: CallbackContext):
    context.user_data['back_func'] = to_choose_category
    bot.send_message(chat_id=update.message.from_user.id,
                     text=text_confirm_add_transaction(context.user_data['amount_money_consumption'],
                                                       context.user_data['category_consumption']),
                     reply_markup=keyboard_confirm,
                     parse_mode=telegram.ParseMode.HTML)
    return States.TO_CONFIRM_ADD_CONSUMPTION


def to_write_money(update, context):
    bot.send_message(chat_id=update.message.from_user.id,
                     text=text_to_write_money(),
                     reply_markup=keyboard_exit)
    return States.TO_WRITE_AMOUNT_MONEY


@exit_dialog
def handler_write_money(update: Update, context: CallbackContext):
    try:
        amount_money = float(update.message.text)
    except ValueError:
        send_message_error_enter_amount_money(update.message.from_user.id)
        return States.TO_WRITE_AMOUNT_MONEY
    context.user_data['amount_money_consumption'] = amount_money
    return to_choose_category(update, context)


def to_choose_category(update, context):
    context.user_data['back_func'] = to_write_money
    send_message_to_choose_category(update.message.from_user.id,
                                    context.user_data['amount_money_consumption'])
    return States.TO_CHOOSE_CATEGORY


def send_message_error_enter_amount_money(telegram_user_id):
    bot.send_message(chat_id=telegram_user_id,
                     text=text_error_enter_amount_money(),
                     parse_mode=telegram.ParseMode.HTML)


def send_message_to_choose_category(telegram_user_id, amount_money):
    user = session.query(User).filter(User.telegram_user_id == telegram_user_id).first()
    buttons = make_buttons_for_choose_category(count_buttons_per_row=config['buttons_per_row'],
                                               categories=CategoryConsumption.get_all_categories(session, user.id))
    buttons = add_buttons_exit_and_back(buttons)
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    bot.send_message(chat_id=telegram_user_id,
                     text=text_to_choose_category(amount_money),
                     parse_mode=telegram.ParseMode.HTML,
                     reply_markup=keyboard)


@back
@exit_dialog
def handler_confirm_add_consumption(update: Update, context: CallbackContext):
    if update.message.text == Buttons.confirm:
        add_consumption_in_db(session,
                              update.message.from_user.id,
                              context.user_data['amount_money_consumption'],
                              context.user_data['category_consumption'])
        bot.send_message(chat_id=update.message.from_user.id,
                         text=text_success_add_consumption(),
                         reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END


def add_consumption_in_db(session, telegram_user_id, amount_money, category_text):
    user = session.query(User).filter(User.telegram_user_id == telegram_user_id).first()
    category = session.query(CategoryConsumption).filter(CategoryConsumption.category == category_text,
                                                         CategoryConsumption.user_id == user.id).first()
    session.add(Consumption(user_id=user.id,
                            category_id=category.id,
                            amount_money=amount_money))
    session.commit()


add_consumption = ConversationHandler(
    entry_points=[
        CommandHandler('add_consumption',
                       entry_point,
                       pass_user_data=True)],
    states={
        ConversationHandler.TIMEOUT: [MessageHandler(Filters.all,
                                                     handler_timeout)],
        States.TO_CHOOSE_CATEGORY: [MessageHandler(Filters.text,
                                                   handler_to_choose_category,
                                                   pass_user_data=True)],

        States.TO_WRITE_AMOUNT_MONEY: [MessageHandler(Filters.text,
                                                      handler_write_money,
                                                      pass_user_data=True)],

        States.TO_CONFIRM_ADD_CONSUMPTION: [MessageHandler(Filters.text,
                                                           handler_confirm_add_consumption,
                                                           pass_user_data=True)],


    },
    conversation_timeout=config['conversations']['timeout'],
    fallbacks=[CommandHandler('exit_point', exit_point)],

    name="add_consumption",
)



