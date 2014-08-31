#!/usr/bin/env python
"""
Use the Czech et al. method for generating minimal perfect hashes for strings. 
"""

import random
import collections

import forest



HashInfo = collections.namedtuple('HashInfo', 't1 t2 g indices')


def hash_parameters(words, minimize_indices=False):
    """
    Gives hash parameters for the given set of words.

    >>> info = hash_parameters('sun mon tue wed thu fri sat'.split())
    >>> len(info.t1)
    3
    >>> len(info.t2)
    3
    >>> len(info.g)
    21
    """
    # Ensure that we have an indexable sequence.
    words = tuple(words)

    # generate acyclic graph should... generate the tables...
    graph, associations = generate_acyclic_graph(words)
    g = assign(graph, associations)

    return HashInfo(t1=(), t2=(), g=g, indices=None)


def create_hash(words):
    return


def generate_random_table(words, n):
    """
    Generates random tables for given word lists.
    """
    table = range(0, n)
    random.shuffle(table)
    return table


def generate_func(words, n):
    """
    Generates a random table based mini-hashing function.
    """
    table = generate_random_table(words, n)

    def func(word):
        return sum(x * ord(c) for x, c in zip(table, word)) % n

    func.table = table
    return func


def generate_or_fail(words):
    # TODO: Return the tables! 
    # TODO: get the association step out of here!

    # Hardcoded n = cm, where c = 3
    # There might be a good way to choose an appropriate C,
    # but [1] suggests the average amount of iterations needed
    # to generate an acyclic graph is sqrt(3).
    n = 3 * len(words)
    f1 = generate_func(words, n)
    f2 = generate_func(words, n)

    edges = [(f1(word), f2(word)) for word in words]

    # Try to generate that graph, mack!
    try:
        graph = forest.ForestGraph(edges=edges)
    except forest.InvariantError:
        return None

    # Associate each edge with its corresponding word.
    associations = {}
    for num in xrange(len(words)):
        edge = edges[num]
        word = words[num]
        associations[graph.canonical_order(edge)] = (num, word)

    return graph, associations

def generate_acyclic_graph(words):
    """
    Generates an acyclic graph for the given words.
    Returns graph, and a list of edge-word associations.
    """

    max_tries = len(words) ** 2

    for trial in xrange(max_tries):
        value = generate_or_fail(words)
        if value is None:
            continue
        return value

def assign(graph, associations):
    # TODO: pass n to this as an argument
    n = max(graph.vertices)

    # Create an vector of empty assignments.
    g = [None] * (n + 1)

    # Assign all vertices.
    for vertex in graph.vertices:
        assert isinstance(vertex, int) and vertex <= n
        # This vertex has already been assigned.
        if g[vertex] is not None:
            continue

        g[vertex] = 0
        assign_vertex(vertex, graph, associations, g)

    return g

def assign_vertex(vertex, graph, associations, g):
    for neighbour in graph.neighbours(vertex):
        if g[neighbour] is not None:
            # This neighbour has already been assigned.
            continue

        # Get the associated edge number
        edge = graph.canonical_order((vertex, neighbour))
        num, _word = associations[edge]

        # Assign this vertex such that
        # h(word) == g(vertex) + g(neighbour)
        g[neighbour] = num - g[vertex]
        assign_vertex(neighbour, graph, associations, g)


def do_example():
    import keyword
    words = keyword.kwlist

    graph, associations = generate_acyclic_graph(words)
    print
    print graph.to_dot(edge_labels={
        edge: '%d: %s' % assoc for edge, assoc in associations.items()
    })
    
if __name__ == '__main__':
    do_example()
