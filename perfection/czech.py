#!/usr/bin/env python
"""
Use the Czech et al. method for generating minimal perfect hashes for strings. 
"""

import random
import forest

def generate_random_table(words):
    """
    Generates random tables.
    """
    #r = lambda: random.randint(0, table_size -1)
    #table_size = len(max(words, key=len))
    feature_size = sum(len(w) for w in words)
    #table = range(0, table_size)
    table = range(0, feature_size)
    random.shuffle(table)
    return table
    #return tuple(tuple(r() for _ in xrange(len(word))) for word in words)
    #return tuple(r() for _ in xrange(table_size))


def generate_func(words):
    table = generate_random_table(words)
    #print table
    max_length = len(max(words, key=len))
    feature_size = sum(len(w) for w in words)
    assert len(table) >= max_length
    def func(word):
        return sum(x * ord(c) for x, c in zip(table, word)) % feature_size
    return func

def generate_and_try(words):
    from operator import itemgetter
    f1 = generate_func(words)
    f2 = generate_func(words)
    pairs = [((f1(word), f2(word)), word) for word in words]
    edges = map(itemgetter(0), pairs)
    try:
        graph = forest.ForestGraph(edges=edges)
    except forest.InvariantError:
        return None
    return graph, pairs


if __name__ == '__main__':
    words = ('program type const var procedure function '
             'enum record array of '
             'while for do goto '
             'begin end').split()

    initial_message = "Generating trial: "
    print initial_message,

    max_tries = len(words) ** 2
    for trial in xrange(max_tries):
        print "\033[%dG\033[k" % len(initial_message),
        print "\033[1m%d\033[m" % trial,
        value = generate_and_try(words)
        if value is None:
            continue
        graph, pairs = value   
        break

    print
    print pairs
    print graph.to_dot()
    

