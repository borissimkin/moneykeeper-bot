import abc

from telegram import Update
from telegram.ext import CallbackContext


class CategoryManager(abc.ABC):
    @staticmethod
    def make_text_list_categories(session, telegram_user_id):
        pass

    @staticmethod
    def check_any_categories(session, telegram_user_id):
        pass

    @staticmethod
    def text_confirm_add_category(new_category: str):
        pass

    @staticmethod
    def add_category_in_db(session, new_category: str, telegram_user_id):
        pass

    @staticmethod
    def text_success_add_category(new_category: str):
        pass

    @classmethod
    def confirm_add_category(cls, update: Update, context: CallbackContext):
        pass

    @classmethod
    def get_all_categories(cls, session, telegram_user_id):
        pass

    @classmethod
    def get_all_categories_by_text(cls, session, telegram_user_id):
        pass

    @classmethod
    def text_confirm_delete_category(cls, category: str):
        pass

    @classmethod
    def delete_category_in_db(cls, session, category: str, telegram_user_id):
        pass

    @classmethod
    def text_success_delete(cls, category: str):
        pass
