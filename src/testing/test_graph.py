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
        pass

    def testGraphNodeEquality(self):
        pass

    def testGraphNodeHash(self):
        pass

    def testGraphNodeStr(self):
        pass

    def testGraphNodeAddEdge(self):
        pass

    def testGraphNodeRemoveEdge(self):
        pass

    def testGraphNodeSetEdgeTarget(self):
        pass

    def testGraphNodeGetEdgeTarget(self):
        pass

    def testGraphNodeRemoveEdgeTarget(self):
        pass

    def testGraphNodeGetEdges(self):
        pass

    def testGraphNodeGetExploredEdges(self):
        pass

    def testGraphNodeGetUnexploredEdges(self):
        pass

if __name__ == "__main__":
    unittest.main()
