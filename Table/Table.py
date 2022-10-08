from abc import ABC, abstractmethod


class Table(ABC):
    def __init__(self, value_count):
        self.values = []
        self.initialize_table(value_count)

    @abstractmethod
    def initialize_table(self, value_count):
        pass

    def get(self, index):
        return self.values[index]

    def set(self, index, value):
        self.values[index] = value

    def swap(self, index1, index2):
        tmp_value = self.values[index1]
        self.values[index1] = self.values[index2]
        self.values[index2] = tmp_value
