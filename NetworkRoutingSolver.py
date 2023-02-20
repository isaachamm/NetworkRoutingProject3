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
        self.queue = set()

    def insert(self, node_index):
        self.queue.add(node_index)
        return

    def decrease_key(self, dist, node_index):
        self.dist[node_index] = dist
        return

    def delete_min(self):

        # Note: minimum is the index of the lowest node, not it's value
        minimum = None

        for node in self.queue:

            if minimum is None:
                minimum = node

            # If in pq, compare the new node's value to the current minimum value. If lower, make curr
            #   index the new minimum
            if self.dist[node] < self.dist[minimum]:
                minimum = node

        temp = minimum
        self.queue.remove(minimum)

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
        self.queue = None
        self.q_pointer = [-1] * len(nodes)

    def insert(self, node_index):
        if self.queue is None:
            self.queue = []
            self.queue.append(node_index)
            self.q_pointer[node_index] = 0
        else:
            new_index = len(self.queue)
            self.queue.append(node_index)
            self.q_pointer[node_index] = new_index

            # These indexes point to where a node is on the heap
            child_index = new_index

            self.bubble_up(child_index)

        return

    def bubble_up(self, child_index):

        parent_index = (child_index - 1) // 2

        while True:
            if self.dist[self.queue[child_index]] > self.dist[self.queue[parent_index]]:

                # Switch where the pointer array points to them
                self.q_pointer[self.queue[child_index]] = parent_index
                self.q_pointer[self.queue[parent_index]] = child_index

                # Then switch where they are in the heap
                self.queue[child_index], self.queue[parent_index] = \
                    self.queue[parent_index], self.queue[child_index]
                child_index = parent_index
                parent_index = (child_index - 1) // 2
            else:
                break

    def decrease_key(self, dist, node_index):
        self.dist[node_index] = dist

        child_index = self.q_pointer[node_index]

        self.bubble_up(child_index)

        return

    def delete_min(self):
        min_index = self.queue[0]

        if len(self.queue) == 1:
            self.queue.pop()
            return min_index

        # Move the last element in the heap to the top, then delete it
        last_index = len(self.queue) - 1
        self.queue[0] = self.queue[last_index]
        self.queue.pop(last_index)

        parent_index = 0

        # Percolate that number down
        while True:
            left_child_index = (parent_index * 2) + 1
            right_child_index = (parent_index * 2) + 2
            if len(self.queue) <= left_child_index:
                return min_index

            if self.dist[self.queue[parent_index]] > self.dist[self.queue[left_child_index]]:

                if len(self.queue) <= right_child_index:
                    return min_index

                if self.dist[self.queue[left_child_index]] > self.dist[self.queue[right_child_index]] and \
                        len(self.queue) > right_child_index:
                    self.q_pointer[self.queue[right_child_index]] = parent_index
                    self.q_pointer[self.queue[parent_index]] = right_child_index

                    self.queue[right_child_index], self.queue[parent_index] = \
                        self.queue[parent_index], self.queue[right_child_index]
                    parent_index = right_child_index
                else:
                    self.q_pointer[self.queue[left_child_index]] = parent_index
                    self.q_pointer[self.queue[parent_index]] = left_child_index

                    self.queue[left_child_index], self.queue[parent_index] = \
                        self.queue[parent_index], self.queue[left_child_index]
                    parent_index = left_child_index
            else:
                break

        return min_index


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


        if use_heap:
            pq = HeapArray.__new__(HeapArray)
        else:
            pq = PQArray.__new__(PQArray)

        pq.__init__(self.network.nodes)
        self.prev_array = [None] * len(self.network.nodes)
        pq.insert(srcIndex)
        pq.decrease_key(0, srcIndex)
        while pq.queue:
            curr_min_node_index = pq.delete_min()
            curr_node = self.network.nodes[curr_min_node_index]
            for edge in curr_node.neighbors:
                if (pq.dist[edge.dest.node_id] >
                        pq.dist[curr_min_node_index] + edge.length):
                    node_index = edge.dest.node_id
                    new_distance = pq.dist[curr_min_node_index] + edge.length
                    pq.insert(node_index)
                    pq.decrease_key(new_distance, node_index)
                    self.prev_array[edge.dest.node_id] = curr_min_node_index

        t2 = time.time()
        return t2 - t1
