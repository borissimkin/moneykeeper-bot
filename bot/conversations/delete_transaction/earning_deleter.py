from bot.conversations.delete_transaction.transaction_deleter import TransactionDeleter
from bot.models import User, Earning, CategoryEarning
from bot.utils import ruble_declension


class EarningDeleter(TransactionDeleter):
    def get_transaction(self, session):
        return session.query(Earning).get(self.transaction_id)

    def make_text_delete_transaction(self, session):
        earning = self.get_transaction(session)
        category = session.query(CategoryEarning).get(earning.category_id)
        return f'Вы уверены, что хотите удалить доход в размере <b>{earning.amount_money} ' \
            f'{ruble_declension(int(earning.amount_money))}</b> категории <b>{category.category}</b>,' \
            f' созданный в <b>{earning.get_str_time_creation()}</b>?'

    def check_exist_transaction(self, session):
        user = User.get_user_by_telegram_user_id(session,
                                                 self.telegram_user_id)
        earning = session.query(Earning).filter(
            Earning.user_id == user.id,
            Earning.id == self.transaction_id
        ).first()
        return True if earning else False

    def make_text_success_delete_transaction(self):
        return 'Вы успешно удалили доход.'

    def delete_transaction(self, session):
        earning = self.get_transaction(session)
        session.delete(earning)
        session.commit()

    def text_error_id_transaction(self):
        return f'Извините, вы не можете удалить доход с id={self.transaction_id}.'
