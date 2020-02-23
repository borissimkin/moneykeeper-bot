from copy import deepcopy

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.buttons import Buttons
from bot.conversations.view_transactions import prefix_query

main_keyboard = [[InlineKeyboardButton(Buttons.all, callback_data='{}all'.format(prefix_query)),
                  InlineKeyboardButton(Buttons.earnings, callback_data='{}earnings'.format(prefix_query)),
                  InlineKeyboardButton(Buttons.consumptions, callback_data='{}consumptions'.format(prefix_query))]]
reply_main_keyboard = InlineKeyboardMarkup(main_keyboard)


next_and_previous_keyboard = [InlineKeyboardButton(Buttons.previous, callback_data='{}previous'.format(prefix_query)),
                              InlineKeyboardButton(Buttons.next, callback_data='{}next'.format(prefix_query))]

next_keyboard = [InlineKeyboardButton(Buttons.next, callback_data='{}next'.format(prefix_query))]

previous_keyboard = [InlineKeyboardButton(Buttons.previous, callback_data='{}previous'.format(prefix_query))]


def get_keyboard(transactions_controller):
    new_keyboard = deepcopy(main_keyboard)
    if may_add_button_next(transactions_controller) and may_add_button_previous(transactions_controller):
        new_keyboard.insert(0, next_and_previous_keyboard)
    elif may_add_button_next(transactions_controller):
        new_keyboard.insert(0, next_keyboard)
    elif may_add_button_previous(transactions_controller):
        new_keyboard.insert(0, previous_keyboard)
    return InlineKeyboardMarkup(new_keyboard)


def may_add_button_next(transactions_controller):
    return True if transactions_controller.last_index_part < len(transactions_controller.transactions) else False


def may_add_button_previous(transactions_controller):
    return True if transactions_controller.first_index_part > 0 else False





