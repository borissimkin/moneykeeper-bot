# -*- coding: utf-8 -*-
import datetime

import sqlalchemy

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


def get_consumptions_for_graph_user_all_time(session, user):
    consumptions = session.query(sqlalchemy.func.sum(Consumption.amount_money), Consumption.category_id).filter(
        Consumption.user_id == user.id
    ).group_by(Consumption.category_id).all()
    categories = []
    money = []
    for money_, category_id in consumptions:
        category = session.query(CategoryConsumption).get(category_id)
        category = r'{}'.format(category.category)
        categories.append(category)
        money.append(money_)
    return money, categories


def get_earnings_for_graph_user_all_time(session, user):
    consumptions = session.query(sqlalchemy.func.sum(Earning.amount_money), Earning.category_id).filter(
        Earning.user_id == user.id
    ).group_by(Earning.category_id).all()
    categories = []
    money = []
    for money_, category_id in consumptions:
        category = session.query(CategoryEarning).get(category_id)
        category = r'{}'.format(category.category)
        categories.append(category)
        money.append(money_)
    return money, categories


def total_amount_money(transactions: list):
    total = .0
    for t in transactions:
        total += t.amount_money
    return total


def from_datetime_to_str(datetime_):
    return datetime_.strftime('%d.%m.%Y')


def get_lifetime_user(user: User, now):
    return '{} - {}'.format(from_datetime_to_str(user.date_registration), from_datetime_to_str(now))
