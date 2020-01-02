import datetime
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bot.models import Base, User

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
        session.add(User(id=cls.user['id'], telegram_username=cls.user['telegram_username'],
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


if __name__ == '__main__':
    unittest.main()
