#!/usr/bin/env python

"""
Includes the ForestGraph, which is pretty much just intended to be used to ...
do stuff.

"""

import itertools

__all__ = ['InvariantError', 'ForestGraph']

class InvariantError(ValueError):
    pass

class ForestGraph(object):
    """
    An acyclic graph comprising of one or more components.

    >>> graph = ForestGraph(edges=[(1, 2), (2, 3)])
    >>> graph += (3, 4)
    >>> graph += (4, 2)
    Traceback (most recent call last):
        ...
    InvariantError: Adding (4, 2) would form a cycle
    >>> graph += (5, 5)
    Traceback (most recent call last):
        ...
    InvariantError: Cannot add loop: (5, 5)
    >>> 4 in graph.vertices
    True
    >>> 5 in graph.vertices
    False
    >>> print graph.to_dot()
    graph {
        "1";
        "2";
        "3";
        "4";
    <BLANKLINE>
        "1" -- "2";
        "3" -- "4";
        "2" -- "3";
    }

    """

    def __init__(self, vertices=(), edges=()):
        self.vertices = set()
        self.edges = set()
        # Components is a dictionary of vertex -> to the set of all vertices
        # that comprise that component. Note that all vertex of the same
        # component share the exactly the SAME set instance!
        self.components = {}

        # Add all the original edges.
        self.vertices.update(vertices)
        for edge in edges:
            self.add_edge(edge)

    def __iadd__(self, edge):
        self.add_edge(edge)
        return self

    def add_edge(self, edge):
        """
        Add edge (u, v) to the graph. Raises InvariantError if adding the edge
        would form a cycle.
        """
        u, v = edge

        both_exist = u in self.vertices and v in self.vertices
        # Using `is` because if they belong to the same component, they MUST
        # share the same set object!
        if both_exist and self.components[u] is self.components[v]:
            # Both vertices are part of the same connected component.
            raise InvariantError('Adding %r would form a cycle' % (edge,))
        if u == v:
            raise InvariantError('Cannot add loop: %r' % (edge,))

        # Ensure the vertices exist in the graph.
        self.add_vertex(u)
        self.add_vertex(v)

        self.edges.add(self.canonical_order(edge))

        # Add all of the smaller components to the bigger one.
        smaller_component, bigger_component = self.sort_components(u, v)
        for vertex in smaller_component:
            bigger_component.add(vertex)
            # And with this assignment, say bye-bye to the smaller component.
            self.components[vertex] = bigger_component

    def sort_components(self, u, v):
        return sorted((self.components[u], self.components[v]), key=len)

    def add_vertex(self, vertex):
        if vertex not in self.vertices:
            self.vertices.add(vertex)
            self.components[vertex] = {vertex}

    def to_dot(self, *args, **kwargs):
        return graph_as_dot(self.vertices, self.edges, *args, **kwargs)

    @staticmethod
    def canonical_order(edge):
        u, v = edge
        return edge if u < v else (v, u)

    def __repr__(self):
        cls_name = type(self).__name__
        args = ', '.join(getattr(self, attr) for attr in ('vertices', 'edges'))
        return ''.join((cls_name, '(', args, ')'))



def graph_as_dot(vertex_set, edge_set, indentation=4):
    indent = ' ' * indentation

    def sanitize(vertex):
        return '"%s"' % str(vertex).replace('"', r'\"')

    def yield_lines():
        yield 'graph {'
        for vertex in vertex_set:
            yield indent + sanitize(vertex) + ';'

        yield ''

        for edge in edge_set:
            u, v = edge
            yield '%s%s -- %s;' % (indent, sanitize(u), sanitize(v))

        yield '}'

    return '\n'.join(yield_lines())

def print_example_graph():
    l = globals()
    for c in 'uvwxy':
        l[c] = c
    g = ForestGraph(edges=[(u, w), (w, x), (v,y)])
    print g.to_dot()


if __name__ == '__main__':
    import sys

    if '-g' in sys.argv:
        print_example_graph()
    else:
        # Test the module.
        import doctest
        exit(doctest.testmod(verbose=False).failed)
