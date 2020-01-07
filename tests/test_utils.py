import unittest

from bot.buttons import text_button_cancel, text_button_back, text_button_exit
from bot.utils import add_button_cancel, add_buttons_exit_and_back, add_button_exit


class TestAddButtonCancel(unittest.TestCase):
    def test_empty_list(self):
        expected = [[text_button_cancel]]
        self.assertListEqual(add_button_cancel([]), expected)

    def test_not_empty_list(self):
        buttons = [['Транспорт', 'Еда']]
        expected = [['Транспорт', 'Еда'], [text_button_cancel]]
        self.assertListEqual(add_button_cancel(buttons), expected)


class TestAddButtonsExitAndBack(unittest.TestCase):
    def test_empty_list(self):
        expected = [[text_button_back, text_button_exit]]
        self.assertListEqual(add_buttons_exit_and_back([]), expected)

    def test_not_empty_list(self):
        buttons = [['Транспорт', 'Еда']]
        expected = [['Транспорт', 'Еда'], [text_button_back, text_button_exit]]
        self.assertListEqual(add_buttons_exit_and_back(buttons), expected)


class TestAddButtonsExit(unittest.TestCase):
    def test_empty_list(self):
        expected = [[text_button_exit]]
        self.assertListEqual(add_button_exit([]), expected)

    def test_not_empty_list(self):
        buttons = [['Доход', 'Расход']]
        expected = [['Доход', 'Расход'], [text_button_exit]]
        self.assertListEqual(add_button_exit(buttons), expected)
