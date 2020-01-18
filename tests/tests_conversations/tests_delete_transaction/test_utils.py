import unittest

from bot.conversations.delete_transaction.utils import message_has_delete_consumption, get_id_transaction


class TestMessageHasDeleteConsumption(unittest.TestCase):
    def test_yes_has_delete_consumption(self):
        text_command = '/del_c213'
        self.assertEqual(message_has_delete_consumption(text_command), True)

    def test_no_has_delete_consumption(self):
        text_command = '/del_e213'
        self.assertEqual(message_has_delete_consumption(text_command), False)


class TestGetIdTransaction(unittest.TestCase):
    def test_get_id_transaction(self):
        text_command = '/del_c69'
        self.assertEqual(get_id_transaction(text_command), 69)
