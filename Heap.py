class Heap:
    def __init__(self, dist, nodes):
        self.heapList = [0]
        self.currentSize = 0
        for i in range(len(dist)):
            element = [dist[i], nodes[i]]
            self.heapList.append(element)
            self.heap(self.heapList)

    def perUp(self,i):
        while i // 2 > 0:
            if self.heapList[i][0] < self.heapList[i // 2][0]:
                tmp = self.heapList[i // 2]
                self.heapList[i // 2][0] = self.heapList[i][0]
                self.heapList[i][0] = tmp
            i = i // 2

    def insert(self, k):
        self.heapList.append(k)
        self.currentSize = self.currentSize + 1
        self.percUp(self.currentSize)

    def percDown(self, i):
        while (i * 2) <= self.currentSize:
            mc = self.minChild(i)
            if self.heapList[i][0] > self.heapList[mc][0]:
                tmp = self.heapList[i][0]
                self.heapList[i][0] = self.heapList[mc][0]
                self.heapList[mc][0] = tmp
            i = mc

    def minChild(self, i):
        if i * 2 + 1 > self.currentSize:
            return i * 2
        else:
            if self.heapList[i * 2][0] < self.heapList[i * 2 + 1][0]:
                return i * 2
            else:
                return i * 2 + 1

    def delMin(self):
        retval = self.heapList[1][0]
        self.heapList[1][0] = self.heapList[self.currentSize][0]
        self.currentSize = self.currentSize - 1
        self.heapList.pop()
        self.percDown(1)
        return retval

    def heap(self,list):
        i = len(list) // 2
        self.currentSize = len(list)
        self.heapList = [0] + list[:]
        while (i > 0):
            self.percDown(i)
            i = i - 1

    def makeQuene(self, dist, nodes):
        list = []
        for i in range(len(dist)):
            element = [dist[i], nodes[i]]
            list.append(element)
            self.heap(list)

    def decreaseKey(self, dist, node_id):
        for i in range (len(self.heapList)):
            if(self.heapList[i][1] == node_id):
                self.heapList[i][0] = dist
                return self.heapList