import abc


class TransactionDeleter(abc.ABC):
    def __init__(self, transaction_id, telegram_user_id, session):
        self.transaction_id = transaction_id
        self.telegram_user_id = telegram_user_id
        self.session = session

    def get_transaction(self):
        pass

    def make_text_delete_transaction(self):
        pass

    def make_text_success_delete_transaction(self):
        pass

    def delete_transaction(self):
        pass

    def check_exist_transaction(self):
        pass

    def text_error_id_transaction(self):
        pass
