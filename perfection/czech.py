#!/usr/bin/env python
"""
Use the Czech et al. method for generating minimal perfect hashes for strings.
"""

import random
import collections

import forest


__all__ = ['hash_info', 'create_hash', 'make_dict']


_info_fields = ('t1', 't2', 'g', 'indicies')
HashInfo = collections.namedtuple('HashInfo', _info_fields)


class CzechHashBuilder(object):
    """
    A helper class that groups all data needed to create a Czech hash.

    The entire hash algoritm occurs in  __init__.
    """

    def __init__(self, words, minimize=False):
        # Store the words as an immutable sequence.
        self.words = tuple(words)

        # TODO: Index minimization
        self.indicies = range(len(words[0]))

        # Each of the following steps add fields to `self`:

        # Mapping step:
        #  - n, t1, t2, f1, f2, graph
        self.generate_acyclic_graph()
        # Assignment step:
        #  - g
        self.assign()

        # Now hash_info will return the approriate object.

    @property
    def hash_info(self):
        """
        HashInfo tuple for the created hash.
        """
        return HashInfo(*(getattr(self, key) for key in _info_fields))

    # Algorithm steps.

    def generate_acyclic_graph(self):
        """
        Generates an acyclic graph for the given words.
        Returns graph, and a list of edge-word associations.
        """

        # Maximum length of each table, respectivly.
        # Hardcoded n = cm, where c = 3
        # There might be a good way to choose an appropriate C,
        # but [1] suggests the average amount of iterations needed
        # to generate an acyclic graph is sqrt(3).
        self.n = 3 * len(self.words)

        max_tries = len(self.words) ** 2
        for trial in xrange(max_tries):
            try:
                self.generate_or_fail()
            except forest.InvariantError:
                continue
            else:
                self.trials_taken = trial + 1
                break

    def generate_random_table(self):
        """
        Generates random tables for given word lists.
        """
        table = range(0, self.n)
        random.shuffle(table)
        return table

    def generate_or_fail(self):
        """
        Attempts to generate a random acylic graph, raising an
        InvariantError if unable to.
        """

        t1 = self.generate_random_table()
        t2 = self.generate_random_table()
        f1 = self.generate_func(t1)
        f2 = self.generate_func(t2)
        edges = [(f1(word), f2(word)) for word in self.words]

        # Try to generate that graph, mack!
        # Note that failure to generate the graph here should be caught
        # by the caller.
        graph = forest.ForestGraph(edges=edges)

        # Associate each edge with its corresponding word.
        associations = {}
        for num in xrange(len(self.words)):
            edge = edges[num]
            word = self.words[num]
            associations[graph.canonical_order(edge)] = (num, word)

        # Assign all of these to the object.
        for name in ('t1', 't2', 'f1', 'f2', 'graph', 'associations'):
            self.__dict__[name] = locals()[name]

    def generate_func(self, table):
        """
        Generates a random table based mini-hashing function.
        """

        # Ensure that `self` isn't suddenly in the closure...
        n = self.n

        def func(word):
            return sum(x * ord(c) for x, c in zip(table, word)) % n

        return func

    def assign(self):
        # Create an vector of empty assignments.
        self.g = [None] * (self.n + 1)

        # Assign all vertices.
        for vertex in self.graph.vertices:
            assert isinstance(vertex, int) and vertex <= self.n
            # This vertex has already been assigned.
            if self.g[vertex] is not None:
                continue

            self.g[vertex] = 0
            self.assign_vertex(vertex)


    def assign_vertex(self, vertex,):
        for neighbour in self.graph.neighbours(vertex):
            if self.g[neighbour] is not None:
                # This neighbour has already been assigned.
                continue

            # Get the associated edge number
            edge = self.graph.canonical_order((vertex, neighbour))
            num, _word = self.associations[edge]

            # Assign this vertex such that
            # h(word) == g(vertex) + g(neighbour)
            self.g[neighbour] = num - self.g[vertex]
            self.assign_vertex(neighbour)



def hash_parameters(words, minimize_indices=False):
    """
    Gives hash parameters for the given set of words.

    >>> info = hash_parameters('sun mon tue wed thu fri sat'.split())
    >>> len(info.t1)
    21
    >>> len(info.t2)
    21
    >>> len(info.g) # g values are 1-indexed...
    22
    """
    # Ensure that we have an indexable sequence.
    words = tuple(words)

    # Delegate to the hash builder.
    return CzechHashBuilder(words).hash_info



def do_example():
    import keyword
    words = keyword.kwlist

    hb = CzechHashBuilder(words)
    

    print '/*', hb.t1, hb.t2, hb.g, '*/'
    print hb.graph.to_dot(edge_labels={
        edge: '%d: %s' % assoc for edge, assoc in hb.associations.items()
    })

if __name__ == '__main__':
    do_example()
