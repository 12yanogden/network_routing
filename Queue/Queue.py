from abc import ABC, abstractmethod


class Queue(ABC):
    def __init__(self, nodes):
        self.queue = []
        self.make_queue(nodes)

    def is_empty(self):
        return len(self.queue) == 0

    @abstractmethod
    def insert(self, node):
        pass

    @abstractmethod
    def make_queue(self, nodes):
        pass

    @abstractmethod
    def delete_min(self):
        pass

    @abstractmethod
    def decrease_key(self, node_id):
        pass

    @abstractmethod
    def is_in_queue(self, node):
        pass

    @abstractmethod
    def to_string(self):
        out = "Queue:\n"

        for i in range(len(self.queue)):
            out += str(i) + ": " + str(self.queue[i]) + "\n"

        return out
