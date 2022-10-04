#!/usr/bin/python3


class CS312GraphEdge:
    def __init__(self, src_node, end_node, edge_length):
        self.src = src_node
        self.end = end_node
        self.length = edge_length

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '(src={} end={} length={})'.format(self.src, self.end, self.length)


class CS312GraphNode:
    def __init__(self, node_id, node_loc):
        self.node_id = node_id
        self.loc = node_loc
        self.neighbors = []  # node_neighbors

    # Not to be called by solver
    def add_edge(self, neighbor_node, weight):
        self.neighbors.append(CS312GraphEdge(self, neighbor_node, weight))

    def __str__(self):
        neighbors = [edge.end.node_id for edge in self.neighbors]
        return 'Node(id:{},neighbors:{})'.format(self.node_id, neighbors)


class CS312Graph:
    def __init__(self, node_list, edge_list):
        self.nodes = []
        for i in range(len(node_list)):
            self.nodes.append(CS312GraphNode(i, node_list[i]))

        for i in range(len(node_list)):
            neighbors = edge_list[i]
            for n in neighbors:
                self.nodes[i].add_edge(self.nodes[n[0]], n[1])
        
    def __str__(self):
        s = []
        for n in self.nodes:
            s.append(n.neighbors)
        return str(s)

    def get_nodes(self):
        return self.nodes
