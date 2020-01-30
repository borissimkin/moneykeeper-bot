import unittest

from sqlalchemy.orm import sessionmaker

from bot.conversations.delete_transaction.earning_deleter import EarningDeleter
from bot.models import Base, Earning
from tests.test_models import engine
from tests.utils_models import example_user, add_example_category_earning, \
    example_category_earning, example_earning, add_example_earning

Session = sessionmaker(bind=engine)
session = Session()


class TestEarningDeleter(unittest.TestCase):
    def setUp(self):
        self.deleter = EarningDeleter(1, example_user['telegram_user_id'],
                                          )
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_get_transaction(self):
        add_example_earning(session)
        answer = self.deleter.get_transaction(session)
        expected = session.query(Earning).get(1)
        self.assertEqual(answer, expected)

    def test_make_text_delete_transaction(self):
        add_example_category_earning(session)
        add_example_earning(session)

        earning = session.query(Earning).get(1)
        expected = f"Вы уверены, что хотите удалить доход в размере <b>{example_earning['amount_money']} " \
            f"рублей</b> категории <b>{example_category_earning['category']}</b>, созданный в " \
            f"<b>{earning.get_str_time_creation()}</b>?"
        self.assertEqual(self.deleter.make_text_delete_transaction(session), expected)

    def test_delete_transaction(self):
        add_example_earning(session)
        self.deleter.delete_transaction(session)
        answer = session.query(Earning).get(1)
        expected = None
        self.assertEqual(answer, expected)

