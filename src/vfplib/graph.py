'''
Created on Jun 6, 2014

@author: mschaffe
'''

import random
from collections import deque

class GraphNode(object):
    # immutable
    def __init__(self, value, edges=[]):
        self.value = value
        self.edgemap = {}
        for edge in edges:
            self.edgemap[edge] = None

    def add_edge(self, edge, target=None):
        self.edgemap[edge] = target

    def remove_edge(self, edge):
        del self.edgemap[edge]

    def set_edge_target(self, edge, target):
        if edge not in self.edgemap:
            raise KeyError(edge)
        self.edgemap[edge] = target

    def get_edge_target(self, edge):
        return self.edgemap[edge]

    def remove_edge_target(self, edge):
        if edge not in self.edgemap:
            raise KeyError(edge)
        self.edgemap[edge] = None

    def get_edges(self):
        for edge in self.edgemap:
            yield edge

    def get_explored_edges(self):
        for edge in self.edgemap:
            if self.edgemap[edge] != None:
                yield edge

    def get_unexplored_edges(self):
        for edge in self.edgemap:
            if self.edgemap[edge] == None:
                yield edge

    def __eq__(self, other):
        if isinstance(other, GraphNode):
            return self.value == other.value
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.value)

    def __str__(self):
        return 'GraphNode: ' + str(self.value)

class Graph():
    def __init__(self):
        self.nodemap = {}

    def add(self, item, edgevalues=[]):
        if item in self.nodemap:
            raise ValueError('Item already exists in graph: ' + str(item))
        self.nodemap[item] = GraphNode(item, edgevalues)

    def find(self, item):
        return self.nodemap[item].value

    def add_edge(self, source, edge, target=None):
        sourcenode = self.nodemap[source]
        if target:
            targetnode = self.nodemap[target]
            sourcenode.add_edge(edge, targetnode)
        else:
            sourcenode.add_edge(edge)

    def edges(self, source):
        sourcenode = self.nodemap[source]
        return sourcenode.get_edges()

    def explored_edges(self, source):
        sourcenode = self.nodemap[source]
        return sourcenode.get_explored_edges()

    def unexplored_edges(self, source):
        sourcenode = self.nodemap[source]
        return sourcenode.get_unexplored_edges()

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
                unexplorededgevalue = random.sample(unexplorededges, 1)[0]
                return currentpath + [unexplorededgevalue]
            else:
                explorededges = set(currentnode.get_explored_edges())
                for edge in explorededges:
                    targetnode = currentnode.get_edge_target(edge)
                    if targetnode not in touchednodes:
                        nodequeue.append((currentpath + [edge], targetnode))
                        touchednodes.add(targetnode)
        # if this point is reached, nothing is unexplored
        return None

    # returns a list of edges that is the shortest path from source to target,
    def shortest_path(self, source, target):
        marked = set()
        marked.add(source)
        queue = deque()  # each entry is (path-to-node, node)
        queue.append(([], source))
        while len(queue) > 0:
            currenttuple = queue.popleft()
            currentpath = currenttuple[0]
            current = currenttuple[1]
            if current == target:
                return currentpath
            edges = self.explored_edges(current)
            for edge in edges:
                intermediate = self.follow_edge(current, edge)
                if intermediate not in marked:
                    marked.add(intermediate)
                    queue.append((currentpath + [edge], intermediate))
        # if this point is reached, path does not exist
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
        for v in self.nodemap:
            yield v

    def __contains__(self, item):
        return self.nodemap.__contains__(item)

    def __missing__(self):
        raise NotImplementedError()

    def __str__(self):
        return 'Graph: ' + str(self.nodemap)







