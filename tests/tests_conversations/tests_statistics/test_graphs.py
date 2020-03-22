import unittest

from bot.conversations.statistics.utils import get_consumptions_for_graph_user_all_time
from bot.models import User, Base
from tests.test_models import session, engine
from tests.utils_models import add_example_user


class TestGeneralGraph(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_graph(self):
        add_example_user(session)
        user = session.query(User).get(1)
        get_consumptions_for_graph_user_all_time(session, user)
        print('tuta')