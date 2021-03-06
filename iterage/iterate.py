# -*- coding=utf-8 -*-

import itertools
import operator
from .compat import *

# Adaptors
# - adapt a iterable
def take(iterable, n):
    """
    take only the first n elements of the iterable.

    >>> list(take(range(12), 2))
    [0, 1]

    """
    return itertools.islice(iterable, n)


def drop(iterable, n):
    """
    drop the first n elements of the iterable.

    >>> list(drop(range(12), 10))
    [10, 11]

    @see itertools.islice
    """
    return itertools.islice(iterable, n, None)


def cycle(iterable):
    """
    Repeats iterable endless:

    >>> list(take(cycle(range(2)), 5))
    [0, 1, 0, 1, 0]

    @note: function is saving content of iterable in the first run and returns in
      second cycle the elements of the copy. So it uses significant auxiliary
      storage (depending on the length of the iterable).

    @see itertools.cycle
    """
    return itertools.cycle(iterable)


def unique(iterable, key=None):
    """
    List unique elements, preserving order. Remember only the element just seen.

    >>> tuple(unique([1, 2, 2, 3]))
    (1, 2, 3)
    >>> tuple(unique(sorted([5, 4, 3, 5, 3, 3])))
    (3, 4, 5)

    """
    return map(
        next,
        map(operator.itemgetter(1), itertools.groupby(iterable, key)))


def unique_v2(iterable, key=None):
    """
    List unique elements, preserving order. Remember only the element just seen.
    """
    return map(operator.itemgetter(0), itertools.groupby(iterable, key))


def visit(iterable, func):
    """
    Visit every element in iterable, without editing the data.
    """
    for e in iterable:
        func(e)
        yield e


def transform(iterable, func):
    """
    Transform data from C{iterable} through call to C{func}.

    >>> tuple(transform([1, 2, 3], str))
    ('1', '2', '3')

    """
    return map(func, iterable)


def chunk(iterable, n):
    """
    Group data in fixed-length chunks.

    >>> tuple(chunk([1, 2, 3, 4, 5], 2))
    ((1, 2), (3, 4), (5,))

    """
    islice = itertools.islice
    ltuple = tuple

    it = iter(iterable)
    item = ltuple(islice(it, n))
    while item:
        yield item
        item = ltuple(islice(it, n))


def chunk_filled(iterable, n, fillvalue=None):
    """
    Group data in fixed-length chunks and fill up chunks with C{fillvalue}.

    >>> tuple(chunk_filled([1, 2, 3, 4, 5], 2))
    ((1, 2), (3, 4), (5, None))

    >>> tuple(chunk_filled([1, 2, 3, 4, 5], 2, fillvalue=0))
    ((1, 2), (3, 4), (5, 0))

    """
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


def chunk_trunc(iterable, n):
    """
    Group data in full fixed-length chunks.

    >>> tuple(chunk_trunc([1, 2, 3, 4, 5], 2))
    ((1, 2), (3, 4))

    """
    args = [iter(iterable)] * n
    return zip(*args)
