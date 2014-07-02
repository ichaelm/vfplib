'''
Created on Jun 6, 2014

@author: mschaffe
'''

from .hashset import HashSet
import random
from collections import deque

class GraphEdge(object):
    def __init__(self, value, target=None):
        self.value = value
        if target == None:
            self.explored = False
        else:
            assert isinstance(target, GraphNode)
            self.explored = True
            self.target = target

    def set_target(self, target):
        assert isinstance(target, GraphNode)
        self.explored = True
        self.target = target

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return 'GraphEdge: ' + str(self.value)

class GraphNode(object):
    # immutable
    def __init__(self, value, edgevalues=None):
        self.value = value
        self.edges = HashSet()
        if not edgevalues == None:
            for edgevalue in edgevalues:
                edge = GraphEdge(edgevalue)
                self.edges.add(edge)

    def set_edge_target(self, edgevalue, target):
        assert isinstance(target, GraphNode)
        self.edges.find(GraphEdge(edgevalue)).set_target(target)

    def get_edges(self):
        for edge in self.edges:
            yield edge

    def get_explored_edges(self):
        for edge in self.edges:
            if edge.explored:
                yield edge

    def get_unexplored_edges(self):
        for edge in self.edges:
            if not edge.explored:
                yield edge

    def get_edge_target(self, edgevalue):
        return self.edges.find(GraphEdge(edgevalue)).target

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.value == other.value
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return 'GraphNode: ' + str(self.value)

class Graph():
    def __init__(self):
        self.hashmap = HashSet()

    def add(self, item, edgevalues=None):
        if GraphNode(item) not in self.hashmap:
            self.hashmap.add(GraphNode(item, edgevalues))

    def remove(self, item):
        self.hashmap.remove(GraphNode(item))

    def find(self, item):
        return self.hashmap.find(GraphNode(item)).value

    def add_edge(self, source, key, target):
        sourcenode = self.hashmap.find(GraphNode(source))
        targetnode = self.hashmap.find(GraphNode(target))
        sourcenode.set_edge_target(key, targetnode)

    def edges(self, source):
        sourcenode = self.hashmap.find(GraphNode(source))
        for edge in sourcenode.get_edges():
            yield edge.value

    def explored_edges(self, source):
        sourcenode = self.hashmap.find(GraphNode(source))
        for edge in sourcenode.get_explored_edges():
            yield edge.value

    def unexplored_edges(self, source):
        sourcenode = self.hashmap.find(GraphNode(source))
        for edge in sourcenode.get_unexplored_edges():
            yield edge.value

    def follow_edge(self, source, key):
        sourcenode = self.hashmap.find(GraphNode(source))
        return sourcenode.get_edge_target(key).value

    def nearest_unexplored_edge(self, source):
        nodequeue = deque([])
        touchednodes = HashSet()
        sourcenode = self.hashmap.find(GraphNode(source))
        nodequeue.append(([], sourcenode))
        touchednodes.add(sourcenode)
        while len(nodequeue) > 0:
            currentlocation = nodequeue.popleft()
            currentnode = currentlocation[1]
            currentpath = currentlocation[0]
            unexplorededges = set(currentnode.get_unexplored_edges())
            if len(unexplorededges) > 0:
                unexplorededgevalue = random.sample(unexplorededges, 1)[0].value
                return currentpath + [unexplorededgevalue]
            else:
                explorededges = set(currentnode.get_explored_edges())
                for edge in explorededges:
                    targetnode = edge.target
                    if targetnode not in touchednodes:
                        nodequeue.append((currentpath + [edge.value], targetnode))
                        touchednodes.add(targetnode)
        # if this point is reached, nothing is unexplored
        return None

    def __len__(self):
        return self.hashmap.__len__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.hashmap == other.hashmap
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getitem__(self, key):
        raise NotImplementedError()

    def __setitem__(self, key, value):
        raise NotImplementedError()

    def __delitem__(self, key):
        raise NotImplementedError()

    def __iter__(self):
        for v in self.hashmap:
            yield v.value

    def __contains__(self, item):
        return self.hashmap.__contains__(item)

    def __missing__(self):
        raise NotImplementedError()

    def __str__(self):
        return 'Graph: ' + str(self.hashmap.hashTable)







