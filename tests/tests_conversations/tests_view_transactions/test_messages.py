import datetime

from sqlalchemy.orm import sessionmaker
import unittest

from bot.conversations.view_transactions.messages import make_text_list_transactions
from bot.conversations.view_transactions.utils import make_list_transactions
from bot.models import Base, Earning, Consumption
from tests.test_models import engine
from tests.utils_models import example_user, add_example_user, add_example_category_consumption, \
    example_category_consumption, add_example_earning, add_example_consumption, add_example_category_earning, \
    example_category_earning

Session = sessionmaker(bind=engine)
session = Session()


class TestMakeTextListTransactions(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_exist_transactions(self):
        add_example_user(session)
        add_example_category_earning(session)
        add_example_category_consumption(session)

        session.add(Earning(id=1,
                            time_creation=datetime.datetime(2020, 1, 10, 12, 30, 00),
                            category_id=1,
                            user_id=1))
        session.add(Consumption(id=1,
                                time_creation=datetime.datetime(2020, 1, 9, 12, 30, 00),
                                category_id=1,
                                user_id=1))
        session.commit()
        list_transactions = make_list_transactions(session, example_user['telegram_user_id'])
        expected = f"Доход 0.0 руб. {example_category_earning['category']} 10.01.2020, 12:30\n" \
            f"Расход 0.0 руб. {example_category_consumption['category']} 09.01.2020, 12:30\n"
        actual = make_text_list_transactions(session, list_transactions)
        self.assertEqual(actual, expected)
