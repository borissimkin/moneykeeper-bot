from bot.conversations.edit_categories.category_manager import CategoryManager


def text_choose_earning_or_consumption():
    return 'Для какого типа транзакций вы хотите изменить категории?'


def text_exit_point():
    return 'Вы вышли из диалога изменения категорий.'


def text_timeout():
    return 'Вы вышли из диалога изменения категорий из-за бездействия.'


def text_add_category():
    return 'Введите название новой категории.'


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
               'Удалить категорию - <b>Удалить</b>.\n' \
               '<b>ВНИМАНИЕ!</b> Удаляя категорию, пропадут записи с данной категорией.'

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
