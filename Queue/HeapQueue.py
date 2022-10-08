from Queue import Queue
from Table.IndexTable import IndexTable


class HeapQueue(Queue):
    def __init__(self):
        super().__init__()
        self.index_table = IndexTable

    def is_empty(self):
        if len(self.queue) == 0:
            return True
        else:
            return False

    def insert(self, value):
        current_index = len(self.queue)
        self.queue[current_index] = value

        while current_index != 0 and self.queue[current_index] < self.queue[self.get_parent_index(current_index)]:
            self.swap(current_index, self.get_parent_index(current_index))

    def delete_min(self):
        self.swap(0, self.get_last_index())
        min_value = self.queue.pop()
        current_index = 0
        left_child_index = self.get_left_child_index(current_index)
        right_child_index = self.get_right_child_index(current_index)

        # Check if left is in array
        # Check if right is in the array

        # Check if current is larger than both children
            # swap with least of children

        return min_value

    def decrease_dist(self, point, dist):
        # get point from index_table
        # adjust dist
        pass

    def get_parent_index(self, child_index):
        return child_index // 2

    def get_left_child_index(self, parent_index):
        return 2 * parent_index + 1

    def get_right_child_index(self, parent_index):
        return 2 * parent_index + 2

    def get_last_index(self):
        return len(self.queue) - 1

    def swap(self, index1, index2):
        tmp_value = self.queue[index1]
        self.queue[index1] = self.queue[index2]
        self.queue[index2] = tmp_value

        # adjust index_table?


    def bubble_up(self, x, i):
        p = i // 2

        while i != 1 and True:
            break


    def bubble_down(self):
        pass
