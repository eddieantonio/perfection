# Perfect hashing

A module that creates perfect hash functions for a known set of integer
inputs.

```python
>>> import perfection

>>> l = (0, 3, 4, 7 ,10, 13, 15, 18, 19, 21, 22, 24, 26, 29, 30, 34)
>>> hf = mphf.make_hash(l)
>>> hf(19)
1
```

# Credit

Algorithm described by [Thomas Gettys][Getty01].

Python code © 2014 Eddie Antonio Santos. MIT licensed.

[Getty01]: http://www.drdobbs.com/architecture-and-design/generating-perfect-hash-functions/184404506

