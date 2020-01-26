import telegram
from telegram import Update
from telegram.ext import CallbackContext

from bot import config, bot
from bot.utils import log_handler

text_command = 'help'


@log_handler
def handler(update: Update, context: CallbackContext):
    telegram_user_id = update.message.from_user.id
    bot.send_message(chat_id=telegram_user_id,
                     text=make_text_help(telegram_user_id),
                     parse_mode=telegram.ParseMode.HTML)


def make_text_help(telegram_user_id):
    text = '{}\n\n{}\n\n'.format(get_welcome_text(),
                                 get_text_general_commands())
    if telegram_user_id in config['admin_list']:
        text += get_text_admin_commands()
    return text


def get_welcome_text():
    with open('info/welcome', mode='r', encoding='utf-8') as f_hello:
        return f_hello.read()


def get_text_general_commands():
    with open('info/commands', mode='r', encoding='utf-8') as f_commands:
        return f_commands.read()


def get_text_admin_commands():
    with open('info/admin_commands', mode='r', encoding='utf-8') as f_admin:
        return f_admin.read()