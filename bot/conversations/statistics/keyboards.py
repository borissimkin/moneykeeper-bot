from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.buttons import Buttons
from bot.conversations.statistics import prefix_query_statistics

main_keyboard = [[InlineKeyboardButton(Buttons.earnings, callback_data='{}earnings'.format(prefix_query_statistics)),
                  InlineKeyboardButton(Buttons.consumptions, callback_data='{}consumptions'.format(prefix_query_statistics))]]
reply_main_keyboard = InlineKeyboardMarkup(main_keyboard)
