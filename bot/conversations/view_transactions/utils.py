from bot.models import User, Consumption, Earning


def make_list_transactions(session, telegram_user_id):
    user = session.query(User).filter(User.telegram_user_id == telegram_user_id).first()
    earnings = session.query(Earning).filter(Earning.user_id == user.id).all()
    consumptions = session.query(Consumption).filter(Consumption.user_id == user.id).all()
    all_transactions = earnings + consumptions
    sort_list_transactions = sorted(all_transactions, key=lambda x: x.time_creation, reverse=True)
    return sort_list_transactions
