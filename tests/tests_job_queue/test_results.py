import unittest
import datetime

from sqlalchemy.orm import sessionmaker

from bot.job_queue.results import is_time_to_week_results, make_text_week_results
from bot.models import Base, User
from tests.test_models import engine
from tests.utils_models import add_example_user, add_example_consumption, example_consumption

Session = sessionmaker(bind=engine)
session = Session()


class TestIsTimeToWeekResults(unittest.TestCase):
    def test_is_time_to_week_results(self):
        now = datetime.datetime(2020, 1, 26)
        self.assertEqual(is_time_to_week_results(now), True)

    def test_no_time_to_week_results(self):
        now = datetime.datetime(2020, 1, 25)
        self.assertEqual(is_time_to_week_results(now), False)


class TestMakeTextWeekResults(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_make_text_week_results(self):
        now = datetime.datetime(2020, 1, 12, 12, 30, 00)
        add_example_user(session)
        add_example_consumption(session)
        user = session.query(User).get(1)
        actual = make_text_week_results(session, now, user)
        expected = 'За прошедшую неделю вы потратили <b>{} рублей</b>.'.format(example_consumption['amount_money'])
        self.assertEqual(expected, actual)


