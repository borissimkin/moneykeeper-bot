import unittest

from sqlalchemy.orm import sessionmaker

from bot.conversations.edit_categories.earning_category_manager import EarningCategoryManager
from bot.models import Base, CategoryEarning
from tests.test_models import engine
from tests.utils_models import add_example_user, add_example_category_earning, example_user, \
    example_category_earning

Session = sessionmaker(bind=engine)
session = Session()


class TestCheckAnyCategories(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_has_any_categories(self):
        add_example_user(session)
        add_example_category_earning(session)
        self.assertTrue(EarningCategoryManager.check_any_categories(session,
                                                                    example_user['telegram_user_id']))

    def test_not_has_any_categories(self):
        add_example_user(session)
        self.assertFalse(EarningCategoryManager.check_any_categories(session,
                                                                     example_user['telegram_user_id']))


class TestMakeTextListCategories(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_make_text_list_categories(self):
        add_example_user(session)
        add_example_category_earning(session)
        expected = f"1. {example_category_earning['category']}\n"
        self.assertEqual(EarningCategoryManager.make_text_list_categories(session,
                                                                          example_user['telegram_user_id']),
                         expected)


class TestMessages(unittest.TestCase):
    def test_text_confirm_add_category(self):
        new_category = 'Стипендия'
        expected = f'Вы уверены, что хотите добавить <b>{new_category}</b> в категории <b>доходов</b>?'
        self.assertEqual(EarningCategoryManager.text_confirm_add_category(new_category), expected)

    def test_text_success_add_category(self):
        new_category = 'Стипендия'
        expected = f'Новая категория доходов - <b>{new_category}</b> успешно добавлена!'
        self.assertEqual(EarningCategoryManager.text_success_add_category(new_category), expected)


class TestAddCategoryInDb(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_add_category_in_db(self):
        add_example_user(session)
        new_category = 'Стипендия'
        expected = CategoryEarning(id=1,
                                   category=new_category,
                                   user_id=1)
        EarningCategoryManager.add_category_in_db(session, new_category, example_user['telegram_user_id'])
        answer = session.query(CategoryEarning).get(1)
        self.assertEqual(answer, expected)
