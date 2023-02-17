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
        self.dist = [math.inf] * len(nodes)

        # 0 if the node is not in the queue, change to 1 if it is
        # self.q_array = [0] * len(nodes)
        self.q_array = set()

    def insert(self, node_index):
        # self.q_array[node_index] = 1
        self.q_array.add(node_index)
        return

    def decrease_key(self, dist, node_index):
        self.dist[node_index] = dist
        return

    def delete_min(self):

        # minimum is the index of the lowest node, not it's actual value
        minimum = 0
        for i in range(len(self.dist)):
            # Check to see if it's in the PQ
            if i in self.q_array:
                # If in pq, compare the new node's value to the current minimum value. If lower, make curr
                #   index the new minimum
                if self.dist[i] < self.dist[minimum]:
                    minimum = i
        # temp = self.dist[minimum]
        # self.q_array[minimum] = 0
        temp = minimum
        self.q_array.remove(minimum)

        # TODO: does this return the node or the index to the node? depends on the implementation of the other side
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
        #       Need to make new class members to store cost and shortest path
        # if use_heap:
        # heap implementation of Dijkstra's
        # else:
        # array implementation of Dijkstra's
        pq_array = PQArray.__new__(PQArray)
        pq_array.__init__(self.network.nodes)
        pq_array.insert(srcIndex)
        pq_array.decrease_key(0, srcIndex)
        prev_array = [None] * len(self.network.nodes)
        while pq_array.q_array:
            curr_min_node_index = pq_array.delete_min()
            curr_node = self.network.nodes[curr_min_node_index]
            for edge in curr_node.neighbors:
                if (pq_array.dist[edge.dest.node_id] >
                        pq_array.dist[curr_min_node_index] + edge.length):
                    node_index = edge.dest.node_id
                    new_distance = pq_array.dist[curr_min_node_index] + edge.length
                    pq_array.decrease_key(new_distance, node_index)
                    prev_array[edge.dest.node_id] = curr_min_node_index

        # Need this call to return the shortest path to the GUI once we find it with Dijkstra's
        # self.getShortestPath(destIndex=srcIndex):

        t2 = time.time()
        return (t2 - t1)
