import unittest

from sqlalchemy.orm import sessionmaker

from bot.conversations.limits.messages import text_limit
from bot.models import Base, TypeLimit, Limit
from tests.test_models import engine
from tests.utils_models import add_example_limit, add_example_category_consumption, add_example_consumption, \
    example_limit, example_category_consumption

Session = sessionmaker(bind=engine)
session = Session()


class TestTextLimit(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_exist_category(self):
        add_example_limit(session)
        add_example_category_consumption(session)
        add_example_consumption(session)
        limit = session.query(Limit).get(1)
        expected = f"{TypeLimit.text_type(example_limit['type_limit']).title()} " \
                   f"{example_category_consumption['category']} - {example_limit['amount_money']} р."
        actual = text_limit(session, limit)
        self.assertEqual(expected, actual)

    def test_non_exist_category(self):
        limit = Limit(user_id=1,
                      type_limit=0,
                      amount_money=100)
        expected = f"{TypeLimit.text_type(example_limit['type_limit']).title()} " \
                   f"Общий - {example_limit['amount_money']} р."
        actual = text_limit(session, limit)
        self.assertEqual(expected, actual)


