from bot.conversations.edit_categories.category_manager import CategoryManager
from bot.models import CategoryEarning, User


class EarningCategoryManager(CategoryManager):
    @staticmethod
    def check_any_categories(session, telegram_user_id):
        categories = session.query(CategoryEarning).filter(
            CategoryEarning.user_id == User.get_user_by_telegram_user_id(session, telegram_user_id).id).all()
        return True if categories else False

    @staticmethod
    def make_text_list_categories(session, telegram_user_id):
        user = User.get_user_by_telegram_user_id(session, telegram_user_id)
        categories_text = CategoryEarning.get_all_categories_by_text(session=session,
                                                                     user_id=user.id)
        result = ''
        for index, text in enumerate(categories_text):
            result += f'{index+1}. {text}\n'
        return result

    @staticmethod
    def add_category_in_db(session, new_category, telegram_user_id):
        user = User.get_user_by_telegram_user_id(session, telegram_user_id)
        CategoryEarning.add_category(session, user.id, new_category)

    @staticmethod
    def text_confirm_add_category(new_category):
        return f'Вы уверены, что хотите добавить <b>{new_category}</b> в категории <b>доходов</b>?'

    @staticmethod
    def text_success_add_category(new_category: str):
        return f'Новая категория доходов - <b>{new_category}</b> успешно добавлена!'

    @classmethod
    def get_all_categories(cls, session, telegram_user_id):
        user = session.query(User).filter(User.telegram_user_id == telegram_user_id).first()
        return CategoryEarning.get_all_categories(session, user.id)

    @classmethod
    def get_all_categories_by_text(cls, session, telegram_user_id):
        user = session.query(User).filter(User.telegram_user_id == telegram_user_id).first()
        return CategoryEarning.get_all_categories_by_text(session, user.id)

    @classmethod
    def text_confirm_delete_category(cls, category: str):
        return f'Вы уверены что хотите удалить <b>{category}</b> в категориях <b>доходов</b>?'

    @classmethod
    def delete_category_in_db(cls, session, category: str, telegram_user_id):
        user = session.query(User).filter(User.telegram_user_id == telegram_user_id).first()
        category = session.query(CategoryEarning).filter(CategoryEarning.category == category,
                                                         CategoryEarning.user_id == user.id).first()
        category.delete_category(session)

    @classmethod
    def text_success_delete(cls, category: str):
        return f'Категория <b>{category}</b> в <b>доходах</b> успешно удалена!'
