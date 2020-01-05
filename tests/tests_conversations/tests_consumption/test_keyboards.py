import unittest
from unittest import mock

from bot.conversations.consumption.keyboards import make_buttons_for_choose_category, row_is_full
from bot.models import CategoryConsumption


class TestMakeButtonsForChooseCategory(unittest.TestCase):
    def setUp(self):
        self.category = mock.Mock(CategoryConsumption)
        self.category.category = 'Продукты'

    def init_categories(self, count_categories):
        categories = []
        for i in range(count_categories):
            categories.append(self.category)
        return categories

    def test_nine_categories(self):
        categories = self.init_categories(9)
        expected = [[self.category.category, self.category.category, self.category.category],
                    [self.category.category, self.category.category, self.category.category],
                    [self.category.category, self.category.category, self.category.category]]
        answer = make_buttons_for_choose_category(3, categories)
        self.assertListEqual(answer, expected)

    def test_two_categories(self):
        categories = self.init_categories(2)
        expected = [[self.category.category, self.category.category]]
        answer = make_buttons_for_choose_category(3, categories)
        self.assertListEqual(answer, expected)


class TestRowIsFull(unittest.TestCase):
    def test_row_full(self):
        self.assertTrue(row_is_full(2, 3))

    def test_row_not_full(self):
        self.assertFalse(row_is_full(1, 3))

    def test_row_equal_zero(self):
        self.assertFalse(row_is_full(0, 3))
