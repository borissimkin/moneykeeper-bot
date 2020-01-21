import datetime
import unittest

from sqlalchemy.orm import sessionmaker

from bot.conversations.view_transactions.utils import make_list_transactions
from bot.models import Base, Earning, Consumption
from tests.test_models import engine
from tests.utils_models import example_user, add_example_user, add_example_category_consumption, \
    example_category_consumption, add_example_earning, add_example_consumption

Session = sessionmaker(bind=engine)
session = Session()


class TestMakeListTransactions(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_make_list_transactions(self):
        add_example_user(session)
        session.add(Consumption(id=1,
                                user_id=1,
                                time_creation=datetime.datetime(2020, 1, 10, 12, 30, 00)))
        session.add(Consumption(id=2,
                                user_id=1,
                                time_creation=datetime.datetime(2020, 1, 8, 12, 25, 00)))
        session.add(Earning(id=1,
                            user_id=1,
                            time_creation=datetime.datetime(2020, 1, 9, 12, 25, 00)))
        session.add(Consumption(id=3,
                                user_id=1,
                                time_creation=datetime.datetime(2020, 1, 12, 12, 25, 00)))
        session.commit()
        answer = make_list_transactions(session, example_user['telegram_user_id'])
        expected = [Consumption(id=3), Consumption(id=1), Earning(id=1), Consumption(id=2)]
        self.assertEqual(answer, expected)