import datetime

from bot.models import User, Earning, Consumption
from bot.conversations.statistics.utils import total_amount_money
from bot.utils import ruble_declension


def make_text_week_results(session, now, user: User):
    consumptions = session.query(Consumption).filter(
        Consumption.user_id == user.id,
        Consumption.time_creation >= now - datetime.timedelta(days=7)
    )
    total_consumption = total_amount_money(consumptions)
    return 'За прошедшую неделю вы потратили <b>{} {}</b>.'.format(total_consumption,
                                                                   ruble_declension(int(total_consumption)))


def is_time_to_week_results(now):
    return True if now.weekday() == 6 else False
