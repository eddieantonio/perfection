"""
Utilities for generating perfect hash functions for integer keys.

This module implements the first fit decreasing method, described in
Gettys01_. It is **not** guaranteed to generate a *minimal* perfect hash,
though by no means is it impossible. See for example:

>>> phash = hash_parameters('+-<>[].,', to_int=ord)
>>> len(phash.slots)
8
>>> phash.slots
('+', ',', '-', '.', '<', '[', '>', ']')

.. _Gettys01: http://www.drdobbs.com/architecture-and-design/generating-perfect-hash-functions/184404506

"""

from .perfection import make_hash, make_dict, hash_parameters

__version__ = '1.0.2'
__all__ = ['make_hash', 'make_dict', 'hash_parameters']
