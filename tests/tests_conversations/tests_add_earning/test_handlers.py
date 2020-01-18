import unittest
from unittest import mock

from sqlalchemy.orm import sessionmaker

from bot.conversations.add_earning.handlers import add_earning_in_db
from bot.models import User, CategoryEarning, Earning, CategoryConsumption, Consumption, Base
from tests.test_models import engine
from tests.utils_models import add_example_user, \
    example_user, add_example_category_earning, example_category_earning

Session = sessionmaker(bind=engine)
session = Session()


class TestAddEarningInDb(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_add_earning_in_db(self):
        amount_money = 120.120
        add_example_user(session)
        add_example_category_earning(session)

        expected = Earning(id=1,
                           category_id=example_category_earning['id'],
                           amount_money=amount_money)
        add_earning_in_db(session=session,
                          telegram_user_id=example_user['telegram_user_id'],
                          amount_money=amount_money,
                          category_text=example_category_earning['category'])
        answer = session.query(Earning).get(1)
        self.assertEqual(answer, expected)