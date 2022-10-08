#!/usr/bin/python3
from Queue.ArrayQueue import ArrayQueue
from CS312Graph import *
import time

from Table.DistanceTable import DistanceTable
from Queue.HeapQueue import HeapQueue
from Table.PrevTable import PrevTable


class NetworkRoutingSolver:
    def __init__(self):
        self.source = None
        self.end = None
        self.network = None

    def initialize_network(self, network):
        assert (type(network) == CS312Graph)
        self.network = network

    def get_shortest_path(self, end_index):
        self.end = end_index
        # Erase work from array run when doing heap run
        # TODO: RETURN THE SHORTEST PATH FOR end_index
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL 
        #       NEED TO USE
        path_edges = []
        total_length = 0
        node = self.network.nodes[self.source]
        edges_left = 3
        while edges_left > 0:
            edge = node.neighbors[2]
            path_edges.append((edge.src.loc, edge.end.loc, '{:.0f}'.format(edge.length)))
            total_length += edge.length
            node = edge.end
            edges_left -= 1
        return {'cost': total_length, 'path': path_edges}

    def make_queue(self, use_heap):
        if use_heap:
            return HeapQueue()
        else:
            return ArrayQueue()

    def compute_shortest_paths(self, src_index, use_heap=False):
        self.source = src_index
        t1 = time.time()
        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO get_shortest_path(end_index)

        dist = DistanceTable(len(self.network.nodes))
        prev = PrevTable(len(self.network.nodes))

        dist.set(0, src_index)

        queue = self.make_queue(use_heap)

        while queue.is_empty():
            queue.delete_min()

        # What is V? What is the dist table or prev table?

        # self.network.nodes = V
        # node.neighbors = E

        # for all u in V:
        #     dist(u) = infinity
        #     prev(u) = nil
        # dist(s) = 0
        #
        # H = make_queue(V)
        # while H is not empty:
        #     u = delete_min(H) TODO: What point is being returned here?
        #     for all edges (u, v) in E:
        #         if dist(v) > dist(u) + l(u, v): (node.neighbors are edges with weights that are l(u, v))
        #             dist(v) = dist(u) + l(u, v)
        #             prev(v) = u
        #             decrease_key(H, v) TODO: What is the key?

        # Use dijkstra's out of the book
        # distance array has to be visible to getShortestPath()
        # Create array implementation of a Q and a heap implementation. They should inherit the same interface.
        t2 = time.time()
        return t2 - t1
