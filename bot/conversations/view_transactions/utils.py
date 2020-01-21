from bot.models import User, Consumption, Earning


def make_list_transactions(session, telegram_user_id):
    user = session.query(User).filter(User.telegram_user_id == telegram_user_id).first()
    earnings = session.query(Earning).filter(Earning.user_id == user.id).all()
    consumptions = session.query(Consumption).filter(Consumption.user_id == user.id).all()
    all_transactions = earnings + consumptions
    sort_list_transactions = sorted(all_transactions, key=lambda x: x.time_creation, reverse=True)
    return sort_list_transactions


def make_list_earnings(session, telegram_user_id):
    user = session.query(User).filter(User.telegram_user_id == telegram_user_id).first()
    earnings = session.query(Earning).filter(Earning.user_id == user.id).order_by(Earning.time_creation.desc()).all()
    return earnings


def make_list_consumptions(session, telegram_user_id):
    user = session.query(User).filter(User.telegram_user_id == telegram_user_id).first()
    consumptions = session.query(Consumption).filter(Consumption.user_id == user.id).\
        order_by(Consumption.time_creation.desc()).all()
    return consumptions
