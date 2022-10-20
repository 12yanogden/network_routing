from Queue.Queue import Queue


class ArrayQueue(Queue):
    def __init__(self, nodes, dist):
        super().__init__(nodes, dist)

    # Time: O(1), Space: O(1)
    def insert(self, node):
        self.queue.append(node)
        self.index_table[node.node_id] = len(self.queue) - 1

    # Time: O(|V|), Space: O(|V|)
    def make_queue(self, nodes):
        for node in nodes:
            self.insert(node)

    # Time: O(|V|), Space: O(|V|)
    def delete_min(self):
        min_value_index = 0

        # Iterate through O(|V|) nodes
        for i in range(len(self.queue)):
            if self.get_dist(i) < self.get_dist(min_value_index):
                min_value_index = i

        min_value = self.queue[min_value_index]

        # Remove min_value
        self.queue.pop(min_value_index)
        self.index_table.pop(min_value.node_id)

        return min_value

    # Time: O(1), Space: O(1)
    def decrease_key(self, node_id):
        pass

    def to_string(self):
        return super().to_string()

