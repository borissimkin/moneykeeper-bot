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
