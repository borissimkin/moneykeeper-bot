import datetime

import telegram
from telegram.ext import CallbackContext

from bot import bot, config
from bot.commands.export_database import send_database
from bot.commands.today import make_text_today
from bot.job_queue.results import make_text_week_results, is_time_to_week_results
from bot.models import User, session_scope
from bot.utils import log_job_queue


@log_job_queue
def job_results(context: CallbackContext):
    now = datetime.datetime.now()
    with session_scope() as session:
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


@log_job_queue
def job_backup_database(context: CallbackContext):
    if datetime.datetime.now().weekday() != 6:
        return
    with session_scope() as session:
        admin_users = session.query(User).filter(
            User.telegram_user_id.in_(config['admin_list'])
        ).all()
        for user in admin_users:
            send_database(user.telegram_user_id)


