from Table import Table


class PointerTable(Table):
    def __init__(self):
        super().__init__()

    def initialize_table(self, value_count):
        for i in range(value_count):
            self.values[i] = None
