#!/usr/bin/python3


from CS312Graph import *
import time


class NetworkRoutingSolver:
    def __init__(self):
        pass

    def initialize_network(self, network):
        assert (type(network) == CS312Graph)
        self.network = network

    def get_shortest_path(self, end_index):
        self.end = end_index
        # Erase work from array run when doing heap run
        # TODO: RETURN THE SHORTEST PATH FOR end_ndex
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

    def compute_shortest_paths(self, src_index, use_heap=False):
        self.source = src_index
        t1 = time.time()
        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)
        # Use dijkra's out of the book
        # distance array has to be visible to getShortestPath()
        # Create array implementation of a Q and a heap implementation. They should inherit the same interface.
        t2 = time.time()
        return t2 - t1
