'''
Created on Jul 2, 2014

@author: mschaffe
'''
import unittest

from vfplib.graph import Graph, GraphNode

class Test(unittest.TestCase):

    def assertEqualityContract(self, a, b, expected, message=None):
        if message == None:
            message = str(a) + ' and ' + str(b)
        self.assertEqual(a == b, expected, 'Equality contract broken for: ' + message)
        self.assertEqual(b == a, expected, 'Equality contract broken for: ' + message)
        self.assertEqual(a != b, not expected, 'Equality contract broken for: ' + message)
        self.assertEqual(b != a, not expected, 'Equality contract broken for: ' + message)

    def assertHashContract(self, a, b, message=None):
        if message == None:
            message = str(a) + ' and ' + str(b)
        if a == b:
            self.assertEqual(hash(a), hash(b), 'Hash contract broken for: ' + message)
        else:
            self.assertNotEqual(hash(a), hash(b), 'Hash contract quasi-broken for: ' + message)

    def testGraphNodeInit(self):
        a = GraphNode('a')
        a2 = GraphNode('a', [])
        a3 = GraphNode('a', '')
        b = GraphNode('b', ['edge1'])
        c = GraphNode('c', ['edge1', 'edge2', 'edge3'])
        d = GraphNode('d', 'abcde')
        # exceptions
        try:
            _ = GraphNode('invalid edges', 1)
            self.assertTrue(False, 'GraphNode.__init__: Failed to throw TypeError exception on non-iterable edges')
        except TypeError, e:
            if str(e) != "'int' object is not iterable":
                raise
        try:
            _ = GraphNode('invalid edges', [set()])
            self.assertTrue(False, 'Screen.__init__: Failed to throw TypeError exception on unhashable edges')
        except TypeError, e:
            if str(e) != "unhashable type: 'set'":
                raise
        # attributes
        self.assertEqual(a.value, 'a', 'GraphNode.__init__: Problem setting value')
        self.assertEqual(a2.value, 'a', 'GraphNode.__init__: Problem setting value')
        self.assertEqual(a2.edgemap, {}, 'GraphNode.__init__: Problem setting empty edgemap')
        self.assertEqual(a3.edgemap, {}, 'GraphNode.__init__: Problem setting empty edgemap')
        self.assertEqual(b.edgemap, {'edge1': None}, 'GraphNode.__init__: Problem setting single edgemap')
        self.assertEqual(c.edgemap, {'edge1': None,
                                     'edge2': None,
                                     'edge3': None}, 'GraphNode.__init__: Problem setting multiple edgemap')
        self.assertEqual(d.edgemap, {'a': None,
                                     'b': None,
                                     'c': None,
                                     'd': None,
                                     'e': None}, 'GraphNode.__init__: Problem setting multiple edgemap')

    def testGraphNodeEquality(self):
        a = GraphNode('a')
        a2 = GraphNode('a')
        a3 = GraphNode('a', [])
        a4 = GraphNode('a', [1, 2, 3])
        b = GraphNode('b')
        other = 'GraphNode: a'
        class DummySubGraphNode(GraphNode):
            pass
        asub = DummySubGraphNode('a')
        self.assertEqualityContract(a, a, True, 'same GraphNode object')
        self.assertEqualityContract(a, a2, True, 'identical GraphNode object')
        self.assertEqualityContract(a, a3, True, 'same value, different constructor')
        self.assertEqualityContract(a, a4, True, 'same value, different edgemap')
        self.assertEqualityContract(a, b, False, 'different value')
        self.assertEqualityContract(a, other, False, 'non-GraphNode objects')
        self.assertEqualityContract(a, asub, True, 'subclasses')

    def testGraphNodeHash(self):
        a = GraphNode('a')
        a2 = GraphNode('a')
        a3 = GraphNode('a', [])
        a4 = GraphNode('a', [1, 2, 3])
        b = GraphNode('b')
        other = 'GraphNode: a'
        class DummySubGraphNode(GraphNode):
            pass
        asub = DummySubGraphNode('a')
        unhashable = GraphNode(set())
        try:
            hash(unhashable)
            self.assertTrue(False, 'Screen.__hash__: Failed to throw TypeError exception on unhashable value')
        except TypeError, e:
            if str(e) != "unhashable type: 'set'":
                raise
        self.assertHashContract(a, a, 'same GraphNode object')
        self.assertHashContract(a, a2, 'identical GraphNode object')
        self.assertHashContract(a, a3, 'same value, different constructor')
        self.assertHashContract(a, a4, 'same value, different edgemap')
        self.assertHashContract(a, b, 'different value')
        self.assertHashContract(a, other, 'non-GraphNode objects')
        self.assertHashContract(a, asub, 'subclasses')

    def testGraphNodeStr(self):
        a = GraphNode('name', [1, 2, 3])
        self.assertEquals(str(a), 'GraphNode: name', 'GraphNode.__str__ is incorrect')

    def testGraphNodeAddEdge(self):
        pass  # unimplemented test

    def testGraphNodeRemoveEdge(self):
        pass  # unimplemented test

    def testGraphNodeSetEdgeTarget(self):
        pass  # unimplemented test

    def testGraphNodeGetEdgeTarget(self):
        pass  # unimplemented test

    def testGraphNodeRemoveEdgeTarget(self):
        pass  # unimplemented test

    def testGraphNodeGetEdges(self):
        pass  # unimplemented test

    def testGraphNodeGetExploredEdges(self):
        pass  # unimplemented test

    def testGraphNodeGetUnexploredEdges(self):
        pass  # unimplemented test

    def testGraphInit(self):
        pass  # unimplemented test

    def testGraphEquality(self):
        pass  # unimplemented test

    def testGraphLen(self):
        pass  # unimplemented test

    def testGraphGetItem(self):
        pass  # unimplemented test

    def testGraphSetItem(self):
        pass  # unimplemented test

    def testGraphDelItem(self):
        pass  # unimplemented test

    def testGraphIter(self):
        pass  # unimplemented test

    def testGraphContains(self):
        pass  # unimplemented test

    def testGraphMissing(self):
        pass  # unimplemented test

    def testGraphStr(self):
        pass  # unimplemented test

if __name__ == "__main__":
    unittest.main()
