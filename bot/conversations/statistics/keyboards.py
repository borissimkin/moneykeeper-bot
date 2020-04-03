from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot.buttons import Buttons
from bot.conversations.statistics import prefix_query_statistics

text_button_today = 'Сегодня'
text_button_yesterday = 'Вчера'
text_button_current_week = 'Текущая неделя'
text_button_current_month = 'Текущий месяц'
text_button_all_time = 'Все время'
text_button_choose_time_period = 'Выбрать период времени'
text_button_specify_time_period = 'Указать временной период'

main_keyboard = [[InlineKeyboardButton(text_button_choose_time_period,
                                       callback_data='{}time_period'.format(prefix_query_statistics))],
                 [InlineKeyboardButton(Buttons.earnings, callback_data='{}earnings'.format(prefix_query_statistics)),
                  InlineKeyboardButton(Buttons.consumptions,
                                       callback_data='{}consumptions'.format(prefix_query_statistics))]]
reply_main_keyboard = InlineKeyboardMarkup(main_keyboard)


keyboard_choose_time_period = [[InlineKeyboardButton(text_button_specify_time_period,
                                                     callback_data='{}specify_time_period'.format(
                                                         prefix_query_statistics))],
                               [InlineKeyboardButton(text_button_yesterday,
                                                     callback_data='{}yesterday'.format(prefix_query_statistics)),
                                InlineKeyboardButton(text_button_today,
                                                     callback_data='{}today'.format(prefix_query_statistics))],
                               [InlineKeyboardButton(text_button_current_week,
                                                     callback_data='{}current_week'.format(prefix_query_statistics)),
                                InlineKeyboardButton(text_button_current_month,
                                                     callback_data='{}current_month'.format(prefix_query_statistics))],
                               [InlineKeyboardButton(text_button_all_time,
                                                     callback_data='{}all_time'.format(prefix_query_statistics))],
                               [InlineKeyboardButton(Buttons.back,
                                                     callback_data='{}back'.format(prefix_query_statistics))]]

reply_keyboard_choose_time_period = InlineKeyboardMarkup(keyboard_choose_time_period)
