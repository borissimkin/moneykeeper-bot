import datetime

import sqlalchemy

from bot.conversations.limits import emoji_alarm, emoji_warning, emoji_ok
from bot.conversations.statistics.utils import total_amount_money, get_current_week, get_current_month, \
    take_percentage_number
from bot.models import Consumption, TypeLimit


def current_amount_money_daily_limit_user(session, limit, now):
    if limit.category_id:
        consumptions = session.query(Consumption).filter(
            Consumption.user_id == limit.user_id,
            Consumption.category_id == limit.category_id,
            sqlalchemy.func.date(Consumption.time_creation) == now.date()
        ).all()
    else:
        consumptions = session.query(Consumption).filter(
            Consumption.user_id == limit.user_id,
            sqlalchemy.func.date(Consumption.time_creation) == now.date()
        ).all()
    return total_amount_money(consumptions)


def current_amount_money_weekly_limit_user(session, limit, now):
    interval = get_current_week(now)
    return current_amount_money_interval_limit_user(session, limit, interval)


def current_amount_money_monthly_limit_user(session, limit, now):
    interval = get_current_month(now)
    return current_amount_money_interval_limit_user(session, limit, interval)


def current_amount_money_interval_limit_user(session, limit, interval):
    interval = interval.replace(" ", "")
    start, end = interval.split('-')
    if limit.category_id:
        consumptions = session.query(Consumption).filter(
            Consumption.user_id == limit.user_id,
            Consumption.category_id == limit.category_id,
            sqlalchemy.func.date(Consumption.time_creation) >= datetime.datetime.strptime(start, '%d.%m.%Y').date(),
            sqlalchemy.func.date(Consumption.time_creation) <= datetime.datetime.strptime(end, '%d.%m.%Y').date()
        ).all()
    else:
        consumptions = session.query(Consumption).filter(
            Consumption.user_id == limit.user_id,
            sqlalchemy.func.date(Consumption.time_creation) >= datetime.datetime.strptime(start, '%d.%m.%Y').date(),
            sqlalchemy.func.date(Consumption.time_creation) <= datetime.datetime.strptime(end, '%d.%m.%Y').date()
        ).all()
    return total_amount_money(consumptions)


def get_emoji_for_limit(limit_amount_money, current_amount_money, percentage_to_warning):
    percentage_number = take_percentage_number(limit_amount_money, percentage_to_warning)
    if current_amount_money >= limit_amount_money:
        return emoji_alarm
    elif current_amount_money >= limit_amount_money - percentage_number:
        return emoji_warning
    else:
        return emoji_ok


def limits_has_this_type(limits, type_limit: int):
    return any(x.type_limit == type_limit for x in limits)
