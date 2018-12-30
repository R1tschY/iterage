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

__version__ = "0.1.dev"

import itertools
import operator
import sys

if sys.version_info >= (3, 0):
    # Python 3
    irange = range
    imap = map
    ifilter = filter
    ifilterfalse = itertools.filterfalse
    izip = zip
    izip_longest = itertools.zip_longest
else:
    # Python 2.7
    irange = xrange
    imap = itertools.imap
    ifilter = itertools.ifilter
    ifilterfalse = itertools.ifilterfalse
    izip = itertools.izip
    izip_longest = itertools.izip_longest


# Adaptors
# - adapt a iterable
def take(iterable, n):
    """
    take only the first n elements of the iterable.

    >>> list(take(irange(12), 2))
    [0, 1]

    """
    return itertools.islice(iterable, n)


def drop(iterable, n):
    """
    drop the first n elements of the iterable.

    >>> list(drop(irange(12), 10))
    [10, 11]

    @see itertools.islice
    """
    return itertools.islice(iterable, n, None)


def cycle(iterable):
    """
    Repeats iterable endless:

    >>> list(take(cycle(irange(2)), 5))
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
    return imap(next,
                imap(operator.itemgetter(1), itertools.groupby(iterable, key)))


def unique_v2(iterable, key=None):
    """
    List unique elements, preserving order. Remember only the element just seen.
    """
    return imap(operator.itemgetter(0), itertools.groupby(iterable, key))


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
    return imap(func, iterable)


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
    return izip_longest(fillvalue=fillvalue, *args)


def chunk_trunc(iterable, n):
    """
    Group data in full fixed-length chunks.

    >>> tuple(chunk_trunc([1, 2, 3, 4, 5], 2))
    ((1, 2), (3, 4))

    """
    args = [iter(iterable)] * n
    return izip(*args)


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
