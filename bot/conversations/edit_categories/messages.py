from bot.conversations.edit_categories.category_manager import CategoryManager


def text_choose_earning_or_consumption():
    return 'Для какого типа транзакций вы хотите изменить категории?'


def text_exit_point():
    return 'Вы вышли из диалога изменения категорий.'


def text_timeout():
    return 'Вы вышли из диалога изменения категорий из-за бездействия.'


def text_add_category():
    return 'Введите название новой категории.'


def text_warning_delete_category():
    return '<b>ВНИМАНИЕ!</b> Удаляя категорию, пропадут все записи с данной категорией.'


def text_edit_category():
    return 'Выберите категорию, которую хотите изменить.'


def text_write_edit_category(category: str):
    return f'Введите новую категеорию, вместо <b>{category}</b>'


def text_confirm_edit_category(old_category: str, new_category: str):
    return f'Вы уверены, что хотите изменить <b>{old_category}</b> на <b>{new_category}</b>'


def text_delete_category(session, telegram_user_id, category_manager: CategoryManager):
    text_categories = category_manager.make_text_list_categories(session, telegram_user_id)
    return f'Выберите категорию для удаления.\n' \
           f'\n{text_categories}'


class TextMenuManageCategories:
    @staticmethod
    def classic_text_manage_categories():
        return 'Вы находитесь в меню управления категориями.'

    @staticmethod
    def text_instruction_empty_categories():
        return 'На данный момент у вас нет каких-либо категорий.\n' \
               'Нажмите добавить чтобы добавить категорию.'

    @staticmethod
    def text_instruction_not_empty_categories():
        return 'Чтобы добавить категорию нажмите <b>Добавить</b>.\n' \
               'Изменить одну из существующих категорий - <b>Изменить</b>.\n' \
               'Удалить категорию - <b>Удалить</b>.\n'

    @classmethod
    def make_text_menu_manage_categories(cls, session, telegram_user_id, category_manager: CategoryManager):
        if category_manager.check_any_categories(session, telegram_user_id):
            text_categories = category_manager.make_text_list_categories(session, telegram_user_id)
            return f'{cls.classic_text_manage_categories()}\n' \
                f'{cls.text_instruction_not_empty_categories()}\n' \
                f'\nТекущие категории:\n' \
                f'\n{text_categories}'
        else:
            return f'{cls.classic_text_manage_categories()}\n' \
                f'{cls.text_instruction_empty_categories()}'
