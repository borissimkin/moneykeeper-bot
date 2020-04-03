import datetime
import unittest

from sqlalchemy.orm import sessionmaker

from bot.conversations.statistics.utils import get_consumptions_for_graph_user, get_earnings_for_graph_user
from bot.models import Base, Consumption, User, Earning
from tests.test_models import engine
from tests.utils_models import add_example_user, example_category_consumption, add_example_category_consumption, \
    add_example_category_earning

Session = sessionmaker(bind=engine)
session = Session()


class GetConsumptionsForGraphUser(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)
        add_example_user(session)
        add_example_category_consumption(session)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_time_period_has_not_dash(self):
        time_period = '10.02.2020'
        session.add(Consumption(user_id=1,
                                category_id=1,
                                amount_money=100,
                                time_creation=datetime.datetime(2020, 2, 10, 14, 30, 10)))
        session.add(Consumption(user_id=1,
                                category_id=1,
                                amount_money=200,
                                time_creation=datetime.datetime(2020, 2, 11, 14, 30, 10)))
        session.add(Consumption(user_id=1,
                                category_id=1,
                                amount_money=200,
                                time_creation=datetime.datetime(2020, 2, 9, 14, 30, 10)))
        session.add(Consumption(user_id=2,
                                category_id=1,
                                amount_money=200,
                                time_creation=datetime.datetime(2020, 2, 10, 14, 30, 10)))
        session.commit()
        user = session.query(User).get(1)
        expected = [(100.0, 1)]
        actual = get_consumptions_for_graph_user(session, user, time_period)
        self.assertListEqual(expected, actual)

    def test_time_period_has_dash(self):
        time_period = '10.02.2020 - 12.02.2020'
        session.add(Consumption(user_id=1,
                                category_id=1,
                                amount_money=100,
                                time_creation=datetime.datetime(2020, 2, 10, 14, 30, 10)))
        session.add(Consumption(user_id=1,
                                category_id=1,
                                amount_money=200,
                                time_creation=datetime.datetime(2020, 2, 12, 14, 30, 10)))
        session.add(Consumption(user_id=1,
                                category_id=1,
                                amount_money=200,
                                time_creation=datetime.datetime(2020, 2, 9, 14, 30, 10)))
        session.add(Consumption(user_id=2,
                                category_id=1,
                                amount_money=200,
                                time_creation=datetime.datetime(2020, 2, 10, 14, 30, 10)))
        session.commit()
        user = session.query(User).get(1)
        expected = [(300.0, 1)]
        actual = get_consumptions_for_graph_user(session, user, time_period)
        self.assertListEqual(expected, actual)


class GetEarningForGraphUser(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)
        add_example_user(session)
        add_example_category_earning(session)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_time_period_has_not_dash(self):
        time_period = '10.02.2020'
        session.add(Earning(user_id=1,
                            category_id=1,
                            amount_money=100,
                            time_creation=datetime.datetime(2020, 2, 10, 14, 30, 10)))
        session.add(Earning(user_id=1,
                            category_id=1,
                            amount_money=200,
                            time_creation=datetime.datetime(2020, 2, 11, 14, 30, 10)))
        session.add(Earning(user_id=1,
                            category_id=1,
                            amount_money=200,
                            time_creation=datetime.datetime(2020, 2, 9, 14, 30, 10)))
        session.add(Earning(user_id=2,
                            category_id=1,
                            amount_money=200,
                            time_creation=datetime.datetime(2020, 2, 10, 14, 30, 10)))
        session.commit()
        user = session.query(User).get(1)
        expected = [(100.0, 1)]
        actual = get_earnings_for_graph_user(session, user, time_period)
        self.assertListEqual(expected, actual)

    def test_time_period_has_dash(self):
        time_period = '10.02.2020 - 12.02.2020'
        session.add(Earning(user_id=1,
                            category_id=1,
                            amount_money=100,
                            time_creation=datetime.datetime(2020, 2, 10, 14, 30, 10)))
        session.add(Earning(user_id=1,
                            category_id=1,
                            amount_money=200,
                            time_creation=datetime.datetime(2020, 2, 12, 14, 30, 10)))
        session.add(Earning(user_id=1,
                            category_id=1,
                            amount_money=200,
                            time_creation=datetime.datetime(2020, 2, 9, 14, 30, 10)))
        session.add(Earning(user_id=2,
                            category_id=1,
                            amount_money=200,
                            time_creation=datetime.datetime(2020, 2, 10, 14, 30, 10)))
        session.commit()
        user = session.query(User).get(1)
        expected = [(300.0, 1)]
        actual = get_earnings_for_graph_user(session, user, time_period)
        self.assertListEqual(expected, actual)
