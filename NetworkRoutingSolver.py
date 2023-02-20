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

        # We only need to compare the nodes in the queue
        ''' Worst case O(logV) if we had to test every node '''
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
        # -1 is the value we give for nodes that aren't in the queue
        self.q_pointer = [-1] * len(nodes)

    def insert(self, node_index):

        if self.queue is None:
            self.queue = []
            self.queue.append(node_index)
            self.q_pointer[node_index] = 0

        else:
            # Insert the index at the end of the heap
            new_index = len(self.queue)
            self.queue.append(node_index)
            self.q_pointer[node_index] = new_index

            # This index points to where a node is on the heap, not it's value
            child_index = new_index

            ''' O(logV) '''
            self.bubble_up(child_index)

        return

    def decrease_key(self, dist, node_index):
        self.dist[node_index] = dist

        child_index = self.q_pointer[node_index]

        # Adjust the heap based off the node's new value
        ''' O(logV) '''
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

    def delete_min(self):
        # Min is always the first value in the heap
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
        ''' This is where the O(logV) comes for insert '''
        while True:
            left_child_index = (parent_index * 2) + 1
            right_child_index = (parent_index * 2) + 2

            # If no left child is present, then we're done
            if len(self.queue) <= left_child_index:
                return min_index

            # Check parent against left child
            if self.dist[self.queue[parent_index]] > self.dist[self.queue[left_child_index]]:

                right_child_present = len(self.queue) > right_child_index

                # check if right child is present, and if it is, if it's greater than the left child
                if right_child_present:
                    if self.dist[self.queue[left_child_index]] > self.dist[self.queue[right_child_index]]:
                        self.q_pointer[self.queue[right_child_index]] = parent_index
                        self.q_pointer[self.queue[parent_index]] = right_child_index

                        self.queue[right_child_index], self.queue[parent_index] = \
                            self.queue[parent_index], self.queue[right_child_index]
                        parent_index = right_child_index
                        continue

                # We only get here if either of the above if statements fail – if both are true, we don't
                #   actually hit this because we continue through to the start of the while loop
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

        path_edges = []
        total_length = 0
        curr_node_index = destIndex

        ''' Worst case O(V), if you had to go through every node for the shortest path '''
        while True:

            # Is this the only check we need, or do we need the lower two as well?
            if self.prev_array[curr_node_index] is None:
                return {'cost': math.inf, 'path': []}

            # Find the previous node
            prev_node = self.network.nodes[self.prev_array[curr_node_index]]
            if prev_node.neighbors is None:
                return {'cost': math.inf, 'path': []}

            # Find the edge from previous node to current node
            edge = None
            ''' O(1) since neighbors is limited to 3 '''
            for neighbor in prev_node.neighbors:
                if neighbor.dest.node_id == curr_node_index:
                    edge = neighbor
                    break

            if edge is None:
                return {'cost': math.inf, 'path': []}

            # Note: this returns a QT edge, not a 312GraphEdge -- that's what the GUI needs
            path_edges.append((edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)))

            total_length += edge.length

            # Set curr node to previous node
            curr_node_index = prev_node.node_id
            if edge.src.node_id == self.source:
                break

        return {'cost': total_length, 'path': path_edges}

    def computeShortestPaths(self, srcIndex, use_heap=False):
        self.source = srcIndex
        t1 = time.time()

        if use_heap:
            pq = HeapArray.__new__(HeapArray)
        else:
            pq = PQArray.__new__(PQArray)

        ''' 
            This is my "makequeue" function, I just do it inside the constructor
            This is O(V) for both because we have to add each node to the distance array    
        '''
        pq.__init__(self.network.nodes)
        self.prev_array = [None] * len(self.network.nodes)

        # Start with the source node
        pq.insert(srcIndex)
        pq.decrease_key(0, srcIndex)

        while pq.queue:
            # Get the lowest distance node
            ''' O(V) for array, O(logV) for heap '''
            curr_min_node_index = pq.delete_min()
            curr_node = self.network.nodes[curr_min_node_index]

            # Check each edge from the lowest distance node
            ''' O(1) since we limit neighbor edges to a maximum of 3 '''
            for edge in curr_node.neighbors:

                # If the distance is lower, insert that node to the pq (no worries about duplicates, since it's a set),
                #   change the distance, and change the node's prev value
                ''' O(1) for array, O(logV) for heap '''
                if pq.dist[edge.dest.node_id] > pq.dist[curr_min_node_index] + edge.length:
                    node_index = edge.dest.node_id
                    new_distance = pq.dist[curr_min_node_index] + edge.length
                    pq.insert(node_index)
                    pq.decrease_key(new_distance, node_index)
                    self.prev_array[edge.dest.node_id] = curr_min_node_index

        t2 = time.time()
        return t2 - t1
