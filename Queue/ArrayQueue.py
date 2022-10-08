from Queue import Queue


class ArrayQueue(Queue):
    def __init__(self):
        super().__init__()

    def is_empty(self):
        if len(self.queue) == 0:
            return True
        else:
            return False

    def insert(self, value):
        self.queue.append(value)

    def make_queue(self, values):
        for value in values:
            self.insert(value)

    def delete_min(self):
        min_value = self.queue[0]

        for i in range(len(self.queue)):
            if 0 < self.queue[i] < min_value:
                min_value = self.queue[i]
                self.queue[i] = -1

        return min_value

    def decrease_key(self):
        pass


