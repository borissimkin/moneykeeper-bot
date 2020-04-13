import datetime

import telegram
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, CallbackContext, MessageHandler, Filters

from bot import config, bot, session
from bot.buttons import Buttons
from bot.conversations.limits.keyboards import get_keyboard_main_menu, keyboard_choose_type_limit, text_button_daily, \
    text_button_weekly, text_button_monthly, get_keyboard_category_limit, text_button_general_category, \
    make_keyboard_choose_limits, keyboard_choose_action_edit, text_button_type, text_button_category, \
    text_button_amount_money
from bot.conversations.limits.messages import text_timeout, text_exit_point, text_main_menu, text_choose_type_limit, \
    text_choose_category, text_to_write_money, text_error_write_money, text_success_add_limit, \
    make_text_and_dict_limits, text_to_edit_limit, text_choose_edit_type, text_edit_type_success, \
    text_choose_edit_category, get_text_limit_category, text_edit_category_success, text_edit_amount_money_success, \
    text_choose_limit_to_edit
from bot.conversations.limits.states import States
from bot.keyboards import keyboard_confirm
from bot.models import Limit, User, TypeLimit, CategoryConsumption
from bot.utils import log_handler, update_username, update_activity, clear_user_data, exit_dialog, back, \
    add_button_back, add_buttons_exit_and_back


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
        return to_edit_limit(update, context)
    elif update.message.text == Buttons.delete:
        ...


def to_edit_limit(update: Update, context: CallbackContext):
    context.user_data['back_func'] = to_main_menu
    user = User.get_user_by_telegram_user_id(session, update.message.from_user.id)
    limits = session.query(Limit).filter(
        Limit.user_id == user.id
    ).all()
    text, ids_limits = make_text_and_dict_limits(session, limits)
    context.user_data['ids_limits'] = ids_limits
    update.message.reply_text(text=text_choose_limit_to_edit())
    update.message.reply_text(text=text,
                              reply_markup=make_keyboard_choose_limits(ids_limits),
                              parse_mode=telegram.ParseMode.HTML)
    return States.TO_CHOOSE_EDIT_LIMIT


@back
@exit_dialog
def handler_choose_limit_to_edit(update: Update, context: CallbackContext):
    ids_limits = context.user_data['ids_limits']
    if int(update.message.text) in list(ids_limits.keys()):
        context.user_data['id_limit_to_edit'] = int(update.message.text)
        return to_choose_action_edit(update, context)


def to_choose_action_edit(update, context):
    context.user_data['back_func'] = to_edit_limit
    limit = session.query(Limit).get(context.user_data['id_limit_to_edit'])
    update.message.reply_text(text=text_to_edit_limit(session, limit),
                              reply_markup=keyboard_choose_action_edit,
                              parse_mode=telegram.ParseMode.HTML)
    return States.TO_CHOOSE_EDIT_ACTION


@exit_dialog
@back
def handler_choose_action_edit(update, context):
    text = update.message.text
    if text == text_button_type:
        return to_edit_type(update, context)
    elif text == text_button_category:
        return to_edit_category(update, context)
    elif text == text_button_amount_money:
        return to_edit_amount_money(update, context)


def to_edit_amount_money(update, context):
    context.user_data['back_func'] = to_choose_action_edit
    update.message.reply_text(text=text_to_write_money(),
                              reply_markup=ReplyKeyboardMarkup(add_buttons_exit_and_back([]),
                                                               resize_keyboard=True)
                              )
    return States.TO_EDIT_WRITE_MONEY


@exit_dialog
@back
def handler_edit_write_money(update, context):
    text = update.message.text
    try:
        context.user_data['amount_money'] = float(text)
    except ValueError:
        update.message.reply_text(text=text_error_write_money())
        return States.TO_EDIT_WRITE_MONEY
    return edit_amount_money(update, context)


def edit_amount_money(update, context):
    limit_to_edit = session.query(Limit).get(context.user_data['id_limit_to_edit'])
    old_amount_money = limit_to_edit.amount_money
    new_amount_money = context.user_data['amount_money']
    limit_to_edit.amount_money = new_amount_money
    session.commit()
    update.message.reply_text(text=text_edit_amount_money_success(old_amount_money, new_amount_money),
                              parse_mode=telegram.ParseMode.HTML)
    return to_choose_action_edit(update, context)


