#!/usr/bin/python3
import math

from Queue.ArrayQueue import ArrayQueue
from CS312Graph import *
import time

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

    def initialize_dist_prev(self):
        for node in self.network.nodes:
            self.dist[node.node_id] = math.inf
            self.prev[node.node_id] = None

    def get_edge(self, src_index, end_index):
        for neighbor in self.network.nodes[src_index].neighbors:
            if neighbor.end.node_id == end_index:
                return neighbor

        raise Exception("prev[" + src_index + "] neighbors does not contain node " + end_index)

    def get_shortest_path(self, end_index):
        self.end = end_index

        current_index = end_index
        path_edges = []
        cost = 0

        if self.prev[end_index] is None:
            cost = float('inf')

        else:
            while self.prev[current_index] != current_index:
                edge = self.get_edge(self.prev[current_index], current_index)
                cost += edge.length

                path_edges.append((edge.src.loc, edge.end.loc, '{:.0f}'.format(edge.length)))

                current_index = self.prev[current_index]

        return {'cost': cost, 'path': path_edges}

    def make_queue(self, use_heap):
        if use_heap:
            return HeapQueue(self.network.nodes, self.dist)
        else:
            return ArrayQueue(self.network.nodes, self.dist)

    def compute_shortest_paths(self, src_index, use_heap=False):
        self.source = src_index

        t1 = time.time()

        self.initialize_dist_prev()                         # Time: O(n), Space: O(n)

        self.dist[src_index] = 0
        self.prev[src_index] = src_index

        queue = self.make_queue(use_heap)                   # See ArrayQueue and HeapQueue

        while not queue.is_empty():                         # Time: O(n), Space: O(1)
            min_node = queue.delete_min()                   # See ArrayQueue and HeapQueue

            for neighbor in min_node.neighbors:
                src_node_id = min_node.node_id
                end_node_id = neighbor.end.node_id

                if self.dist[end_node_id] > self.dist[src_node_id] + neighbor.length:
                    self.dist[end_node_id] = self.dist[src_node_id] + neighbor.length
                    self.prev[end_node_id] = src_node_id

                    if queue.is_in_queue(neighbor.end):
                        queue.decrease_key(end_node_id)     # See ArrayQueue and HeapQueue

        t2 = time.time()

        return t2 - t1
