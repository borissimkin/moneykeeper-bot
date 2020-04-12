from telegram import ReplyKeyboardMarkup

from bot import config
from bot.buttons import Buttons
from bot.keyboards import make_buttons_for_choose_category
from bot.utils import add_button_exit, add_buttons_exit_and_back

text_button_daily = 'Суточный'
text_button_weekly = 'Недельный'
text_button_monthly = 'Месячный'
text_button_general_category = 'По всем категориям'

keyboard_main_menu_limits_exist = ReplyKeyboardMarkup(add_button_exit([[Buttons.add, Buttons.delete],
                                                                       [Buttons.edit]]), resize_keyboard=True)

keyboard_main_menu_limits_non_exist = ReplyKeyboardMarkup(add_button_exit([[Buttons.add]]), resize_keyboard=True)


keyboard_choose_type_limit = ReplyKeyboardMarkup(add_buttons_exit_and_back([[text_button_daily, text_button_weekly],
                                                                            [text_button_monthly]]),
                                                 resize_keyboard=True)


def get_keyboard_category_limit(categories):
    keyboard_categories = make_buttons_for_choose_category(config['buttons_per_row'], categories)
    keyboard_categories.insert(0, [text_button_general_category])
    return ReplyKeyboardMarkup(add_buttons_exit_and_back(keyboard_categories),
                               resize_keyboard=True)


def get_keyboard_main_menu(limits):
    return keyboard_main_menu_limits_exist if limits else keyboard_main_menu_limits_non_exist


