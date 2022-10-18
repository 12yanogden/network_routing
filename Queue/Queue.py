from abc import ABC, abstractmethod


class Queue(ABC):
    def __init__(self, nodes, dist):
        self.dist = dist
        self.index_table = {}
        self.queue = []
        self.make_queue(nodes)

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

    def is_empty(self):
        return len(self.queue) == 0

    def is_in_queue(self, node):
        return node.node_id in self.index_table

    def get_dist(self, index):
        return self.dist[self.queue[index].node_id]

    @abstractmethod
    def to_string(self):
        out = "Queue:\n"

        for i in range(len(self.queue)):
            out += str(i) + ": " + str(self.queue[i]) + "\n"

        return out
