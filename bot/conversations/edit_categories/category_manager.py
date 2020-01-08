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
    def delete_category(cls, update: Update, context: CallbackContext):
        pass

    @classmethod
    def confirm_delete_category(cls, update: Update, context: CallbackContext):
        pass

    @classmethod
    def confirm_set_default_category(cls, update: Update, context: CallbackContext):
        pass

    @classmethod
    def edit_category(cls, update: Update, context: CallbackContext):
        pass

    @classmethod
    def write_new_category(cls, update: Update, context: CallbackContext):
        pass

    @classmethod
    def confirm_edit_category(cls, update: Update, context: CallbackContext):
        pass
