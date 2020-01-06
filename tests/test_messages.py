import unittest

from bot.messages import text_confirm_add_transaction


class TestTextConfirmAddTransaction(unittest.TestCase):
    def setUp(self):
        self.category = 'Транспорт'

    def test_one_ruble(self):
        expected = 'Записать <b>1 рубль</b> на категорию <b>Транспорт</b>?'
        self.assertEqual(text_confirm_add_transaction(1, 'Транспорт'), expected)

    def test_hundred_ruble(self):
        expected = 'Записать <b>100 рублей</b> на категорию <b>Транспорт</b>?'
        self.assertEqual(text_confirm_add_transaction(100, 'Транспорт'), expected)
