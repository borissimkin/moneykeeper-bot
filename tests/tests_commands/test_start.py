import unittest
from unittest import mock

from sqlalchemy.orm import sessionmaker
import telegram

from bot.commands.start import StartHandler
from bot.models import Base, User
from tests.test_models import engine
from tests.utils_models import example_user, add_example_user

Session = sessionmaker(bind=engine)
session = Session()



class TestStart(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    @staticmethod
    def init_mock_update():
        update = mock.Mock(telegram.Update)
        message = mock.Mock(telegram.Message)
        telegram_user = mock.Mock(telegram.User)
        telegram_user.id = example_user['telegram_user_id']
        telegram_user.first_name = example_user['first_name']
        telegram_user.last_name = example_user['last_name']
        message.from_user = telegram_user
        update.message = message
        return update

    def test_add_user_in_db(self):
        update = self.init_mock_update()
        StartHandler.add_user_in_db(update, session)
        answer = session.query(User).get(1)
        expected = User(id=1,
                        )
        self.assertEqual(answer, expected)

    def test_check_user_in_db_user_exist(self):
        add_example_user(session)
        self.assertTrue(StartHandler.check_user_in_db(example_user['telegram_user_id'], session))

    def test_check_user_in_db_user_not_exits(self):
        self.assertFalse(StartHandler.check_user_in_db(example_user['telegram_user_id'], session))