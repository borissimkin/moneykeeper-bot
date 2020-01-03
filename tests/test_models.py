import datetime
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bot.models import User, CategoryEarning, Earning, CategoryConsumption, Consumption, Base

engine = create_engine('sqlite:///:memory:')

Session = sessionmaker(bind=engine)
session = Session()


class TestUser(unittest.TestCase):
    now = datetime.datetime(2020, 1, 10, 12, 30, 00)
    user = {'id': 1,
            'telegram_username': 'username',
            'telegram_user_id': 41231323,
            'first_name': 'Boris',
            'last_name': 'last_name',
            'last_activity': now,
            'date_registration': now,
            }

    @classmethod
    def add_user(cls):
        session.add(User(telegram_username=cls.user['telegram_username'],
                         telegram_user_id=cls.user['telegram_user_id'],
                         first_name=cls.user['first_name'],
                         last_name=cls.user['last_name'],
                         last_activity=cls.user['last_activity'],
                         date_registration=cls.user['date_registration']))
        session.commit()

    def setUp(self):
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_query_user(self):
        self.add_user()
        expected = [User(id=1, telegram_username='username', telegram_user_id=123,
                         first_name='boris', last_name='last name')]
        result = session.query(User).all()
        self.assertEqual(result, expected)

    def test_update_activity(self):
        self.add_user()
        now = datetime.datetime(2021, 1, 10, 12, 55, 12)
        user = session.query(User).get(1)
        user.update_activity(now)
        self.assertEqual(user.last_activity, now)

    def test_repr(self):
        self.add_user()
        user = session.query(User).get(1)
        expected = f"<User ('{self.user['id']}', '{self.user['telegram_username']}', " \
            f"'{self.user['telegram_user_id']}', '{self.user['first_name']}', " \
            f"'{self.user['last_name']}', '{self.user['last_activity']}', '{self.user['date_registration']}')>"
        self.assertEqual(repr(user), expected)


class TestCategoryEarning(unittest.TestCase):
    category_earning = {'id': 1,
                        'category': 'Работа',
                        }

    def add_category_earning(self):
        session.add(CategoryEarning(
                                    category=self.category_earning['category']))
        session.commit()

    def setUp(self):
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_query_category_earning(self):
        self.add_category_earning()
        expected = [CategoryEarning(id=1, category='Работа')]
        category_earning = session.query(CategoryEarning).all()
        self.assertEqual(category_earning, expected)

    def test_repr(self):
        self.add_category_earning()
        expected = f"<CategoryEarning('{self.category_earning['id']}', " \
            f"'{self.category_earning['category']}')>"
        category_earning = session.query(CategoryEarning).get(1)
        self.assertEqual(repr(category_earning), expected)


class TestEarning(unittest.TestCase):
    earning = {'id': 1,
               'user_id': 1,
               'category_id': 1,
               'amount_money': 100.123,
               }

    def add_earning(self):
        session.add(Earning(
                            user_id=self.earning['user_id'],
                            category_id=self.earning['category_id'],
                            amount_money=self.earning['amount_money']))
        session.commit()

    def setUp(self):
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_query_earning(self):
        self.add_earning()
        expected = [Earning(id=1, user_id=1, category_id=1, amount_money=0)]
        earnings = session.query(Earning).all()
        self.assertEqual(earnings, expected)

    def test_repr(self):
        self.add_earning()
        expected = f"<Earning('{self.earning['id']}', '{self.earning['user_id']}', " \
            f"'{self.earning['category_id']}', '{self.earning['amount_money']}')>"
        earning = session.query(Earning).get(1)
        self.assertEqual(repr(earning), expected)


class TestCategoryConsumption(unittest.TestCase):
    category_consumption = {'id': 1,
                            'category': 'Транспорт'}

    def add_category_consumption(self):
        session.add(CategoryConsumption(
                                        category=self.category_consumption['category']))
        session.commit()

    def setUp(self):
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_query_category_consumption(self):
        self.add_category_consumption()
        expected = [CategoryConsumption(id=1, category='Транспорт')]
        category_consumption = session.query(CategoryConsumption).all()
        self.assertEqual(category_consumption, expected)

    def test_repr(self):
        self.add_category_consumption()
        expected = f"<CategoryConsumption('{self.category_consumption['id']}', " \
            f"'{self.category_consumption['category']}')>"
        category_consumption = session.query(CategoryConsumption).get(self.category_consumption['id'])
        self.assertEqual(repr(category_consumption), expected)


class TestConsumption(unittest.TestCase):
    consumption = {'id': 1,
                   'user_id': 1,
                   'category_id': 1,
                   'amount_money': 100.123,
                   }

    def add_consumption(self):
        session.add(Consumption(
                                user_id=self.consumption['user_id'],
                                category_id=self.consumption['category_id'],
                                amount_money=self.consumption['amount_money']))
        session.commit()

    def setUp(self):
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_query_consumption(self):
        self.add_consumption()
        expected = [Consumption(id=1, user_id=1, category_id=1, amount_money=1)]
        consumptions = session.query(Consumption).all()
        self.assertEqual(consumptions, expected)

    def test_repr(self):
        self.add_consumption()
        expected = f"<Consumption('{self.consumption['id']}', " \
            f"'{self.consumption['user_id']}', '{self.consumption['category_id']}', " \
            f"'{self.consumption['amount_money']}')>"
        consumption = session.query(Consumption).get(1)
        self.assertEqual(repr(consumption), expected)


if __name__ == '__main__':
    unittest.main()
