#!/usr/bin/python3
import math

from CS312Graph import *
import time


class PQArray:
    """
        A class that acts as our priority queue for the array implementation

        Attributes:
            dist acts as our distance map from index (node id) to distance (originally infinity for all of them)
            q_array is our queue, where we keep the nodes we need to visit in an unordered manner
    """

    def __init__(self, nodes):
        # Set all nodes = to infinity
        self.dist = [math.inf] * len(nodes)
        self.q_array = set()

    def insert(self, node_index):
        self.q_array.add(node_index)
        return

    def decrease_key(self, dist, node_index):
        self.dist[node_index] = dist
        return

    def delete_min(self):

        # Note: minimum is the index of the lowest node, not it's value
        minimum = None
        for i in range(len(self.dist)):
            # Check to see if it's in the PQ
            if i in self.q_array:

                if minimum is None:
                    minimum = i

                # If in pq, compare the new node's value to the current minimum value. If lower, make curr
                #   index the new minimum
                if self.dist[i] < self.dist[minimum]:
                    minimum = i
        temp = minimum
        self.q_array.remove(minimum)

        # We're returning the index here, not the node
        return temp


class HeapArray:
    """
        A class that acts as our priority queue for the heap implementation

        Attributes:
            dist acts as our distance map from index (node id) to distance (originally infinity for all of them)
            q_heap is our queue, where we keep the nodes we need to visit in an ordered manner
            q_pointer keeps track of the indices of nodes in our q_heap so that we can access them quickly
    """

    def __init__(self, nodes):
        self.dist = [math.inf] * len(nodes)
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
        self.prev_array = None
        self.cost = None


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
        curr_node_index = destIndex

        while True:

            # Is this the only check we need, or do we need the lower two as well?
            if self.prev_array[curr_node_index] is None:
                return {'cost': math.inf, 'path': []}

            prev_node = self.network.nodes[self.prev_array[curr_node_index]]
            if prev_node.neighbors is None:
                return {'cost': math.inf, 'path': []}

            edge = None
            for neighbor in prev_node.neighbors:
                if neighbor.dest.node_id == curr_node_index:
                    edge = neighbor
                    break

            if edge is None:
                return {'cost': math.inf, 'path': []}

            # Note: this returns a QT edge, not a 312GraphEdge
            path_edges.append((edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)))

            total_length += edge.length

            curr_node_index = prev_node.node_id
            if edge.src.node_id == self.source:
                break

        return {'cost': total_length, 'path': path_edges}

    def computeShortestPaths(self, srcIndex, use_heap=False):
        self.source = srcIndex
        t1 = time.time()
        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)
        #       Need to make new class members to store cost and shortest path
        # if use_heap:
        # heap implementation of Dijkstra's
        # else:
        # array implementation of Dijkstra's
        pq_array = PQArray.__new__(PQArray)
        pq_array.__init__(self.network.nodes)
        pq_array.insert(srcIndex)
        pq_array.decrease_key(0, srcIndex)
        self.prev_array = [None] * len(self.network.nodes)
        while pq_array.q_array:
            curr_min_node_index = pq_array.delete_min()
            curr_node = self.network.nodes[curr_min_node_index]
            for edge in curr_node.neighbors:
                if (pq_array.dist[edge.dest.node_id] >
                        pq_array.dist[curr_min_node_index] + edge.length):
                    node_index = edge.dest.node_id
                    new_distance = pq_array.dist[curr_min_node_index] + edge.length
                    pq_array.insert(node_index)
                    pq_array.decrease_key(new_distance, node_index)
                    self.prev_array[edge.dest.node_id] = curr_min_node_index

        t2 = time.time()
        return (t2 - t1)
