import unittest

from bot.conversations.add_consumption.messages import text_to_choose_category


class TestTextToChooseCategory(unittest.TestCase):
    def test_one_ruble(self):
        expected = 'Выберите категорию, куда вы потратили <b>1 рубль.</b>'
        self.assertEqual(text_to_choose_category(1), expected)

    def test_hundred_ruble(self):
        expected = 'Выберите категорию, куда вы потратили <b>100 рублей.</b>'
        self.assertEqual(text_to_choose_category(100), expected)


