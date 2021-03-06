import datetime
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bot.models import User, CategoryEarning, Earning, CategoryConsumption, Consumption, Base
from tests.utils_models import add_example_user, example_user, add_example_category_earning, example_category_earning, \
    add_example_earning, example_earning, add_example_category_consumption, example_category_consumption, \
    add_example_consumption, \
    example_consumption

engine = create_engine('sqlite:///:memory:')

Session = sessionmaker(bind=engine)
session = Session()


class TestUser(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_query_user(self):
        add_example_user(session)
        expected = [User(id=1, telegram_username='username', telegram_user_id=123,
                         first_name='boris', last_name='last name')]
        result = session.query(User).all()
        self.assertEqual(result, expected)

    def test_update_activity(self):
        add_example_user(session)
        now = datetime.datetime(2021, 1, 10, 12, 55, 12)
        user = session.query(User).get(1)
        user.update_activity(session, now)
        self.assertEqual(user.last_activity, now)

    def test_repr(self):
        add_example_user(session)
        user = session.query(User).get(1)
        expected = f"<User ('{example_user['id']}', '{example_user['telegram_username']}', " \
            f"'{example_user['telegram_user_id']}', '{example_user['first_name']}', " \
            f"'{example_user['last_name']}', '{example_user['last_activity']}', '{example_user['date_registration']}')>"
        self.assertEqual(repr(user), expected)


class TestCategoryEarning(unittest.TestCase):

    def setUp(self):
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_query_category_earning(self):
        add_example_category_earning(session)
        expected = [CategoryEarning(id=1, category='Работа')]
        category_earning = session.query(CategoryEarning).all()
        self.assertEqual(category_earning, expected)

    def test_repr(self):
        add_example_category_earning(session)
        expected = f"<CategoryEarning('{example_category_earning['id']}', " \
            f"'{example_category_earning['category']}', '{example_category_earning['user_id']}')>"
        category_earning = session.query(CategoryEarning).get(1)
        self.assertEqual(repr(category_earning), expected)

    def test_delete_category(self):
        add_example_category_earning(session)
        category = session.query(CategoryEarning).get(1)
        category.delete_category(session)
        answer = session.query(CategoryEarning).get(1)
        self.assertEqual(answer, None)

    def test_update_category(self):
        new_category = 'Подработка'
        add_example_category_earning(session)
        category = session.query(CategoryEarning).get(1)
        category.update_category(session, new_category)
        category = session.query(CategoryEarning).get(1)
        self.assertEqual(category.category, new_category)


class TestEarning(unittest.TestCase):

    def setUp(self):
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_query_earning(self):
        add_example_earning(session)
        expected = [Earning(id=1, user_id=1, category_id=1, amount_money=0)]
        earnings = session.query(Earning).all()
        self.assertEqual(earnings, expected)

    def test_repr(self):
        add_example_earning(session)
        expected = f"<Earning('{example_earning['id']}', '{example_earning['user_id']}', " \
            f"'{example_earning['category_id']}', '{example_earning['amount_money']}', " \
            f"'{example_earning['time_creation']}')>"
        earning = session.query(Earning).get(1)
        self.assertEqual(repr(earning), expected)

    def test_delete_list_earning(self):
        for _ in range(2):
            add_example_earning(session)
        earnings = session.query(Earning).all()
        Earning.delete_list_earning(session, earnings)
        answer = session.query(Earning).all()
        self.assertEqual(answer, [])

    def test_get_time_creation(self):
        add_example_earning(session)
        earning = session.query(Earning).get(1)
        answer = earning.get_str_time_creation()
        expected = '10.01.2020, 12:30'
        self.assertEqual(answer, expected)


class TestCategoryConsumption(unittest.TestCase):

    def setUp(self):
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_query_category_consumption(self):
        add_example_category_consumption(session)
        expected = [CategoryConsumption(id=1, category='Транспорт')]
        category_consumption = session.query(CategoryConsumption).all()
        self.assertEqual(category_consumption, expected)

    def test_repr(self):
        add_example_category_consumption(session)
        expected = f"<CategoryConsumption('{example_category_consumption['id']}', " \
            f"'{example_category_consumption['category']}', '{example_category_consumption['user_id']}')>"
        category_consumption = session.query(CategoryConsumption).get(example_category_consumption['id'])
        self.assertEqual(repr(category_consumption), expected)

    def test_delete_category(self):
        add_example_category_consumption(session)
        category = session.query(CategoryConsumption).get(1)
        category.delete_category(session)
        answer = session.query(CategoryConsumption).get(1)
        self.assertEqual(answer, None)

    def test_update_category(self):
        new_category = 'Шаурма'
        add_example_category_consumption(session)
        category = session.query(CategoryConsumption).get(1)
        category.update_category(session, new_category)
        category = session.query(CategoryConsumption).get(1)
        self.assertEqual(category.category, new_category)


class TestConsumption(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_query_consumption(self):
        add_example_consumption(session)
        expected = [Consumption(id=1, user_id=1, category_id=1, amount_money=1)]
        consumptions = session.query(Consumption).all()
        self.assertEqual(consumptions, expected)

    def test_repr(self):
        add_example_consumption(session)
        expected = f"<Consumption('{example_consumption['id']}', " \
            f"'{example_consumption['user_id']}', '{example_consumption['category_id']}', " \
            f"'{example_consumption['amount_money']}', '{example_consumption['time_creation']}')>"
        consumption = session.query(Consumption).get(1)
        self.assertEqual(repr(consumption), expected)

    def test_delete_list_consumption(self):
        for _ in range(2):
            add_example_consumption(session)
        consumptions = session.query(Consumption).all()
        Consumption.delete_list_consumption(session, consumptions)
        answer = session.query(Consumption).all()
        self.assertEqual(answer, [])

    def test_get_time_creation(self):
        add_example_consumption(session)
        consumption = session.query(Consumption).get(1)
        answer = consumption.get_str_time_creation()
        expected = '10.01.2020, 12:30'
        self.assertEqual(answer, expected)
