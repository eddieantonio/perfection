#!/usr/bin/env python
# coding: utf-8

from pprint import pprint
from math import sqrt, ceil
from operator import itemgetter

def make_hash(items, minimize=True):
    """
    Generates a minimal perfect hash function.

    Based on first fit decreasing method:
    http://www.drdobbs.com/architecture-and-design/generating-perfect-hash-functions/184404506
    """
    items = frozenset(items)

    if minimize:
        offset = 0 - min(items)
        print "Minimize by %d" % offset
        items = frozenset(x + offset for x in items)

    # 1. Start with a square array that is t units on a side.
    # Choose a t such that t**2 >= max(S)
    t = int(ceil(sqrt(max(items))))
    assert t*t >= max(items)

    arr = square_array(t)

    # 2. Place each key K in the square at location (x,y), where x=K/t, y=K mod t.
    for item in items:
        x = item / t
        y = item % t
        arr[x][y] = item

    # 3. Rearrange rows and generate a displacement vector.
    displacement_vector = rearrange_rows(arr)

    print "Result of rearranging:"
    print_array(arr)

    # 4. Flatten the matrix into a row.
    result = [choose_non_none(arr, i) for i in xrange(len(arr[0]))]

    # Return the parameters
    return {
        't': t,
        'r': displacement_vector,
        'result': result,
        'offset': offset
    }

def print_array(array):
    for row in array:
        print '|',
        print '|'.join('%3d' % col
                if col is not None else '   ' for col in row),
        print '|'

def count_nones(seq):
    """Returns occurrences of None in the sequence"""
    i = 0
    for item in seq:
        if item is None:
            i += 1
    return i

def choose_non_none(array, column):
    for row in xrange(len(array)):
        item = array[row][column]
        if item is not None:
            return item
    raise ValueError("array at column %d does not contain any items: %r"
            % (column, array))


def rotate_nones(xs, n=0):
    """
    Rotates a list until the nth element is not None. Returns amount
    displaced.
    """
    assert n < len(xs), "Must choose n less than size of list."

    displacement = 0

    while xs[n] is None:
        head = xs.pop(0)
        xs.append(head)
        displacement += 1
        if displacement >= len(xs):
            raise ValueError("Row only contains None!")

    return displacement

def pair_elements(matrix):
    for number, row in enumerate(matrix):
        score = count_nones(row)
        if score != len(row):
            yield number, score, row

def make_queue(matrix):
    return sorted(pair_elements(matrix), key=itemgetter(1))

def get_first_non_none(xs):
    for i, x in enumerate(xs):
        if x is not None:
            return i
    raise ValueError("All values are None!")

def place_first_at(row, n):
    """
    Places the first item of the row at the nth column.

    >>> l = [None, None, None, 1]
    >>> place_first_at(l, 0)
    -3
    >>> l
    [1, None, None, None]
    >>> l = [1, None, 1, 2]
    >>> place_first_at(l, 2)
    2
    >>> l
    [1, 2, 1, None]
    """
    first = get_first_non_none(row)
    displacement = first - n

    #print "Displacement %d for row %r" % (displacement, row)

    if displacement != 0:
        rotate_row(row, displacement)
    # Rotate row actually takes negative displacement, so... yeah!
    return -displacement

def rotate_row(row, displacement):
    """
    Rotate the amount of times given the displacement. Positive displacements
    rotate to the left.

    >>> rotate_row([1, 2, 3, 4, 5], 1)
    [2, 3, 4, 5, 1]
    >>> rotate_row([1, 2, 3, 4, 5], -2)
    [4, 5, 1, 2, 3]
    """
    front = row[:displacement]
    back = row[displacement:]
    row[:] = back + front

    return row


def rearrange_rows(matrix):
    """
    Mutates the given matrix (list of lists) in order to make all items fit in
    each column. In addition to mutating the original array, returns a
    displacement vector -- a vector the size of the number of rows where each
    element specifies the amount that the corresponding row was displaced.

    The outer list must be a list of rows!
    """

    r = [0] * len(matrix)

    # List of unfilled columns, in ascending order.
    columns_unfilled = range(len(matrix[0]))

    # Sorted in descending order of most populous rows.
    row_queue = make_queue(matrix)

    print("Got these rows: ")
    pprint(row_queue)

    # Rotate all the rows appropriately.
    while row_queue:
        # Get the next elligible row.
        row_number, _score, limbo_row = row_queue.pop(0)

        #print "Next row is %d: %r (len %d)" % (row_number, limbo_row, _score)

        # Try placing it in every available next free slot.
        r[row_number] = try_all_free_slots(columns_unfilled, limbo_row)

        # Mark that columns have been filled. 
        occupied_columns = (index for index, item in enumerate(limbo_row)
                if item is not None)
        for col_num in occupied_columns:
            #print "Removing %d from %r" % (col_num, columns_unfilled)
            columns_unfilled.remove(col_num)

    return r
            

def try_all_free_slots(free_columns, row):
    for free_column in free_columns:
        if check_columns_okay(free_columns, row, free_column):
            # Found a free slot where all items can fit!
            #print "Row can move to column %d: %r" % (free_column, row)
            displacement = place_first_at(row, free_column)
            #print "Row is now", row
            return displacement
    raise ValueError("Could not fit row %r in free columns %r")

def check_columns_okay(free_columns, row, offset):
    """
    Checks if all the occupied columns in the row fit in the indices given by
    free columns.

    >>> check_columns_okay([0,1,2,3], [1, None, 3, None], 0)
    True
    >>> check_columns_okay([0,2,3], [None, None, 3, 4], 0)
    True
    >>> check_columns_okay([], [None, None, 3, 4], 0)
    False
    >>> check_columns_okay([0], [None, None, 3, None], 2)
    True
    >>> check_columns_okay([0], [None, None, None, 4], 2)
    False

    """
    for index, item in enumerate(row, start=offset):
        # Skip empty items in the row.
        if item is None:
            continue
        adjusted_index = index % len(row) 

        # Check if the index is in the appropriate place.
        if adjusted_index not in free_columns:
            #print "index %d not in %r" % (adjusted_index, free_columns)
            return False

    return True
        
        

def square_array(n):
    # TODO: No longer use an actual array!
    if type(n) is not int or n <= 0:
        raise ValueError("Must use non-negative integer.")

    return [[None] * n for _ in xrange(n)]

# This should be the output of the perfect hash mapping.
def perfect_hash(c):
    C = (  0,  1,  2,  3, 48, 17, 50, 19)
    r = (  0 , 0,  4,  0,  0,  0,  4,  0)
    k = ord(c) - 43
    x = k / 8
    y = k % 8
    i = r[x] + y
    return C[i]


if __name__ == '__main__':
    # TODO: Make this main more useful.
    items = (ord(c) for c in '+-<>[],.')
    print make_hash(items, minimize=True)
    print [chr(perfect_hash(c) + 43) for c in '<>+-[],.']


