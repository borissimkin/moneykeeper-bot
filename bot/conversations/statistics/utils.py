# -*- coding: utf-8 -*-
import datetime

import sqlalchemy

from bot.conversations.statistics.type_transacation_graph import TypeTransaction
from bot.models import User, Earning, Consumption, CategoryConsumption, CategoryEarning
from bot.utils import get_past_minutes_day


def get_earnings_today(session, now, user: User):
    today_minutes = get_past_minutes_day(now)
    earnings = session.query(Earning).filter(
        Earning.user_id == user.id,
        Earning.time_creation >= now - datetime.timedelta(minutes=today_minutes)).all()
    return earnings


def get_consumptions_today(session, now, user: User):
    today_minutes = get_past_minutes_day(now)
    consumptions = session.query(Consumption).filter(
        Consumption.user_id == user.id,
        Consumption.time_creation >= now - datetime.timedelta(minutes=today_minutes)).all()
    return consumptions


def get_consumptions_for_graph_user(session, user, time_period):
    time_period = time_period.replace(" ", "")
    if time_period_has_dash(time_period):
        start, end = time_period.split('-')
        consumptions = session.query(sqlalchemy.func.sum(Consumption.amount_money), Consumption.category_id).filter(
            Consumption.user_id == user.id,
            sqlalchemy.func.date(Consumption.time_creation) >= datetime.datetime.strptime(start, '%d.%m.%Y').date(),
            sqlalchemy.func.date(Consumption.time_creation) <= datetime.datetime.strptime(end, '%d.%m.%Y').date()
        ).group_by(Consumption.category_id).all()
    else:
        consumptions = session.query(sqlalchemy.func.sum(Consumption.amount_money), Consumption.category_id).filter(
            Consumption.user_id == user.id,
            sqlalchemy.func.date(Consumption.time_creation) == datetime.datetime.strptime(time_period, '%d.%m.%Y').date()
        ).group_by(Consumption.category_id).all()
    return consumptions


def divide_into_money_and_categories_consumption(session, consumptions):
    categories = []
    money = []
    for money_, category_id in consumptions:
        category = session.query(CategoryConsumption).get(category_id)
        category = r'{}'.format(category.category)
        categories.append(category)
        money.append(money_)
    return money, categories


def get_earnings_for_graph_user(session, user, time_period):
    time_period = time_period.replace(" ", "")
    if time_period_has_dash(time_period):
        start, end = time_period.split('-')
        earnings = session.query(sqlalchemy.func.sum(Earning.amount_money), Earning.category_id).filter(
            Earning.user_id == user.id,
            sqlalchemy.func.date(Earning.time_creation) >= datetime.datetime.strptime(start, '%d.%m.%Y').date(),
            sqlalchemy.func.date(Earning.time_creation) <= datetime.datetime.strptime(end, '%d.%m.%Y').date()
        ).group_by(Earning.category_id).all()
    else:
        earnings = session.query(sqlalchemy.func.sum(Earning.amount_money), Earning.category_id).filter(
            Earning.user_id == user.id,
            sqlalchemy.func.date(Earning.time_creation) == datetime.datetime.strptime(time_period, '%d.%m.%Y').date()
        ).group_by(Earning.category_id).all()
    return earnings


def divide_into_money_and_categories_earnings(session, earnings):
    categories = []
    money = []
    for money_, category_id in earnings:
        category = session.query(CategoryEarning).get(category_id)
        category = r'{}'.format(category.category)
        categories.append(category)
        money.append(money_)
    return money, categories


def get_transactions_for_graph_by_type(session, user, type_transactions, time_period):
    if type_transactions == TypeTransaction.EARNING:
        earnings = get_earnings_for_graph_user(session, user, time_period)
        return divide_into_money_and_categories_earnings(session, earnings)
    else:
        consumptions = get_consumptions_for_graph_user(session, user, time_period)
        return divide_into_money_and_categories_consumption(session, consumptions)


def total_amount_money(transactions: list):
    total = .0
    for t in transactions:
        total += t.amount_money
    return total


def from_datetime_to_str(datetime_):
    return datetime_.strftime('%d.%m.%Y')


def get_lifetime_user(user: User, now):
    return '{} - {}'.format(from_datetime_to_str(user.date_registration), from_datetime_to_str(now))


def get_today(now):
    return '{}'.format(from_datetime_to_str(now))


def get_yesterday(now):
    return '{}'.format(from_datetime_to_str(now - datetime.timedelta(days=1)))


def get_current_week(now):
    current_week_day = now.weekday()
    return '{} - {}'.format(from_datetime_to_str(now - datetime.timedelta(days=current_week_day)),
                            from_datetime_to_str(now))


def get_current_month(now):
    current_day = now.day
    return '{} - {}'.format(from_datetime_to_str(now - datetime.timedelta(days=current_day-1)), from_datetime_to_str(now))


def check_right_time_period(time_period_str: str):
    time_period_str = time_period_str.replace(" ", "")
    try:
        start, end = time_period_str.split('-')
    except ValueError:
        return check_strptime(time_period_str)
    return True if check_strptime(start) and check_strptime(end) else False


def check_strptime(str_time):
    try:
        datetime.datetime.strptime(str_time, '%d.%m.%Y')
    except ValueError:
        return False
    return True


def time_period_has_dash(time_period):
    time_period = time_period.replace(" ", "")
    try:
        start, end = time_period.split('-')
    except ValueError:
        return False
    return True


def take_percentage_number(number, percentage):
    return (number / 100) * percentage
