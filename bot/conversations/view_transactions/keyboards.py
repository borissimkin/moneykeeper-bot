from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.buttons import Buttons

prefix_command = 'view_transactions_'


main_keyboard = [
                [InlineKeyboardButton(Buttons.earnings, callback_data='{}earnings'.format(prefix_command)),
                 InlineKeyboardButton(Buttons.consumptions, callback_data='{}consumptions'.format(prefix_command))]]
reply_main_keyboard = InlineKeyboardMarkup(main_keyboard)


next_and_previous_keyboard = [InlineKeyboardButton(Buttons.previous, callback_data='{}previous'.format(prefix_command)),
                              InlineKeyboardButton(Buttons.next, callback_data='{}next'.format(prefix_command))]

next_keyboard = [InlineKeyboardButton(Buttons.next, callback_data='{}next'.format(prefix_command))]

previous_keyboard = [InlineKeyboardButton(Buttons.previous, callback_data='{}previous'.format(prefix_command))]




