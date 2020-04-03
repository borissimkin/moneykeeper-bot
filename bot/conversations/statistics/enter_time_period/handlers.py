import telegram
from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, CallbackContext, MessageHandler, Filters, \
    CallbackQueryHandler

from bot import config, bot, session
from bot.buttons import Buttons
from bot.models import User
from bot.utils import add_button_cancel
from .messages import text_exit_point, text_to_choose_time_period, text_timeout, text_wrong_enter_time, \
    text_success_change_time_period
from .states import States
from .. import prefix_query_statistics
from ..handlers import handler_button_choose_time_period
from ..utils import check_right_time_period


def entry_point(update: Update, context: CallbackContext):
    context.user_data['temp_callback_query'] = update.callback_query
    bot.send_message(chat_id=update.callback_query.message.chat_id,
                     text=text_to_choose_time_period(),
                     reply_markup=ReplyKeyboardMarkup(add_button_cancel([]),
                                                      resize_keyboard=True),
                     parse_mode=telegram.ParseMode.HTML)
    return States.TO_ENTER_TIME_PERIOD


def handler_timeout(update: Update, context: CallbackContext):
    user_id = context.effective_user['id']
    bot.send_message(chat_id=user_id,
                     text=text_timeout(),
                     reply_markup=ReplyKeyboardRemove(),
                     parse_mode=telegram.ParseMode.HTML)


def exit_point(update: Update, context: CallbackContext):
    bot.send_message(chat_id=update.message.chat.id,
                     text=text_exit_point(),
                     parse_mode=telegram.ParseMode.HTML,
                     reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def handler_to_enter_time_period(update: Update, context: CallbackContext):
    text = update.message.text
    if text == Buttons.cancel:
        return exit_point(update, context)
    if not check_right_time_period(text):
        update.message.reply_text(text=text_wrong_enter_time())
        return States.TO_ENTER_TIME_PERIOD
    graph_controller = context.user_data['statistics']
    graph_controller.update_time_period(text)
    user = session.query(User).filter(User.telegram_user_id == update.message.from_user.id).first()
    update.callback_query = context.user_data['temp_callback_query']
    handler_button_choose_time_period(update, context, user)
    context.user_data.pop('temp_callback_query')
    bot.send_message(chat_id=update.message.from_user.id,
                     text=text_success_change_time_period(),
                     reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


time_period = ConversationHandler(
    entry_points=[CallbackQueryHandler(entry_point,
                                       pattern='{}specify_time_period'.format(prefix_query_statistics))],

    states={
        ConversationHandler.TIMEOUT: [MessageHandler(Filters.all,
                                                     handler_timeout)],
        States.TO_ENTER_TIME_PERIOD: [MessageHandler(Filters.text,
                                                     handler_to_enter_time_period,
                                                     pass_user_data=True)],

    },
    conversation_timeout=config['conversations']['timeout'],
    fallbacks=[CommandHandler('exit_point', exit_point)],

    name="specify_time_period",
)
