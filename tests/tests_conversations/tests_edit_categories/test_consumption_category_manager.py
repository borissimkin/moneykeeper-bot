import unittest

from sqlalchemy.orm import sessionmaker

from bot.conversations.edit_categories.consumption_category_manager import ConsumptionCategoryManager
from bot.models import Base, CategoryConsumption
from tests.test_models import engine
from tests.utils_models import example_user, add_example_user, add_example_category_consumption, \
    example_category_consumption


Session = sessionmaker(bind=engine)
session = Session()


class TestCheckAnyCategories(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_has_any_categories(self):
        add_example_user(session)
        add_example_category_consumption(session)
        self.assertTrue(ConsumptionCategoryManager.check_any_categories(session,
                                                                        example_user['telegram_user_id']))

    def test_not_has_any_categories(self):
        add_example_user(session)
        self.assertFalse(ConsumptionCategoryManager.check_any_categories(session,
                                                                         example_user['telegram_user_id']))


class TestMakeTextListCategories(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_make_text_list_categories(self):
        add_example_user(session)
        add_example_category_consumption(session)
        expected = f"1. {example_category_consumption['category']}\n"
        self.assertEqual(ConsumptionCategoryManager.make_text_list_categories(session,
                                                                              example_user['telegram_user_id']),
                         expected)


class TestMessages(unittest.TestCase):
    def test_text_confirm_add_category(self):
        new_category = 'Транспорт'
        expected = f'Вы уверены, что хотите добавить <b>{new_category}</b> в категории <b>расходов</b>?'
        self.assertEqual(ConsumptionCategoryManager.text_confirm_add_category(new_category), expected)

    def test_text_success_add_category(self):
        new_category = 'Транспорт'
        expected = f'Новая категория расходов - <b>{new_category}</b> успешно добавлена!'
        self.assertEqual(ConsumptionCategoryManager.text_success_add_category(new_category), expected)


class TestAddCategoryInDb(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_add_category_in_db(self):
        add_example_user(session)
        new_category = 'Бензин'
        expected = CategoryConsumption(id=1,
                                       category=new_category,
                                       user_id=1)
        ConsumptionCategoryManager.add_category_in_db(session, new_category, example_user['telegram_user_id'])
        answer = session.query(CategoryConsumption).get(1)
        self.assertEqual(answer, expected)


class TestGetAllCategories(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_get_all_categories(self):
        add_example_user(session)
        add_example_category_consumption(session)
        expected = [CategoryConsumption(id=1,
                                        user_id=example_user['id'],
                                        category=example_category_consumption['category'])]
        answer = session.query(CategoryConsumption).all()
        self.assertEqual(answer, expected)


class TestGetAllCategoriesByText(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_get_all_categories_by_text(self):
        add_example_user(session)
        add_example_category_consumption(session)
        expected = [example_category_consumption['category']]
        answer = ConsumptionCategoryManager.get_all_categories_by_text(session,
                                                                       example_user['telegram_user_id'])
        self.assertEqual(answer, expected)


class TestDeleteCategoryInDb(unittest.TestCase):
    def setUp(self):
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_delete_category_in_db(self):
        add_example_user(session)
        add_example_category_consumption(session)

        ConsumptionCategoryManager.delete_category_in_db(session, example_category_consumption['category'],
                                                         example_user['telegram_user_id'])
        expected = None
        answer = session.query(CategoryConsumption).get(1)
        self.assertEqual(answer, expected)

