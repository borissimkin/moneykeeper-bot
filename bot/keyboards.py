from telegram import ReplyKeyboardMarkup

from bot.buttons import text_button_confirm, text_button_back, text_button_exit

keyboard_confirm = ReplyKeyboardMarkup([[text_button_confirm],
                                        [text_button_back, text_button_exit]], resize_keyboard=True)

keyboard_exit = ReplyKeyboardMarkup([[text_button_exit]], resize_keyboard=True)
