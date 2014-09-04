#!/usr/bin/env python

"""
Shared utilities for perfect hash tools.
"""

import collections


def create_dict_subclass(name, hash_func, slots, doc):
    """
    Creates a dict subclass named name, using the hash_function to index
    hash_length items. Doc should be any additional documentation added to the
    class.
    """

    hash_length = len(slots)

    # Returns array index -- raises a KeyError if the key does not match
    # its slot value.
    def index_or_key_error(key):
        index = hash_func(key)
        # Make sure the key is **exactly** the same.
        if key != slots[index]:
            raise KeyError(key)
        return index

    def init(self, *args, **kwargs):
        self._arr = [None] * hash_length
        self._len = 0

        # Delegate initialization to update provided by MutableMapping:
        self.update(*args, **kwargs)

    def getitem(self, key):
        index = index_or_key_error(key)
        if self._arr[index] is None:
            raise KeyError(key)
        return self._arr[index][1]

    def setitem(self, key, value):
        index = index_or_key_error(key)
        self._arr[index] = (key, value)

    def delitem(self, key):
        index = index_or_key_error(key)
        if self._arr[index] is None:
            raise KeyError(key)
        self._arr[index] = None

    def dict_iter(self):
        return (pair[0] for pair in self._arr if pair is not None)

    def dict_len(self):
        # TODO: Make this O(1) using auxiliary state?
        return sum(1 for _ in self)

    def dict_repr(self):
        arr_repr = (repr(pair) for pair in self._arr if pair is not None)
        return ''.join((name, '([', ', '.join(arr_repr), '])'))

    # Inheriting from MutableMapping gives us a whole whackload of methods for
    # free.
    bases = (collections.MutableMapping,)

    return type(name, bases, {
        '__init__': init,
        '__doc__': doc,

        '__getitem__': getitem,
        '__setitem__': setitem,
        '__delitem__': delitem,
        '__iter__': dict_iter,
        '__len__': dict_len,

        '__repr__': dict_repr,
    })
