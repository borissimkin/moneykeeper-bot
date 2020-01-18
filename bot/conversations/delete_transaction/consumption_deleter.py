from bot.conversations.delete_transaction.transaction_deleter import TransactionDeleter
from bot.models import User, Consumption, CategoryConsumption
from bot.utils import ruble_declension


class ConsumptionDeleter(TransactionDeleter):
    def get_transaction(self):
        return self.session.query(Consumption).get(self.transaction_id)

    def make_text_delete_transaction(self):
        consumption = self.get_transaction()
        category = self.session.query(CategoryConsumption).get(consumption.category_id)
        return f'Вы уверены, что хотите удалить расход в размере <b>{consumption.amount_money} ' \
            f'{ruble_declension(int(consumption.amount_money))}</b> категории <b>{category.category}</b>,' \
            f' созданный в <b>{consumption.get_str_time_creation()}</b>?'

    def check_exist_transaction(self):
        user = User.get_user_by_telegram_user_id(self.session,
                                                 self.telegram_user_id)
        consumption = self.session.query(Consumption).filter(
            Consumption.user_id == user.id,
            Consumption.id == self.transaction_id
        ).first()
        return True if consumption else False

    def make_text_success_delete_transaction(self):
        return 'Вы успешно удалили расход.'

    def delete_transaction(self):
        consumption = self.get_transaction()
        self.session.delete(consumption)
        self.session.commit()

    def text_error_id_transaction(self):
        return f'Извините, вы не можете удалить расход с id={self.transaction_id}.'



