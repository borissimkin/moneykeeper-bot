import unittest

from bot.conversations.consumption.messages import text_to_choose_category, text_confirm_add_consumption


class TestTextToChooseCategory(unittest.TestCase):
    def test_one_ruble(self):
        expected = 'Выберите категорию, куда вы потратили <b>1 рубль.</b>'
        self.assertEqual(text_to_choose_category(1), expected)

    def test_hundred_ruble(self):
        expected = 'Выберите категорию, куда вы потратили <b>100 рублей.</b>'
        self.assertEqual(text_to_choose_category(100), expected)


class TestTextConfirmAddConsumption(unittest.TestCase):
    def setUp(self):
        self.category = 'Транспорт'

    def test_one_ruble(self):
        expected = 'Записать <b>1 рубль</b> на категорию <b>Транспорт</b>?'
        self.assertEqual(text_confirm_add_consumption(1, 'Транспорт'), expected)

    def test_hundred_ruble(self):
        expected = 'Записать <b>100 рублей</b> на категорию <b>Транспорт</b>?'
        self.assertEqual(text_confirm_add_consumption(100, 'Транспорт'), expected)
