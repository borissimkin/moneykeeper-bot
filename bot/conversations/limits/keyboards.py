from telegram import ReplyKeyboardMarkup

from bot import config
from bot.buttons import Buttons
from bot.keyboards import make_buttons_for_choose_category, row_is_full
from bot.utils import add_button_exit, add_buttons_exit_and_back

text_button_daily = 'Суточный'
text_button_weekly = 'Недельный'
text_button_monthly = 'Месячный'
text_button_general_category = 'По всем категориям'
text_button_type = 'Тип'
text_button_category = 'Категория'
text_button_amount_money = 'Количество денег'

keyboard_main_menu_limits_exist = ReplyKeyboardMarkup(add_button_exit([[Buttons.add, Buttons.delete],
                                                                       [Buttons.edit]]), resize_keyboard=True)

keyboard_main_menu_limits_non_exist = ReplyKeyboardMarkup(add_button_exit([[Buttons.add]]), resize_keyboard=True)


keyboard_choose_type_limit = ReplyKeyboardMarkup(add_buttons_exit_and_back([[text_button_daily, text_button_weekly],
                                                                            [text_button_monthly]]),
                                                 resize_keyboard=True)

keyboard_choose_action_edit = ReplyKeyboardMarkup(add_buttons_exit_and_back([[text_button_type, text_button_category,
                                                                             text_button_amount_money]]),
                                                  resize_keyboard=True)


def get_keyboard_category_limit(categories):
    keyboard_categories = make_buttons_for_choose_category(config['buttons_per_row'], categories)
    keyboard_categories.insert(0, [text_button_general_category])
    return ReplyKeyboardMarkup(add_buttons_exit_and_back(keyboard_categories),
                               resize_keyboard=True)


def get_keyboard_main_menu(limits):
    return keyboard_main_menu_limits_exist if limits else keyboard_main_menu_limits_non_exist


def make_keyboard_choose_limits(ids_limits: dict):
    buttons = make_buttons_for_choose_limits(4, list(ids_limits.keys()))
    return ReplyKeyboardMarkup(add_buttons_exit_and_back(buttons), resize_keyboard=True)


def make_buttons_for_choose_limits(count_buttons_per_row, ids):
    buttons = []
    row = []
    for index, category in enumerate(ids):
        row.append(str(category))
        if row_is_full(index, count_buttons_per_row):
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return buttons


