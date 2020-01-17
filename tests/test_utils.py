import unittest

from bot.buttons import Buttons
from bot.utils import add_button_cancel, add_buttons_exit_and_back, add_button_exit, ruble_declension


class TestAddButtonCancel(unittest.TestCase):
    def test_empty_list(self):
        expected = [[Buttons.cancel]]
        self.assertListEqual(add_button_cancel([]), expected)

    def test_not_empty_list(self):
        buttons = [['Транспорт', 'Еда']]
        expected = [['Транспорт', 'Еда'], [Buttons.cancel]]
        self.assertListEqual(add_button_cancel(buttons), expected)


class TestAddButtonsExitAndBack(unittest.TestCase):
    def test_empty_list(self):
        expected = [[Buttons.back, Buttons.exit]]
        self.assertListEqual(add_buttons_exit_and_back([]), expected)

    def test_not_empty_list(self):
        buttons = [['Транспорт', 'Еда']]
        expected = [['Транспорт', 'Еда'], [Buttons.back, Buttons.exit]]
        self.assertListEqual(add_buttons_exit_and_back(buttons), expected)


class TestAddButtonsExit(unittest.TestCase):
    def test_empty_list(self):
        expected = [[Buttons.exit]]
        self.assertListEqual(add_button_exit([]), expected)

    def test_not_empty_list(self):
        buttons = [['Доход', 'Расход']]
        expected = [['Доход', 'Расход'], [Buttons.exit]]
        self.assertListEqual(add_button_exit(buttons), expected)


class TestRubleDeclension(unittest.TestCase):
    def test_one_ruble(self):
        expected = 'рубль'
        self.assertEqual(ruble_declension(1), expected)

    def test_two_ruble(self):
        expected = 'рубля'
        self.assertEqual(ruble_declension(2), expected)

