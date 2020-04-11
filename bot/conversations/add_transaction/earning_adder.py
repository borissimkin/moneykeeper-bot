from telegram import ReplyKeyboardMarkup

from bot import config
from bot.conversations.add_transaction.transaction_adder import TransactionAdder
from bot.keyboards import make_buttons_for_choose_category
from bot.models import CategoryEarning, Earning
from bot.utils import add_buttons_exit_and_back


class EarningAdder(TransactionAdder):
    def text_to_write_money(self):
        return 'Введите количество денег, которое вы получили.'

    def get_keyboard_choose_categories(self, session):
        categories = CategoryEarning.get_all_categories(session, self.user.id)
        buttons = make_buttons_for_choose_category(config['buttons_per_row'],
                                                   categories)
        return ReplyKeyboardMarkup(add_buttons_exit_and_back(buttons),
                                   resize_keyboard=True)

    def get_categories_by_text(self, session):
        return CategoryEarning.get_all_categories_by_text(session, self.user.id)

    def add_transaction(self, session, amount_money, text_category, date):
        category = session.query(CategoryEarning).filter(
            CategoryEarning.category == text_category,
            CategoryEarning.user_id == self.user.id
        ).first()
        session.add(Earning(user_id=self.user.id,
                            category_id=category.id,
                            amount_money=amount_money,
                            time_creation=date))
        session.commit()

    def text_success_add_transaction(self):
        return 'Доход успешно записан!'
