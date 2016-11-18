#!/usr/bin/env python
"""
Includes the ForestGraph, which is pretty much just intended to be used to ...
do stuff.
"""

from __future__ import print_function

import collections

__all__ = ['InvariantError', 'ForestGraph']


class InvariantError(ValueError):
    pass


class ForestGraph(object):
    """
    An acyclic graph comprising of one or more components.

    >>> graph = ForestGraph(edges=[(1, 2), (2, 3)])
    >>> graph += (3, 4)
    >>> 4 in graph.vertices
    True
    >>> 5 in graph.vertices
    False
    >>> print(graph.to_dot())
    graph {
        "1" -- "2";
        "2" -- "3";
        "3" -- "4";
    }
    >>> set(graph.neighbours(2)) == {1, 3}
    True
    >>> set(graph.neighbours(1)) == {2}
    True
    >>> set(graph.neighbours(3)) == {2, 4}
    True
    """

    def __init__(self, vertices=(), edges=()):
        # Each vertex is associated with a list of its neighbouring vertices.
        self._vertices = collections.defaultdict(set)

        # Each edge *may* be associated with an arbitrary value.
        self._edges = {}

        # Components is a dictionary of vertex -> to the set of all vertices
        # that comprise that component. Note that all vertex of the same
        # component share the exactly the SAME set instance!
        self.components = {}

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

        # Add the edges to each other.
        self._vertices[u].add(v)
        self._vertices[v].add(u)

        # Add all of the smaller components to the bigger one.
        smaller_component, bigger_component = self.sort_components(u, v)
        for vertex in smaller_component:
            bigger_component.add(vertex)
            # And with this assignment, say bye-bye to the smaller component.
            self.components[vertex] = bigger_component

    def sort_components(self, u, v):
        return sorted((self.components[u], self.components[v]), key=len)

    def add_vertex(self, vertex):
        # Make a new component for the vertex, if the vertex doesn't exist
        # yet.
        self.components.setdefault(vertex, {vertex})

    def to_dot(self, *args, **kwargs):
        return graph_as_dot(self.edges, *args, **kwargs)

    @property
    def edges(self):
        """
        Edges of this graph, in canonical order.
        """
        canonical_edges = set()
        for v1, neighbours in self._vertices.items():
            for v2 in neighbours:
                edge = self.canonical_order((v1, v2))
                canonical_edges.add(edge)
        return canonical_edges

    @property
    def vertices(self):
        """Set of all vertices in the graph."""
        return self._vertices.keys()

    def neighbours(self, vertex):
        """
        Yields all neighbours of the given vertex, in no particular
        order.
        """
        return self._vertices[vertex]

    @staticmethod
    def canonical_order(edge):
        u, v = edge
        return edge if u < v else (v, u)

    def __repr__(self):
        cls_name = type(self).__name__
        args = ', '.join(getattr(self, attr) for attr in ('vertices', 'edges'))
        return ''.join((cls_name, '(', args, ')'))


def graph_as_dot(edge_set, edge_labels=None, indentation=4):
    if not edge_labels:
        edge_labels = {}

    indent = ' ' * indentation
    edge_tmpl = indent + '"{u}" -- "{v}"{label};'

    def sanitize(vertex):
        return '"%s"' % str(vertex).replace('"', r'\"')

    def make_label(edge):
        if edge not in edge_labels:
            return ""

        text = edge_labels[edge]
        return "[label=%s]" % sanitize(text)

    def yield_lines():
        yield 'graph {'

        for edge in sorted(edge_set):
            u, v = edge
            label = make_label(edge)
            yield edge_tmpl.format(**vars())

        yield '}'

    return '\n'.join(yield_lines())


def print_example_graph():
    l = globals()
    for c in 'uvwxy':
        l[c] = c
    g = ForestGraph(edges=[(u, w), (w, x), (v,y)])
    print(g.to_dot())

if __name__ == '__main__':
    import sys

    if '-g' in sys.argv:
        print_example_graph()
    else:
        # Test the module.
        import doctest
        exit(doctest.testmod(verbose=False).failed)
