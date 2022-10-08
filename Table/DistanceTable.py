from Table import Table
import math


class DistanceTable(Table):
    def __init__(self):
        super().__init__()

    def initialize_table(self, point_count):
        for i in range(point_count):
            self.values[i] = math.inf
