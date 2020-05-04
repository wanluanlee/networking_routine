class unsorted_array:
  def __init__(self, dist, nodes):
      self.array = [0]
      for i in range(len(self.dist)):
          element = [self.dist[i], self.network.nodes[i]]
          self.array.append(element)

  def decreaseKey(self, newDist, node_id):

      for i in range(len(self.array)):
          if (self.array[i][1].node_id == node_id):
              self.array[i][0] = newDist
      return self.array

  def deleteMInArray(self):
      min =  self.array[0]
      for i in range(len(self.array)):
          if (min[0] >  self.array[i][0]):
              min =  self.array[i]
      self.array.remove(min)
      return min[1]



