import datetime

from bot.models import User, Earning, Consumption
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


def total_amount_money(transactions: list):
    total = .0
    for t in transactions:
        total += t.amount_money
    return total