def to_edit_category(update, context):
    context.user_data['back_func'] = to_choose_action_edit
    user = User.get_user_by_telegram_user_id(session, update.message.from_user.id)
    categories = session.query(CategoryConsumption).filter(
        CategoryConsumption.user_id == user.id
    ).all()
    update.message.reply_text(text=text_choose_edit_category(),
                              reply_markup=get_keyboard_category_limit(categories))
    return States.TO_EDIT_CATEGORY


@exit_dialog
@back
def handler_edit_category(update, context):
    text = update.message.text
    user = User.get_user_by_telegram_user_id(session, update.message.from_user.id)
    if text == text_button_general_category:
        context.user_data['category_limit'] = None
        return edit_category(update, context)
    elif text in CategoryConsumption.get_all_categories_by_text(session, user.id):
        context.user_data['category_limit'] = update.message.text
        return edit_category(update, context)


def edit_category(update, context):
    user = User.get_user_by_telegram_user_id(session, update.message.from_user.id)
    limit_to_edit = session.query(Limit).get(context.user_data['id_limit_to_edit'])
    old_category = get_text_limit_category(session, limit_to_edit)
    new_category = 'Общий' if context.user_data['category_limit'] is None else context.user_data['category_limit']
    if context.user_data['category_limit'] is None:
        limit_to_edit.category_id = None
    else:
        category = session.query(CategoryConsumption).filter(
            CategoryConsumption.user_id == user.id,
            CategoryConsumption.category == context.user_data['category_limit']
        ).first()
        limit_to_edit.category_id = category.id
    session.commit()
    update.message.reply_text(text=text_edit_category_success(old_category, new_category),
                              parse_mode=telegram.ParseMode.HTML)
    return to_choose_action_edit(update, context)


def to_edit_type(update, context):
    context.user_data['back_func'] = to_choose_action_edit
    update.message.reply_text(text=text_choose_edit_type(),
                              reply_markup=keyboard_choose_type_limit)
    return States.TO_EDIT_TYPE


@exit_dialog
@back
def handler_edit_type(update, context):
    text = update.message.text
    if text == text_button_daily:
        context.user_data['new_type'] = TypeLimit.DAILY
        return edit_type_limit(update, context)
    elif text == text_button_weekly:
        context.user_data['new_type'] = TypeLimit.WEEKLY
        return edit_type_limit(update, context)
    elif text == text_button_monthly:
        context.user_data['new_type'] = TypeLimit.MONTHLY
        return edit_type_limit(update, context)


def edit_type_limit(update, context):
    limit_to_edit = session.query(Limit).get(context.user_data['id_limit_to_edit'])
    old_type = TypeLimit.text_type(limit_to_edit.type_limit)
    new_type = TypeLimit.text_type(context.user_data['new_type'].value)
    limit_to_edit.type_limit = context.user_data['new_type'].value
    session.commit()
    update.message.reply_text(text=text_edit_type_success(old_type, new_type),
                              parse_mode=telegram.ParseMode.HTML)
    return to_choose_action_edit(update, context)


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
                                                          pass_user_data=True)],
        States.TO_CHOOSE_EDIT_LIMIT: [MessageHandler(Filters.text,
                                                     handler_choose_limit_to_edit,
                                                     pass_user_data=True)],
        States.TO_CHOOSE_EDIT_ACTION: [MessageHandler(Filters.text,
                                                      handler_choose_action_edit,
                                                      pass_user_data=True)],
        States.TO_EDIT_TYPE: [MessageHandler(Filters.text,
                                             handler_edit_type,
                                             pass_user_data=True)],
        States.TO_EDIT_CATEGORY: [MessageHandler(Filters.text,
                                                 handler_edit_category,
                                                 pass_user_data=True)],
        States.TO_EDIT_WRITE_MONEY: [MessageHandler(Filters.text,
                                                    handler_edit_write_money,
                                                    pass_user_data=True)],

    },
    conversation_timeout=config['conversations']['timeout'],
    fallbacks=[CommandHandler('cancel_limits', exit_point)],
    allow_reentry=True,

    name="limits",
)
