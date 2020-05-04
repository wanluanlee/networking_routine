#!/usr/bin/python3


from CS312Graph import *
import time
import numpy as np


class NetworkRoutingSolver:
    def __init__( self ):
        pass


    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network
        self.prev = []
        self.dist = []
        self.myQuene = []


    def getShortestPath( self, destIndex ):
        self.dest = destIndex

        # TODO: RETURN THE SHORTEST PATH FOR destIndex
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL
        #       NEED TO USE
        ifNull = False
        path = []
        path_edges = []
        total_length = 0
        currentNodeIndex = destIndex
        path.append(self.network.nodes[destIndex])
        while(ifNull != True):
            if (self.prev[currentNodeIndex] == None):
                break
            path.append(self.prev[currentNodeIndex])
            currentNodeIndex = self.prev[currentNodeIndex].node_id

        for i in range (0, len(path) - 1 ):
            distNode = path[i]
            sorceNode = path[i + 1]
            edge = distNode
            for i in range (len(sorceNode.neighbors)):
                if(distNode.node_id == sorceNode.neighbors[i].dest.node_id):
                    edge = sorceNode.neighbors[i]

            path_edges.append((sorceNode.loc, distNode.loc, '{:.0f}'.format(edge.length)))
            total_length += edge.length

        return {'cost':total_length, 'path':path_edges}

    def computeShortestPaths( self, srcIndex, use_heap=False):
        t1 = time.time()
        if(use_heap == False):
            self.findfindShortestPathArray(srcIndex)
        else:
            self.findShortestPathHeap(srcIndex)
        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index)


        t2 = time.time()
        return (t2-t1)

    def findfindShortestPathArray(self,srcNode):
        # heap
        for i in range(len(self.network.nodes)):
            self.dist.append(np.inf)

        for i in range(len(self.network.nodes)):
            self.prev.append(None)
        self.dist[srcNode] = 0

        array = self.unsorted_array()
        myQuene = array.makeQuene(self.dist, self.network.nodes)
        nodeNoNeed = []
        while (array.getLength() != 0):
            u = array.deleteMInArray()
            for i in range(len(u.neighbors)):
                if (self.dist[u.neighbors[i].dest.node_id] > self.dist[u.node_id] + u.neighbors[i].length):
                    self.dist[u.neighbors[i].dest.node_id] = self.dist[u.node_id] + u.neighbors[i].length
                    self.prev[u.neighbors[i].dest.node_id] = u
                    myQuene = array.decreaseKey(self.dist[u.neighbors[i].dest.node_id],
                                               u.neighbors[i].dest.node_id)

    def findShortestPathHeap(self, srcNode):

        self.dist = []
        self.prev = []
        for i in range (len(self.network.nodes)):
           self.dist.append(np.inf)
        #dist = np.fill(np.inf)

        for i in range (len(self.network.nodes)):
           self.prev.append(None)
        self.dist[srcNode] = 0
        Heap = self.Heap()
        discardNode = []
        myQuene = Heap.makeQuene(self.dist,self.network.nodes)
        #Time complexity O(v)
        while ((len(myQuene) - 1) != 0):
            u = Heap.delMin()
            discardNode.append(u)
            for i in range (len(u.neighbors)):
                if(self.dist[u.neighbors[i].dest.node_id] > self.dist[u.node_id] + u.neighbors[i].length):
                    self.dist[u.neighbors[i].dest.node_id] = self.dist[u.node_id] + u.neighbors[i].length
                    self.prev[u.neighbors[i].dest.node_id] = u
                    myQuene = Heap.decreaseKey(self.dist[u.neighbors[i].dest.node_id], u.neighbors[i].dest)

    class unsorted_array:
        def __init__(self):
            self.array = []
            self.length = len(self.array)
        # stored distance and nodes in a 2-D array
        # Time O(V)
        # Space O(V)
        def makeQuene(self, dist, nodes):
            for i in range(len(dist)):
                element = [dist[i], nodes[i]]
                self.array.append(element)
                self.length = len(self.array)
            return self.array

        # updated new distance two the corresponding node index
        # Time O(1)
        # Space O(V)
        def decreaseKey(self, newDist, node_id):
            self.array[node_id][0] = newDist
            return self.array

        # deleted the min distance in the array
        # Time O(V) because need to loop through the entire array
        # Space O(V)
        def deleteMInArray(self):
            min = self.array[0]
            for i in range(len(self.array)):
                if (min[0] > self.array[i][0]):
                    min = self.array[i]
            min[0] = 100000
            self.length = self.length-1
            return min[1]

        def getLength(self):
            return self.length

    class Heap:
        def __init__(self):
            self.heapList = [0]
            self.currentSize = 0
            self.dictionary = {}

        # move element up to the heap
        # Time O(log V)
        # Space O(V)
        def percUp(self, i):
            while i // 2 > 0:
                if self.heapList[i][0] < self.heapList[i // 2][0]:
                    preIndex = self.dictionary.get(self.heapList[i][1])
                    newIndex = self.dictionary.get(self.heapList[i // 2][1])
                    self.dictionary[self.heapList[i][1]] = newIndex
                    self.dictionary[self.heapList[i // 2][1]] = preIndex
                    tmp = self.heapList[i // 2]
                    self.heapList[i // 2] = self.heapList[i]
                    self.heapList[i] = tmp
                i = i // 2

         # Appended element to the heap and called perUp
         # Time O(1) because only need to call perUp
         # Space O(n)
        def insert(self, k):
            self.heapList.append(k)
            self.currentSize = self.currentSize + 1
            self.percUp(self.currentSize)

        # move element down to the heap
        # Time O(log V)
        # Space O(V)
        def percDown(self, i):
            while (i * 2) <= self.currentSize:
                mc = self.minChild(i)
                if self.heapList[i][0] > self.heapList[mc][0]:
                    tmp = self.heapList[i]
                    preIndex = self.dictionary.get(self.heapList[i][1])
                    newIndex = self.dictionary.get(self.heapList[mc][1])
                    self.dictionary[self.heapList[i][1]] = newIndex
                    self.dictionary[self.heapList[mc][1]] = preIndex
                    self.heapList[i] = self.heapList[mc]
                    self.heapList[mc] = tmp

                i = mc

        # find the smallest childern element
        # Time O(1)
        # Space O(V)
        def minChild(self, i):
            if i * 2 + 1 > self.currentSize:
                return i * 2
            else:
                if self.heapList[i * 2][0] < self.heapList[i * 2 + 1][0]:
                    return i * 2
                else:
                    return i * 2 + 1

        # delete the min element in heap and change the order of the heap
        # Time O(1) called percDown
        # Space O(V)
        def delMin(self):
            retval = self.heapList[1][1]
            #del self.dictionary[self.heapList[1][1]]
            self.heapList[1] = self.heapList[self.currentSize]
            self.dictionary[self.heapList[self.currentSize][1]] = 1
            self.currentSize = self.currentSize - 1
            self.heapList.pop()
            self.percDown(1)
            return retval

        def heap(self, list):
            i = len(list) // 2
            self.currentSize = len(list)
            self.heapList = [0] + list[:]
            while (i > 0):
                self.percDown(i)
                i = i - 1

        # make heap from a list
        # Time O(V)
        # Space O(V)
        def makeQuene(self, dist, nodes):
            list = []
            for i in range(len(dist)):
                element = [dist[i], nodes[i]]
                list.append(element)
                self.dictionary[nodes[i]] = i + 1
            self.heap(list)
            returnList = self.heapList
            return returnList

        # using a map to get index in the heap given node and decrease the distance
        # Time O(1)
        # Space O(V)
        def decreaseKey(self, dist, node):
            index = self.dictionary.get(node)
            self.heapList[index][0] = dist
            self.percUp(index)
            returnList = self.heapList
            return returnList





