'''
Created on Jun 6, 2014

@author: mschaffe
'''

class HashSet(object):

    def __init__(self, contents=[]):
        self.hashTable = {}
        for item in contents:
            self.hashTable[hash(item)] = item

    # silent clobber
    def add(self, item):
        self.hashTable[hash(item)] = item

    # throws keyerror when not found
    def remove(self, item):
        del self.hashTable[hash(item)]

    # throws keyerror when not found
    def find(self, item):
        return self.hashTable[hash(item)]

    def __len__(self):
        return self.hashTable.__len__()

    def __hash__(self):
        raise NotImplementedError()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return frozenset(self.hashTable.values()) == frozenset(other.hashTable.values())
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
        for key in self.hashTable:
            yield self.hashTable[key]

    def __contains__(self, item):
        return self.hashTable.values().__contains__(item)

    def __missing__(self):
        raise NotImplementedError()

    def __str__(self):
        return 'HashSet: ' + str(self.hashTable.values())

class FrozenHashSet(HashSet):

    def __init__(self, contents):
        super(FrozenHashSet, self).__init__(contents)

    def add(self, item):
        raise NotImplementedError()

    def remove(self, item):
        raise NotImplementedError()

    def __hash__(self):
        return hash(frozenset(self.hashTable.values()))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return frozenset(self.hashTable.values()) == frozenset(other.hashTable.values())
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return 'FrozenHashSet: ' + str(self.hashTable)


