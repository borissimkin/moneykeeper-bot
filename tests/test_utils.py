import datetime
import unittest

from bot.buttons import Buttons
from bot.utils import add_button_cancel, add_buttons_exit_and_back, add_button_exit, ruble_declension, \
    get_past_minutes_day, to_text_weekday, text_goodbye


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


class TestGetPastMinutesDay(unittest.TestCase):
    def test_past_zero_minutes(self):
        now = datetime.datetime(2020, 1, 1)
        self.assertEqual(get_past_minutes_day(now), 0)

    def test_ten_minutes(self):
        now = datetime.datetime(2020, 1, 1, 0, 10)
        self.assertEqual(get_past_minutes_day(now), 10)


class TestToTextWeekday(unittest.TestCase):
    def test_morning(self):
        now = datetime.datetime(2020, 1, 20)
        self.assertEqual(to_text_weekday(now.weekday()), 'Понедельник')

    def test_wednesday(self):
        now = datetime.datetime(2020, 1, 22)
        self.assertEqual(to_text_weekday(now.weekday()), 'Среда')


class TestTextGoodbye(unittest.TestCase):
    def test_good_day(self):
        now = datetime.datetime(2020, 1, 20, 10)
        self.assertEqual(text_goodbye(now), 'Хорошего дня!')

    def test_good_night(self):
        now = datetime.datetime(2020, 1, 20, 20)
        self.assertEqual(text_goodbye(now), 'Доброй ночи!')
