# -*- coding=utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2016 R1tschY
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import Sized
from collections import deque
from functools import singledispatch

from itertools import islice, count, groupby, filterfalse

# a sentinal - do not use as value in any iterable

_SENTINEL = object()
_NOTHING = object()


def consume(iterator, n=None):
    """
    Advance the iterator n-steps ahead. If n is `None`, consume entirely.

    copied from:
    https://docs.python.org/2/library/itertools.html

    >>> it = iter([1, 2, 3])
    >>> consume(it, 2)
    >>> tuple(it)
    (3,)

    >>> list = []
    >>> consume(visit([1, 2, 3], lambda x: list.append("/" + str(x))))
    >>> list
    ['/1', '/2', '/3']

    """
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        deque(iterator, maxlen=0)
    else:
        # advance to the empty slice starting at position n
        next(islice(iterator, n, n), None)


def foreach(function, *iterables):
    consume(map(function, *iterables))


@singledispatch
def ilen(iterable):
    """
    copyied from zuo: http://stackoverflow.com/a/15112059/1188453

    >>> ilen([1, 2, 3])
    3

    """
    counter = count()
    deque(zip(iterable, counter), maxlen=0)
    return next(counter)


@ilen.register(Sized)
def _ilen(iterable):
    return len(iterable)


def icount_if(iterable, pred=bool):
    """
    Count how many times the predicate is true.

    >>> icount_if(x < 5 for x in range(10))
    5
    >>> icount_if(range(10), lambda x: x < 5)
    5

    """
    return ilen(filter(pred, iterable))


def all_equal(iterable):
    """
    Returns True if all the elements are equal to each other

    >>> all_equal((5, 5, 5))
    True

    """
    g = groupby(iterable)
    return next(g, True) and not next(g, False)


def find_first(iterable, pred=bool, default=_NOTHING):
    """
    Find the first value that matches predicate pred
    @todo: find fastest: https://stackoverflow.com/questions/2361426/what-is-the-best-way-to-get-the-first-item-from-an-iterable-matching-a-condition

    >>> find_first((0, 1, 2))
    1
    >>> find_first((0, 1, 2), lambda x: x > 5, default=-1)
    -1

    """
    if default is _NOTHING:
        n = next(filter(pred, iterable), _SENTINEL)
        if n is _SENTINEL:
            raise LookupError("no such element")
        return n
    else:
        return next(filter(pred, iterable), default)


def find_first_not(iterable, pred=bool, default=_NOTHING):
    """
    Find the first value that not matches predicate C{pred}.

    >>> find_first_not((True, 0, 2))
    0
    >>> find_first_not((0, 1, 2), lambda x: x <= 2, default=-1)
    -1

    """
    if default is _NOTHING:
        n = next(filterfalse(pred, iterable), _SENTINEL)
        if n is _SENTINEL:
            raise LookupError("no such element")
        return n
    else:
        return next(filterfalse(pred, iterable), default)


def is_empty(iterable):
    """
    Returns True if iterable contains no elements

    >>> is_empty(())
    True
    >>> is_empty(x for x in range(5) if x > 42)
    True

    """
    return next(iter(iterable), _SENTINEL) is _SENTINEL


def none(iterable):
    """
    Returns True if all values are True

    >>> none([False, 0, [], None, ""])
    True

    """
    return not any(iterable)


def first(iterable, default=None):
    """
    Returns the first item or a default value

    >>> first(x for x in [1, 2, 3] if x % 2 == 0)
    2
    >>> first((x for x in [1, 2, 3] if x > 42), -1)
    -1

    """
    return next(iter(iterable), default)


def single(iterable):
    """
    Returns the item in iterable with one item or raise ValueError exception.

    >>> single(x for x in [1, 2, 3] if x % 2 == 0)
    2
    >>> single((x for x in [1, 2, 3] if x % 2 == 1))
    Traceback (most recent call last):
    ValueError
    >>> single(x for x in [1, 2, 3] if x > 42)
    Traceback (most recent call last):
    ValueError

    """
    iterator = iter(iterable)
    item = next(iterator, _SENTINEL)
    if item is _SENTINEL:
        raise LookupError("empty iterator")

    n = next(iterator, _SENTINEL)
    if n is _SENTINEL:
        return item
    else:
        raise LookupError("more than one element")


def to_optional(iterable):
    """
    Returns the item in iterable with one or none item or
    raise ValueError exception.

    >>> to_optional(x for x in [1, 2, 3] if x % 2 == 0)
    2
    >>> to_optional((x for x in [1, 2, 3] if x % 2 == 1))
    Traceback (most recent call last):
    ValueError
    >>> to_optional(x for x in [1, 2, 3] if x > 42)

    """
    iterator = iter(iterable)
    item = next(iterator, _SENTINEL)
    if item is _SENTINEL:
        return None

    n = next(iterator, _SENTINEL)
    if n is _SENTINEL:
        return item
    else:
        raise ValueError("more than one element")
