from telegram import ReplyKeyboardMarkup

from bot.buttons import Buttons

keyboard_confirm = ReplyKeyboardMarkup([[Buttons.confirm],
                                        [Buttons.back, Buttons.exit]], resize_keyboard=True)

keyboard_exit = ReplyKeyboardMarkup([[Buttons.exit]], resize_keyboard=True)


def make_buttons_for_choose_category(count_buttons_per_row, categories):
    buttons = []
    row = []
    for index, category in enumerate(categories):
        row.append(category.category)
        if row_is_full(index, count_buttons_per_row):
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return buttons


def row_is_full(index, count_buttons_per_row):
    if (index + 1) % count_buttons_per_row == 0 and index > 0:
        return True
    return False
