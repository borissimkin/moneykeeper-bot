from telegram import ReplyKeyboardMarkup

from bot.buttons import Buttons
from bot.conversations.edit_categories.category_manager import CategoryManager
from bot.utils import add_button_exit, add_buttons_exit_and_back


def make_keyboard_menu_manage_categories(session, telegram_user_id, category_manager: CategoryManager):
    if category_manager.check_any_categories(session, telegram_user_id):
        keyboard = ReplyKeyboardMarkup(add_buttons_exit_and_back([[Buttons.add, Buttons.edit, Buttons.delete]]))
    else:
        keyboard = ReplyKeyboardMarkup(add_buttons_exit_and_back([[Buttons.add]]))
    return keyboard


class Keyboards:
    earning_or_consumption = ReplyKeyboardMarkup(add_button_exit([[Buttons.earning, Buttons.consumption]]),
                                                 resize_keyboard=True)
