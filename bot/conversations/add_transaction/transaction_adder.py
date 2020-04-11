import abc


class TransactionAdder(abc.ABC):
    def __init__(self, user):
        self.user = user

    def text_to_write_money(self):
        pass

    def get_keyboard_choose_categories(self, session):
        pass

    def get_categories_by_text(self, session):
        pass

    def add_transaction(self, session, amount_money, text_category, date):
        ...

    def text_success_add_transaction(self):
        ...