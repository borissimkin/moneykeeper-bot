from bot import config


class TransactionsController:
    def __init__(self, transactions):
        self.transactions = transactions
        self.count_elements_in_part = config['view_transactions']['count_transactions_in_list']
        self.first_index_part = 0
        self.last_index_part = 0
        self.init_indexes()

    def init_indexes(self):
        if len(self.transactions) <= self.count_elements_in_part:
            self.last_index_part = len(self.transactions)
        else:
            self.last_index_part = self.count_elements_in_part

    def next(self):
        prev_last_index_part = self.last_index_part
        if self.last_index_part + self.count_elements_in_part >= len(self.transactions):
            self.last_index_part = len(self.transactions)
        else:
            self.last_index_part += self.count_elements_in_part
        self.first_index_part = prev_last_index_part
        return self.get_current_part()

    def previous(self):
        prev_first_index_part = self.first_index_part
        if self.first_index_part - self.count_elements_in_part <= 0:
            self.first_index_part = 0
        else:
            self.first_index_part -= self.count_elements_in_part
        self.last_index_part = prev_first_index_part
        return self.get_current_part()

    def get_current_part(self):
        return self.transactions[self.first_index_part:self.last_index_part]
