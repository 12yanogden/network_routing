from abc import ABC, abstractmethod


class Queue(ABC):
    def __init__(self):
        self.queue = []

    @abstractmethod
    def is_empty(self):
        pass

    @abstractmethod
    def insert(self):
        pass

    @abstractmethod
    def make_queue(self):
        pass

    @abstractmethod
    def delete_min(self):
        pass

    @abstractmethod
    def decrease_key(self):
        pass
