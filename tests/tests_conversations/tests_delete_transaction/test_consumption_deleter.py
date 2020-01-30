import unittest

from sqlalchemy.orm import sessionmaker

from bot.conversations.delete_transaction.consumption_deleter import ConsumptionDeleter
from bot.models import Base, Consumption
from tests.test_models import engine
from tests.utils_models import example_user, add_example_category_consumption, \
    example_category_consumption, example_consumption, add_example_consumption

Session = sessionmaker(bind=engine)
session = Session()


class TestConsumptionDeleter(unittest.TestCase):
    def setUp(self):
        self.deleter = ConsumptionDeleter(1, example_user['telegram_user_id'],
                                          )
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_get_transaction(self):
        add_example_consumption(session)
        answer = self.deleter.get_transaction(session)
        expected = session.query(Consumption).get(1)
        self.assertEqual(answer, expected)

    def test_make_text_delete_transaction(self):
        add_example_category_consumption(session)
        add_example_consumption(session)

        consumption = session.query(Consumption).get(1)
        expected = f"Вы уверены, что хотите удалить расход в размере <b>{example_consumption['amount_money']} " \
            f"рублей</b> категории <b>{example_category_consumption['category']}</b>, созданный в " \
            f"<b>{consumption.get_str_time_creation()}</b>?"
        self.assertEqual(self.deleter.make_text_delete_transaction(session), expected)

    def test_delete_transaction(self):
        add_example_consumption(session)
        self.deleter.delete_transaction(session)
        answer = session.query(Consumption).get(1)
        expected = None
        self.assertEqual(answer, expected)

