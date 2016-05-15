from kd import generate_tree_class
from math import pow
from random import random

class ExampleNode(object):
    def __init__(self):
        self.data = [random(), random(), random(), random(), random()]
        # print('ExampleNode __init__ %d' % (len(self.data)))

    def at_depth(self, depth):
        return self.data[depth % len(self.data)]

    def distance(self, other):
        distance_squared = 0.0
        for ii in range(0, len(self.data)):
            distance_squared += pow(self.data[ii] - other.data[ii], 2)
        return distance_squared

ExampleNode = generate_tree_class(ExampleNode)

tree = ExampleNode()
node1 = ExampleNode()
node2 = ExampleNode()

tree.kd_add_node(node1)
tree.kd_add_node(node2)
