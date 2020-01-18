import telegram
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, RegexHandler, MessageHandler, Filters, CallbackContext, CommandHandler

from bot import config, bot
from bot.buttons import Buttons
from bot.conversations.delete_transaction.consumption_deleter import ConsumptionDeleter
from bot.conversations.delete_transaction.earning_deleter import EarningDeleter
from bot.conversations.delete_transaction.messages import text_timeout
from bot.conversations.delete_transaction.states import States
from bot.conversations.delete_transaction.utils import message_has_delete_consumption, get_id_transaction
from bot.models import session
from bot.utils import exit_dialog, update_activity, update_username, clear_user_data, add_button_exit


@update_activity
@update_username
def entry_point(update: Update, context: CallbackContext):
    context.user_data['exit_func'] = exit_point
    if message_has_delete_consumption(update.message.text):
        context.user_data['transaction_deleter'] = ConsumptionDeleter(telegram_user_id=update.message.from_user.id,
                                                                      transaction_id=get_id_transaction(
                                                                          update.message.text),
                                                                      session=session)
    else:
        context.user_data['transaction_deleter'] = EarningDeleter(telegram_user_id=update.message.from_user.id,
                                                                  transaction_id=get_id_transaction(
                                                                      update.message.text),
                                                                  session=session)
    return to_confirm_delete_transaction(update, context)


@clear_user_data
def handler_timeout(update: Update, context: CallbackContext):
    bot.send_message(chat_id=update.message.from_user.id,
                     text=text_timeout(),
                     reply_markup=ReplyKeyboardRemove())


@clear_user_data
def exit_point(update: Update, context: CallbackContext):
    bot.send_message(chat_id=update.message.from_user.id,
                     text=text_timeout(),
                     reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def to_confirm_delete_transaction(update: Update, context: CallbackContext):
    if context.user_data['transaction_deleter'].check_exist_transaction():
        bot.send_message(chat_id=update.message.from_user.id,
                         text=context.user_data['transaction_deleter'].make_text_delete_transaction(),
                         reply_markup=ReplyKeyboardMarkup(add_button_exit([Buttons.confirm]),
                                                          resize_keyboard=True),
                         parse_mode=telegram.ParseMode.HTML)

        return States.TO_CONFIRM_DELETE_TRANSACTION

    bot.send_message(chat_id=update.message.from_user.id,
                     text=context.user_data['transaction_deleter'].text_error_id_transaction(),
                     )
    return exit_point(update, context)


@exit_dialog
def handler_confirm_delete_transaction(update: Update, context: CallbackContext):
    if update.message.text == Buttons.confirm:
        context.user_data['transaction_deleter'].delete_transaction()
        bot.send_message(chat_id=update.message.from_user.id,
                         text=context.user_data['transaction_deleter'].make_text_success_delete_transaction(),
                         reply_markup=ReplyKeyboardRemove(),
                         parse_mode=telegram.ParseMode.HTML)
        return entry_point(update, context)


delete_transaction = ConversationHandler(
    entry_points=[
        MessageHandler(Filters.regex('^(/del_e\\d{1,}|/del_c\\d{1,})$'),
                       entry_point,
                       pass_user_data=True)],
    states={
        ConversationHandler.TIMEOUT: [MessageHandler(Filters.all,
                                                     handler_timeout)],
        States.TO_CONFIRM_DELETE_TRANSACTION: [MessageHandler(Filters.text,
                                                              handler_confirm_delete_transaction,
                                                              pass_user_data=True)],
    },
    conversation_timeout=config['conversations']['timeout'],
    fallbacks=[CommandHandler('exit_point', exit_point)],

    name="delete_transaction",
)
