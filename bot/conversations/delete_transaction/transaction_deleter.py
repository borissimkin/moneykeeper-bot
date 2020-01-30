import abc


class TransactionDeleter(abc.ABC):
    def __init__(self, transaction_id, telegram_user_id):
        self.transaction_id = transaction_id
        self.telegram_user_id = telegram_user_id

    def get_transaction(self, session):
        pass

    def make_text_delete_transaction(self, session):
        pass

    def make_text_success_delete_transaction(self):
        pass

    def delete_transaction(self, session):
        pass

    def check_exist_transaction(self, session):
        pass

    def text_error_id_transaction(self):
        pass
