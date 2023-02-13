#!/usr/bin/python3


from CS312Graph import *
import time


class PQArray:
    """
        A class that acts as our priority queue for the array implementation

        Attributes:
            dist acts as our distance map from index (node id) to distance (originally infinity for all of them)
            q_array is our queue, where we keep the nodes we need to visit in an unordered manner
    """

    def __init__(self):
        self.dist = []
        self.q_array = []

    def insert(self, node):
        return

    def decrease_key(self, node):
        return

    def delete_min(self):
        return


class HeapArray:
    """
        A class that acts as our priority queue for the heap implementation

        Attributes:
            dist acts as our distance map from index (node id) to distance (originally infinity for all of them)
            q_heap is our queue, where we keep the nodes we need to visit in an ordered manner
            q_pointer keeps track of the indices of nodes in our q_heap so that we can access them quickly
    """
    def __init__(self):
        self.dist = []
        self.q_heap = []
        self.q_pointer = []

    def insert(self, node):
        return

    def decrease_key(self, node):
        return

    def delete_min(self):
        return


class NetworkRoutingSolver:
    def __init__(self):
        pass

    def initializeNetwork(self, network):
        assert (type(network) == CS312Graph)
        self.network = network

    def getShortestPath(self, destIndex):
        self.dest = destIndex
        # TODO: RETURN THE SHORTEST PATH FOR destIndex
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL 
        #       NEED TO USE
        path_edges = []
        total_length = 0
        node = self.network.nodes[self.source]
        edges_left = 3
        while edges_left > 0:
            edge = node.neighbors[2]
            path_edges.append((edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)))
            total_length += edge.length
            node = edge.dest
            edges_left -= 1
        return {'cost': total_length, 'path': path_edges}

    def computeShortestPaths(self, srcIndex, use_heap=False):
        self.source = srcIndex
        t1 = time.time()
        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)
        # if use_heap:
            # heap implementation of Dijkstra's
        # else:
            # array implementation of Dijkstra's

        # Need this call to return the shortest path to the GUI once we find it with Dijkstra's
        # self.getShortestPath(destIndex=srcIndex):
            
        t2 = time.time()
        return (t2 - t1)
