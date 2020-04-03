class GraphController:
    def __init__(self, path_to_current_graph, time_period, type_transactions):
        self.path_to_current_graph = path_to_current_graph
        self.time_period = time_period
        self.type_transactions = type_transactions

    def update_time_period(self, time_period):
        self.time_period = time_period

    def update_path_to_current_graph(self, new_path):
        self.path_to_current_graph = new_path

    def update_type_transactions(self, type_transactions):
        self.type_transactions = type_transactions
