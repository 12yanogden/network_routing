from Queue.Queue import Queue


class ArrayQueue(Queue):
    def __init__(self, nodes, dist):
        self.dist = dist
        self.index_table = {}
        super().__init__(nodes)

    def insert(self, node):
        self.queue.append(node)
        self.index_table[node.node_id] = len(self.queue) - 1

    def make_queue(self, nodes):
        for node in nodes:
            self.insert(node)

    def delete_min(self):
        min_value_index = 0

        for i in range(len(self.queue)):
            if self.get_dist(i) < self.get_dist(min_value_index):
                min_value_index = i

        min_value = self.queue[min_value_index]

        self.queue.pop(min_value_index)
        self.index_table.pop(min_value.node_id)

        return min_value

    def decrease_key(self, node_id):
        pass

    def is_in_queue(self, node):
        return node.node_id in self.index_table

    def get_dist(self, index):
        return self.dist[self.queue[index].node_id]

    def to_string(self):
        return super().to_string()

