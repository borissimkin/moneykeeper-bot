from telegram import ReplyKeyboardMarkup

from bot import config
from bot.conversations.add_transaction.transaction_adder import TransactionAdder
from bot.keyboards import make_buttons_for_choose_category
from bot.models import CategoryConsumption, Consumption
from bot.utils import add_buttons_exit_and_back


class ConsumptionAdder(TransactionAdder):
    def text_to_write_money(self):
        return 'Введите количество денег, которое вы потратили.'

    def get_keyboard_choose_categories(self, session):
        consumption_categories = CategoryConsumption.get_all_categories(session, self.user.id)
        buttons = make_buttons_for_choose_category(config['buttons_per_row'],
                                                   consumption_categories)
        return ReplyKeyboardMarkup(add_buttons_exit_and_back(buttons),
                                   resize_keyboard=True)

    def get_categories_by_text(self, session):
        return CategoryConsumption.get_all_categories_by_text(session, self.user.id)

    def add_transaction(self, session, amount_money, text_category, date):
        category = session.query(CategoryConsumption).filter(
            CategoryConsumption.category == text_category,
            CategoryConsumption.user_id == self.user.id
        ).first()
        session.add(Consumption(user_id=self.user.id,
                                category_id=category.id,
                                amount_money=amount_money,
                                time_creation=date))
        session.commit()

    def text_success_add_transaction(self):
        return 'Расход успешно записан!'


