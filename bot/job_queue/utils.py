from bot import session
from bot.conversations.statistics.utils import get_earnings_today, get_consumptions_today, get_current_week, \
    get_consumptions_for_graph_user, get_earnings_for_graph_user


def user_has_earning_or_consumption_today(user, now):
    earnings = get_earnings_today(session, now, user)
    consumptions = get_consumptions_today(session, now, user)
    if earnings or consumptions:
        return True
    return False


def user_has_earning_or_consumption_current_week(user, now):
    time_period = get_current_week(now)
    consumptions = get_consumptions_for_graph_user(session, user, time_period)
    earnings = get_earnings_for_graph_user(session, user, time_period)
    if consumptions or earnings:
        return True
    return False
