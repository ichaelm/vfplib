'''
Created on Jun 6, 2014

@author: mschaffe
'''

import random
from collections import deque

class GraphEdge(object):
    def __init__(self, value, target=None):
        self.value = value
        self.target = target

    def is_explored(self):
        return self.target != None

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        if isinstance(other, GraphEdge):
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
        self.edgemap = {}
        if not edgevalues == None:
            for edgevalue in edgevalues:
                edge = GraphEdge(edgevalue)
                self.edgemap[edgevalue] = edge

    def set_edge_target(self, edgevalue, target):
        assert isinstance(target, GraphNode)
        self.edgemap[edgevalue].target = target

    def get_edges(self):
        for edge in self.edgemap.values():
            yield edge

    def get_explored_edges(self):
        for edge in self.edgemap.values():
            if edge.is_explored():
                yield edge

    def get_unexplored_edges(self):
        for edge in self.edgemap.values():
            if not edge.is_explored():
                yield edge

    def get_edge_target(self, edgevalue):
        return self.edgemap[edgevalue].target

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        if isinstance(other, GraphNode):
            return self.value == other.value
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return 'GraphNode: ' + str(self.value)

class Graph():
    def __init__(self):
        self.nodemap = {}

    def add(self, item, edgevalues=None):
        if item not in self.nodemap:
            self.nodemap[item] = GraphNode(item, edgevalues)

    def remove(self, item):
        del self.nodemap[item]

    def find(self, item):
        return self.nodemap[item].value

    def add_edge(self, source, key, target):
        sourcenode = self.nodemap[source]
        targetnode = self.nodemap[target]
        sourcenode.set_edge_target(key, targetnode)

    def edges(self, source):
        sourcenode = self.nodemap[source]
        for edge in sourcenode.get_edges():
            yield edge.value

    def explored_edges(self, source):
        sourcenode = self.nodemap[source]
        for edge in sourcenode.get_explored_edges():
            yield edge.value

    def unexplored_edges(self, source):
        sourcenode = self.nodemap[source]
        for edge in sourcenode.get_unexplored_edges():
            yield edge.value

    def follow_edge(self, source, key):
        sourcenode = self.nodemap[source]
        return sourcenode.get_edge_target(key).value

    def nearest_unexplored_edge(self, source):
        nodequeue = deque([])
        touchednodes = set()
        sourcenode = self.nodemap[source]
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
        return self.nodemap.__len__()

    def __eq__(self, other):
        if isinstance(other, Graph):
            return self.nodemap == other.nodemap
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
        for v in self.nodemap.values():
            yield v.value

    def __contains__(self, item):
        return self.nodemap.values().__contains__(item)

    def __missing__(self):
        raise NotImplementedError()

    def __str__(self):
        return 'Graph: ' + str(self.nodemap.values())







