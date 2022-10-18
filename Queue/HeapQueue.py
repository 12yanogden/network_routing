from CS312Graph import CS312GraphNode
from Queue.Queue import Queue


class HeapQueue(Queue):
    def __init__(self, nodes, dist):
        self.index_table = {}
        self.dist = dist
        super().__init__(nodes)

    def insert(self, node):
        current_index = len(self.queue)

        self.queue.append(node)
        self.index_table[node.node_id] = current_index

        self.bubble_up(current_index)

    def make_queue(self, nodes):
        for node in nodes:
            self.insert(node)

    def delete_min(self):
        self.swap(0, self.get_last_index())

        min_dist_node = self.queue.pop()
        self.index_table.pop(min_dist_node.node_id)

        self.bubble_down(0)

        return min_dist_node

    def decrease_key(self, node_id):
        self.bubble_up(self.index_table[node_id])

    def get_parent_index(self, child_index):
        return child_index // 2

    def get_left_child_index(self, parent_index):
        return 2 * parent_index + 1

    def get_right_child_index(self, parent_index):
        return 2 * parent_index + 2

    def get_last_index(self):
        return len(self.queue) - 1

    def swap(self, index1, index2):
        tmp_node = self.queue[index1]

        self.queue[index1] = self.queue[index2]
        self.queue[index2] = tmp_node

        self.index_table[self.queue[index1].node_id] = index1
        self.index_table[self.queue[index2].node_id] = index2

    def is_in_queue(self, node):
        return node.node_id in self.index_table

    def is_index_in_queue(self, index):
        return 0 <= index < len(self.queue)

    def bubble_up(self, current_index):
        parent_index = self.get_parent_index(current_index)

        while current_index > 0 and self.get_dist(current_index) < self.get_dist(parent_index):
            self.swap(current_index, parent_index)

            current_index = parent_index
            parent_index = self.get_parent_index(current_index)

    def calc_min_child(self, parent_index, left_child_index, right_child_index):
        min_child_indexes = []
        min_child_index = -1

        # Populate min_child_indexes
        if self.is_index_in_queue(left_child_index) and self.get_dist(left_child_index) < self.get_dist(parent_index):
            min_child_indexes.append(left_child_index)

        if self.is_index_in_queue(right_child_index) and self.get_dist(right_child_index) < self.get_dist(parent_index):
            min_child_indexes.append(right_child_index)

        # Determine min_child_index
        if len(min_child_indexes) == 1:
            min_child_index = min_child_indexes[0]

        elif len(min_child_indexes) == 2:
            if self.get_dist(min_child_indexes[0]) < self.get_dist(min_child_indexes[1]):
                min_child_index = min_child_indexes[0]

            elif self.get_dist(min_child_indexes[1]) < self.get_dist(min_child_indexes[0]):
                min_child_index = min_child_indexes[1]

            else:
                min_child_index = min_child_indexes[0]

        return min_child_index

    def get(self, index):
        if not self.is_index_in_queue(index):
            return CS312GraphNode(-1, -1)
        else:
            return self.queue[index]

    def bubble_down(self, current_index):
        left_child_index = self.get_left_child_index(current_index)
        right_child_index = self.get_right_child_index(current_index)

        while True:
            min_child_index = self.calc_min_child(current_index, left_child_index, right_child_index)

            if min_child_index == -1:
                break

            self.swap(current_index, min_child_index)

            current_index = min_child_index
            left_child_index = self.get_left_child_index(current_index)
            right_child_index = self.get_right_child_index(current_index)

    def get_dist(self, index):
        if not self.is_index_in_queue(index):
            return -1

        return self.dist[self.queue[index].node_id]

    def to_string(self):
        out = "Index_Table:\n"

        for index in self.index_table:
            out += str(index) + ": " + str(self.index_table[index]) + "\n"

        return super().to_string() + out
