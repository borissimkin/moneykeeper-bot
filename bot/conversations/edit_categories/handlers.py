import telegram
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, CallbackContext, CommandHandler, Filters, MessageHandler

from bot import config, bot
from bot.buttons import Buttons
from bot.conversations.edit_categories.consumption_category_manager import ConsumptionCategoryManager
from bot.conversations.edit_categories.earning_category_manager import EarningCategoryManager
from bot.conversations.edit_categories.keyboards import Keyboards, make_keyboard_menu_manage_categories
from bot.conversations.edit_categories.messages import text_choose_earning_or_consumption, text_exit_point, \
    text_timeout, TextMenuManageCategories, text_add_category, text_warning_delete_category, text_delete_category, \
    text_edit_category, text_write_edit_category, text_confirm_edit_category
from bot.conversations.edit_categories.states import States
from bot.keyboards import keyboard_confirm, make_buttons_for_choose_category
from bot.models import session
from bot.utils import exit_dialog, update_username, update_activity, clear_user_data, back, add_buttons_exit_and_back


@update_username
@update_activity
def entry_point(update: Update, context: CallbackContext):
    context.user_data['exit_func'] = exit_point
    return to_choose_earning_or_consumption(update, context)


@clear_user_data
def exit_point(update: Update, context: CallbackContext):
    bot.send_message(chat_id=update.message.from_user.id,
                     text=text_exit_point(),
                     reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


@clear_user_data
def handler_timeout(update: Update, context: CallbackContext):
    bot.send_message(chat_id=update.message.from_user.id,
                     text=text_timeout(),
                     reply_markup=ReplyKeyboardRemove())


def to_choose_earning_or_consumption(update: Update, context: CallbackContext):
    bot.send_message(chat_id=update.message.from_user.id,
                     text=text_choose_earning_or_consumption(),
                     reply_markup=Keyboards.earning_or_consumption)
    return States.TO_CHOOSE_EARNING_OR_CONSUMPTION


def to_menu_manage_categories(update, context):
    context.user_data['back_func'] = to_choose_earning_or_consumption
    text = TextMenuManageCategories.make_text_menu_manage_categories(session, update.message.from_user.id,
                                                                     context.user_data['category_manager'])
    keyboard = make_keyboard_menu_manage_categories(session, update.message.from_user.id,
                                                    context.user_data['category_manager'])
    bot.send_message(chat_id=update.message.from_user.id,
                     text=text,
                     reply_markup=keyboard,
                     parse_mode=telegram.ParseMode.HTML)
    return States.TO_MENU_MANAGE_CATEGORIES


@exit_dialog
def handler_choose_earning_or_consumption(update: Update, context: CallbackContext):
    if update.message.text == Buttons.earning:
        context.user_data['category_manager'] = EarningCategoryManager
        return to_menu_manage_categories(update, context)
    elif update.message.text == Buttons.consumption:
        context.user_data['category_manager'] = ConsumptionCategoryManager
        return to_menu_manage_categories(update, context)


@exit_dialog
@back
def handler_menu_manage_categories(update: Update, context: CallbackContext):
    if update.message.text == Buttons.add:
        return to_add_category(update, context)
    elif update.message.text == Buttons.edit:
        return to_edit_category(update, context)
    elif update.message.text == Buttons.delete:
        return to_delete_category(update, context)


def to_add_category(update: Update, context: CallbackContext):
    context.user_data['back_func'] = to_menu_manage_categories
    bot.send_message(chat_id=update.message.from_user.id,
                     text=text_add_category(),
                     reply_markup=ReplyKeyboardMarkup(add_buttons_exit_and_back([]),
                                                      resize_keyboard=True))
    return States.TO_ADD_CATEGORY


def to_confirm_add_category(update: Update, context: CallbackContext):
    context.user_data['back_func'] = to_add_category
    bot.send_message(chat_id=update.message.from_user.id,
                     text=context.user_data['category_manager'].text_confirm_add_category(
                         context.user_data['add_category']
                     ),
                     reply_markup=keyboard_confirm,
                     parse_mode=telegram.ParseMode.HTML)
    return States.TO_CONFIRM_ADD_CATEGORY


@exit_dialog
@back
def handler_add_category(update: Update, context: CallbackContext):
    context.user_data['add_category'] = update.message.text
    return to_confirm_add_category(update, context)


@exit_dialog
@back
def handler_confirm_add_category(update: Update, context: CallbackContext):
    if update.message.text == Buttons.confirm:
        new_category = context.user_data['add_category']
        context.user_data['category_manager'].add_category_in_db(session,
                                                                 new_category,
                                                                 update.message.from_user.id)
        bot.send_message(chat_id=update.message.from_user.id,
                         text=context.user_data['category_manager'].text_success_add_category(new_category),
                         parse_mode=telegram.ParseMode.HTML,
                         reply_markup=ReplyKeyboardRemove())
        return entry_point(update, context)


def to_delete_category(update: Update, context: CallbackContext):
    context.user_data['back_func'] = to_menu_manage_categories
    bot.send_message(chat_id=update.message.from_user.id,
                     text=text_warning_delete_category(),
                     parse_mode=telegram.ParseMode.HTML)
    categories = context.user_data['category_manager'].get_all_categories(session,
                                                                          update.message.from_user.id)
    buttons = make_buttons_for_choose_category(config['buttons_per_row'],
                                               categories)
    bot.send_message(chat_id=update.message.from_user.id,
                     text=text_delete_category(session, update.message.from_user.id,
                                               context.user_data['category_manager']),
                     reply_markup=ReplyKeyboardMarkup(add_buttons_exit_and_back(buttons),
                                                      resize_keyboard=True),
                     parse_mode=telegram.ParseMode.HTML,
                     )
    return States.TO_DELETE_CATEGORY


@back
@exit_dialog
def handler_delete_category(update: Update, context: CallbackContext):
    categories = context.user_data['category_manager'].get_all_categories_by_text(session,
                                                                                  update.message.from_user.id)
    answer = update.message.text
    if answer in categories:
        context.user_data['delete_category'] = answer
        return to_confirm_delete_category(update, context)


def to_confirm_delete_category(update: Update, context: CallbackContext):
    context.user_data['back_func'] = to_delete_category
    bot.send_message(chat_id=update.message.from_user.id,
                     text=context.user_data['category_manager'].text_confirm_delete_category(
                         context.user_data['delete_category']),
                     reply_markup=keyboard_confirm,
                     parse_mode=telegram.ParseMode.HTML)
    bot.send_message(chat_id=update.message.from_user.id,
                     text=text_warning_delete_category(),
                     parse_mode=telegram.ParseMode.HTML)
    return States.TO_CONFIRM_DELETE_CATEGORY


def to_edit_category(update: Update, context: CallbackContext):
    context.user_data['back_func'] = to_menu_manage_categories
    categories = context.user_data['category_manager'].get_all_categories(session,
                                                                          update.message.from_user.id)
    buttons = make_buttons_for_choose_category(config['buttons_per_row'],
                                               categories)
    bot.send_message(chat_id=update.message.from_user.id,
                     text=text_edit_category(),
                     reply_markup=ReplyKeyboardMarkup(add_buttons_exit_and_back(buttons),
                                                      resize_keyboard=True),
                     parse_mode=telegram.ParseMode.HTML)
    return States.TO_EDIT_CATEGORY


@back
@exit_dialog
def handler_edit_category(update: Update, context: CallbackContext):
    categories = context.user_data['category_manager'].get_all_categories_by_text(session,
                                                                                  update.message.from_user.id)
    answer = update.message.text
    if answer in categories:
        context.user_data['old_edit_category'] = answer
        return to_write_edit_category(update, context)


def to_write_edit_category(update: Update, context: CallbackContext):
    context.user_data['back_func'] = to_edit_category
    bot.send_message(chat_id=update.message.from_user.id,
                     text=text_write_edit_category(context.user_data['old_edit_category']),
                     parse_mode=telegram.ParseMode.HTML,
                     reply_markup=ReplyKeyboardMarkup(add_buttons_exit_and_back([]),
                                                      resize_keyboard=True))
    return States.TO_WRITE_EDIT_CATEGORY


@exit_dialog
@back
def handler_write_edit_category(update: Update, context: CallbackContext):
    new_category = update.message.text
    context.user_data['new_edit_category'] = new_category
    return to_confirm_edit_category(update, context)


def to_confirm_edit_category(update: Update, context: CallbackContext):
    context.user_data['back_func'] = to_write_edit_category
    bot.send_message(chat_id=update.message.from_user.id,
                     text=text_confirm_edit_category(context.user_data['old_edit_category'],
                                                     context.user_data['new_edit_category']),
                     reply_markup=keyboard_confirm,
                     parse_mode=telegram.ParseMode.HTML)
    return States.TO_CONFIRM_EDIT_CATEGORY


@exit_dialog
@back
def handler_confirm_edit_category(update: Update, context: CallbackContext):
    if update.message.text == Buttons.confirm:
        context.user_data['category_manager'].edit_category_in_db(session, update.message.from_user.id,
                                                                  context.user_data['old_edit_category'],
                                                                  context.user_data['new_edit_category'])
        bot.send_message(chat_id=update.message.from_user.id,
                         text=context.user_data['category_manager'].text_success_edit_category(
                             context.user_data['old_edit_category'],
                             context.user_data['new_edit_category']),
                         reply_markup=ReplyKeyboardRemove(),
                         parse_mode=telegram.ParseMode.HTML)
        return entry_point(update, context)


@exit_dialog
@back
def handler_confirm_delete_category(update: Update, context: CallbackContext):
    if update.message.text == Buttons.confirm:
        context.user_data['category_manager'].delete_category_in_db(session,
                                                                    context.user_data['delete_category'],
                                                                    update.message.from_user.id)
        bot.send_message(chat_id=update.message.from_user.id,
                         text=context.user_data['category_manager'].text_success_delete(
                             context.user_data['delete_category']),
                         reply_markup=ReplyKeyboardRemove(),
                         parse_mode=telegram.ParseMode.HTML)
        return entry_point(update, context)


edit_categories = ConversationHandler(
    entry_points=[
        CommandHandler('edit_categories',
                       entry_point,
                       pass_user_data=True)],
    states={
        ConversationHandler.TIMEOUT: [MessageHandler(Filters.all,
                                                     handler_timeout)],
        States.TO_CHOOSE_EARNING_OR_CONSUMPTION: [MessageHandler(Filters.text,
                                                  handler_choose_earning_or_consumption,
                                                  pass_user_data=True)],

        States.TO_MENU_MANAGE_CATEGORIES: [MessageHandler(Filters.text,
                                                          handler_menu_manage_categories,
                                                          pass_user_data=True)],

        States.TO_ADD_CATEGORY: [MessageHandler(Filters.text,
                                                handler_add_category,
                                                pass_user_data=True)],

        States.TO_CONFIRM_ADD_CATEGORY: [MessageHandler(Filters.text,
                                                        handler_confirm_add_category,
                                                        pass_user_data=True)],

        States.TO_DELETE_CATEGORY: [MessageHandler(Filters.text,
                                                   handler_delete_category,
                                                   pass_user_data=True)],

        States.TO_CONFIRM_DELETE_CATEGORY: [MessageHandler(Filters.text,
                                                           handler_confirm_delete_category,
                                                           pass_user_data=True)],

        States.TO_EDIT_CATEGORY: [MessageHandler(Filters.text,
                                                 handler_edit_category,
                                                 pass_user_data=True)],
        States.TO_WRITE_EDIT_CATEGORY: [MessageHandler(Filters.text,
                                                       handler_write_edit_category,
                                                       pass_user_data=True)],

        States.TO_CONFIRM_EDIT_CATEGORY: [MessageHandler(Filters.text,
                                                         handler_confirm_edit_category,
                                                         pass_user_data=True)],


    },
    conversation_timeout=config['conversations']['timeout'],
    fallbacks=[CommandHandler('exit_point', exit_point)],

    name="edit_categories",
)

