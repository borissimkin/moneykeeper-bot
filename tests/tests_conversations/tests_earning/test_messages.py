import unittest

from bot.conversations.earning.messages import text_to_choose_category


class TestTextToChooseCategory(unittest.TestCase):
    def test_one_ruble(self):
        expected = 'Выберите категорию, откуда вы получили <b>1 рубль.</b>'
        self.assertEqual(text_to_choose_category(1), expected)

    def test_hundred_ruble(self):
        expected = 'Выберите категорию, откуда вы получили <b>100 рублей.</b>'
        self.assertEqual(text_to_choose_category(100), expected)
