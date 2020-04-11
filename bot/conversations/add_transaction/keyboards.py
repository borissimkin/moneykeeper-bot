from telegram import ReplyKeyboardMarkup

from bot.buttons import Buttons
from bot.utils import add_button_exit

keyboard_choose_type_transaction = ReplyKeyboardMarkup(add_button_exit([[Buttons.earning, Buttons.consumption]]),
                                                       resize_keyboard=True)


buttons_days = [Buttons.yesterday, Buttons.today]