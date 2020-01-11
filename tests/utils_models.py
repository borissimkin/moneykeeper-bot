import datetime

from bot.models import User, CategoryEarning, Earning, CategoryConsumption, Consumption

now = datetime.datetime(2020, 1, 10, 12, 30, 00)
example_user = {'id': 1,
                'telegram_username': 'username',
                'telegram_user_id': 41231323,
                'first_name': 'Boris',
                'last_name': 'last_name',
                'last_activity': now,
                'date_registration': now,
                }

example_category_earning = {'id': 1,
                            'category': 'Работа',
                            'user_id': 1
                            }

example_earning = {'id': 1,
                   'user_id': 1,
                   'category_id': 1,
                   'amount_money': 100.123,
                   }

example_category_consumption = {'id': 1,
                                'category': 'Транспорт',
                                'user_id': 1}

example_consumption = {'id': 1,
                       'user_id': 1,
                       'category_id': 1,
                       'amount_money': 100.123,
                       }


def add_example_user(session):
    session.add(User(telegram_username=example_user['telegram_username'],
                     telegram_user_id=example_user['telegram_user_id'],
                     first_name=example_user['first_name'],
                     last_name=example_user['last_name'],
                     last_activity=example_user['last_activity'],
                     date_registration=example_user['date_registration']))
    session.commit()


def add_example_category_earning(session):
    session.add(CategoryEarning(category=example_category_earning['category'],
                                user_id=example_category_earning['user_id']))

    session.commit()


def add_example_earning(session):
    session.add(Earning(
        user_id=example_earning['user_id'],
        category_id=example_earning['category_id'],
        amount_money=example_earning['amount_money']))
    session.commit()


def add_example_category_consumption(session):
    session.add(CategoryConsumption(category=example_category_consumption['category'],
                                    user_id=example_category_consumption['user_id']))
    session.commit()


def add_example_consumption(session):
    session.add(Consumption(user_id=example_consumption['user_id'],
                            category_id=example_consumption['category_id'],
                            amount_money=example_consumption['amount_money'],
                            ))
    session.commit()
