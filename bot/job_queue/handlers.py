import datetime

import telegram
from telegram.ext import CallbackContext

from bot import bot
from bot.commands.today import make_text_today
from bot.job_queue.results import make_text_week_results, is_time_to_week_results
from bot.models import session, User


def job_results(context: CallbackContext):
    now = datetime.datetime.now()
    users = session.query(User).all()
    for user in users:
        today_results = make_text_today(session, now, user)
        bot.send_message(chat_id=user.telegram_user_id,
                         text=today_results,
                         parse_mode=telegram.ParseMode.HTML,)
        if is_time_to_week_results(now):
            week_results = make_text_week_results(session, now, user)
            bot.send_message(chat_id=user.telegram_user_id,
                             text=week_results,
                             parse_mode=telegram.ParseMode.HTML)
