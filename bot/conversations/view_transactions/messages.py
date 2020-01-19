from bot.models import Earning, CategoryEarning, CategoryConsumption, session


def make_text_earning(session, earning):
    category = session.query(CategoryEarning).get(earning.category_id)
    return f'Доход {earning.amount_money} руб. {category.category} {earning.get_str_time_creation()}\n'


def make_text_consumption(session, consumption):
    category = session.query(CategoryConsumption).get(consumption.category_id)
    return f'Расход {consumption.amount_money} руб. {category.category} {consumption.get_str_time_creation()}\n'


def make_text_list_transactions(session, list_transactions: list):
    if not list_transactions:
        return 'Нет транзакций.'
    text = ''
    for transaction in list_transactions:
        if isinstance(transaction, Earning):
            text += make_text_earning(session=session, earning=transaction)
        else:
            text += make_text_consumption(session=session, consumption=transaction)
    return text
