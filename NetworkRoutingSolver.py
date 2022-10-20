#!/usr/bin/python3
import math
import time
from CS312Graph import *
from Queue.ArrayQueue import ArrayQueue
from Queue.HeapQueue import HeapQueue


class NetworkRoutingSolver:
    def __init__(self):
        self.source = None
        self.end = None
        self.network = None
        self.dist = {}
        self.prev = {}

    def initialize_network(self, network):
        assert (type(network) == CS312Graph)
        self.network = network

    # Time: O(|V|), Space: O(|V|)
    def initialize_dist_prev(self):
        for node in self.network.nodes:
            self.dist[node.node_id] = math.inf
            self.prev[node.node_id] = None

    # Time: O(|V|), Space: O(|V|)
    def get_shortest_path(self, end_index):
        self.end = end_index

        current_index = end_index
        path_edges = []

        # Iterate over O(|E|) edges
        while self.prev[current_index] != current_index:
            prev_index = self.prev[current_index]

            path_edges.append((self.network.nodes[current_index].loc, self.network.nodes[prev_index].loc,
                               '{:.0f}'.format(self.dist[current_index] - self.dist[prev_index])))

            current_index = prev_index

        return {'cost': self.dist[end_index], 'path': path_edges}

    def make_queue(self, use_heap):
        if use_heap:
            return HeapQueue(self.network.nodes, self.dist)
        else:
            return ArrayQueue(self.network.nodes, self.dist)

    # Time: Array: O(|V|^2), Heap: O((|V| + |E|)log|V|)
    # Space: Array: O(|V|), Heap: O(|V|)
    def compute_shortest_paths(self, src_index, use_heap=False):
        self.source = src_index

        t1 = time.time()

        # Time: O(|V|), Space: O(|V|)
        self.initialize_dist_prev()

        self.dist[src_index] = 0
        self.prev[src_index] = src_index

        # Time: Array: O(|V|), Heap: O(|V|log|V|)
        # Space: Array: O(|V|), Heap: O(|V|)
        queue = self.make_queue(use_heap)

        # Iterates over O(|V|) nodes in the queue
        # Time: Array: O(|V|^2), Heap: O((|V| + |E|)log|V|)
        # Space: Array: O(|V|), Heap: O(|V|)
        while not queue.is_empty():
            # Time: Array: O(|V|), Heap: O(log|V|)
            # Space: Array: O(|V|), Heap: O(log|V|)
            min_node = queue.delete_min()

            # Will ultimately iterate over O(|E|) edges
            for neighbor in min_node.neighbors:
                src_node_id = min_node.node_id
                end_node_id = neighbor.end.node_id

                if self.dist[end_node_id] > self.dist[src_node_id] + neighbor.length:
                    self.dist[end_node_id] = self.dist[src_node_id] + neighbor.length
                    self.prev[end_node_id] = src_node_id

                    if queue.is_in_queue(neighbor.end):
                        # Time: Array: O(1), Heap: O(log|V|)
                        # Space: Array: O(1), Heap: O(log|V|)
                        queue.decrease_key(end_node_id)

        t2 = time.time()

        return t2 - t1
