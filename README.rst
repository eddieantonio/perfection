***************************************
perfection — Perfect hashing utilities
***************************************

.. image:: https://travis-ci.org/eddieantonio/perfection.svg?branch=master
    :target: https://travis-ci.org/eddieantonio/perfection

A module that creates perfect hash functions for a known set of integer
inputs.

::

    >>> import perfection
    >>> l = (0, 3, 4, 7 ,10, 13, 15, 18, 19, 21, 22, 24, 26, 29, 30, 34)
    >>> hf = perfection.make_hash(l)
    >>> hf(19)
    1


Install
-------

::

   pip install perfection


Main features
-------------

- ``make_hash()`` that generates an honest-to-goodness perfect hash function
  for the given keys.
- ``make_dict()`` creates a dictionary subclass that implements the
  MutableMapping_ interface (thus, acts exactly like a ``dict``), and
  uses the hash function created in the equivalent call to ``make_hash()``.

Additionally, ``hash_parameters()`` may be used to output the parameters of
making a perfect hash for the given set of input keys. These parameters can
then be used to implement a perfect hash function in a language of your
choice.

For example, generate ``t`` and ``r`` parameters using ``hash_parameters()``::

    >>> l = (0, 3, 4, 7 ,10, 13, 15, 18, 19, 21, 22, 24, 26, 29, 30, 34)
    >>> params = hash_parameters(l)
    >>> params.t
    6
    >>> params.r
    (2, 7, 12, 0, 7, 10)

Then, the hash function, in pseudocode is as follows::

     function hash(i):
         static r = { 2, 7, 12, 0, 7, 10 }
         static t = 6

         x = i mod t
         y = i div t
         return x + r[y]

Note that ``div`` stands for *floor* (integer) division.

.. _MutableMapping: https://docs.python.org/2/library/collections.html#collections.MutableMapping

Beta Features
-------------

Can import a minimal perfect (ordered!) hash function with the same API
using::

    import perfection.czech

API is not yet finalized!


Credit
------

Algorithm described by `Thomas Gettys`__.

Python code © 2014, 2016 Eddie Antonio Santos. MIT licensed.

With contributions by Thomas Calmant.

.. __: http://www.drdobbs.com/architecture-and-design/generating-perfect-hash-functions/184404506

