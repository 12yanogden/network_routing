from Queue.Queue import Queue


class HeapQueue(Queue):
    def __init__(self, nodes, dist):
        super().__init__(nodes, dist)

    # Time: O(log|V|), Space: O(log|V|)
    def insert(self, node):
        current_index = len(self.queue)

        self.queue.append(node)
        self.index_table[node.node_id] = current_index

        # Time: O(log|V|), Space: O(log|V|)
        self.bubble_up(current_index)

    # Time: O(|V|log|V|), Space: O(|V|)
    def make_queue(self, nodes):
        for node in nodes:
            self.insert(node)

    # Time: O(log|V|), Space: O(log|V|)
    def delete_min(self):
        # Swap min with last
        self.swap(0, self.get_last_index())

        # Remove min
        min_dist_node = self.queue.pop()
        self.index_table.pop(min_dist_node.node_id)

        # Bubble last down, Time: O(log|V|), Space: O(log|V|)
        self.bubble_down(0)

        # Return min
        return min_dist_node

    # Time: O(log|V|), Space: O(log|V|)
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

    def is_index_in_queue(self, index):
        return 0 <= index < len(self.queue)

    def swap(self, index1, index2):
        tmp_node = self.queue[index1]

        # Swaps nodes
        self.queue[index1] = self.queue[index2]
        self.queue[index2] = tmp_node

        # Syncs index_table
        self.index_table[self.queue[index1].node_id] = index1
        self.index_table[self.queue[index2].node_id] = index2

    # Time: O(log|V|), Space: O(log|V|)
    def bubble_up(self, current_index):
        parent_index = self.get_parent_index(current_index)

        # Iterate through O(log|V|) nodes
        while current_index > 0 and self.get_dist(current_index) < self.get_dist(parent_index):
            # Swaps to bubble up
            self.swap(current_index, parent_index)

            # Increment indexes
            current_index = parent_index
            parent_index = self.get_parent_index(current_index)

    def calc_min_child(self, parent_index, left_child_index, right_child_index):
        min_child_indexes = []
        min_child_index = -1

        # Populate min_child_indexes to indicate index eligibility
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

        # Return min_child_index
        return min_child_index

    # Time: O(log|V|), Space: O(log|V|)
    def bubble_down(self, current_index):
        left_child_index = self.get_left_child_index(current_index)
        right_child_index = self.get_right_child_index(current_index)

        # Iterate through O(log|V|) nodes
        while True:
            # Determines child to swap with
            min_child_index = self.calc_min_child(current_index, left_child_index, right_child_index)

            # Base case: break if there are no children to swap with
            if min_child_index == -1:
                break

            # Swap to bubble down
            self.swap(current_index, min_child_index)

            # Decrement indexes
            current_index = min_child_index
            left_child_index = self.get_left_child_index(current_index)
            right_child_index = self.get_right_child_index(current_index)

    def to_string(self):
        out = "Index_Table:\n"

        for index in self.index_table:
            out += str(index) + ": " + str(self.index_table[index]) + "\n"

        return super().to_string() + out
