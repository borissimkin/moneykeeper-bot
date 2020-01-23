import datetime
import unittest

from sqlalchemy.orm import sessionmaker

from bot.commands.today import make_text_today
from bot.models import Base, CategoryConsumption, User
from tests.test_models import engine
from tests.utils_models import example_user, add_example_user, add_example_category_consumption, \
    example_category_consumption, add_example_category_earning, add_example_consumption, add_example_earning, \
    example_consumption, example_category_earning, example_earning

Session = sessionmaker(bind=engine)
session = Session()


class TestMakeTextToday(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_exist_transactions(self):
        now = datetime.datetime(2020, 1, 22, 10, 10)
        add_example_user(session)
        add_example_category_consumption(session)
        add_example_category_earning(session)
        add_example_consumption(session, now)
        add_example_earning(session, now)
        expected =  f"Информация на 22.01.2020 10:10, Среда\n\n" \
                    f"<b>Расходы:</b>\n" \
            f"{example_category_consumption['category']} - {example_consumption['amount_money']} р.\n\n" \
                    f"<b>Доходы:</b>\n" \
            f"{example_category_earning['category']} - {example_earning['amount_money']} р.\n\n" \
                    f"<b>Всего:</b>\n" \
            f"Доход: {example_earning['amount_money']}\n" \
            f"Расход: {example_consumption['amount_money']}\n\n" \
                    f"Хорошего дня!"
        user = session.query(User).get(1)
        actual = make_text_today(session, now, user)
        self.assertEqual(actual, expected)


