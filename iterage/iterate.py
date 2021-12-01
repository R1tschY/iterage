# -*- coding=utf-8 -*-

# Adaptors
# - adapt a iterable
from collections import Sequence, deque
from itertools import islice, cycle as icycle, groupby, zip_longest
from operator import itemgetter

from typing import Iterable, Iterator, TypeVar, Any, Callable, Optional

T = TypeVar("T")
U = TypeVar("U")


def take(iterable: Iterable[T], n) -> Iterator[T]:
    """
    take only the first n elements of the iterable.

    >>> list(take(range(12), 2))
    [0, 1]

    """
    return islice(iterable, n)


def take_last(iterable: Iterable[T], n: int) -> Iterator[T]:
    """
    take only the last n elements of the iterable.

    >>> list(take_last(range(1000), 3))
    [997, 998, 999]

    """
    return deque(iterable, maxlen=n)


def drop(iterable: Iterable[T], n) -> Iterator[T]:
    """
    drop the first n elements of the iterable.

    >>> list(drop(range(12), 10))
    [10, 11]

    @see itertools.islice
    """
    return islice(iterable, n, None)


def iterate(start: T, fn: Callable[[T], T]) -> T:
    while 1:
        start = fn(start)
        yield start


def uniq(
        iterable: Iterable[T], key: Optional[Callable[[T], U]]=None
) -> Iterator[T]:
    """
    List unique elements, preserving order. Remember only the element just seen.

    >>> tuple(uniq([1, 2, 2, 3]))
    (1, 2, 3)
    >>> tuple(uniq(sorted([5, 4, 3, 5, 3, 3])))
    (3, 4, 5)

    """
    if key is None:
        return map(itemgetter(0), groupby(iterable, key))
    else:
        return map(
            next, map(itemgetter(1), groupby(iterable, key)))


def dedup(
    iterable: Iterable[T], key: Optional[Callable[[T], U]]=None
) -> Iterator[T]:
    """
    List unique elements.

    >>> tuple(dedup([5, 4, 3, 5, 3, 3]))
    (3, 4, 5)

    """
    return uniq(sorted(iterable, key=key), key)


def visit(iterable: Iterable[T], func: Callable[[T], Any]) -> Iterator[T]:
    """
    Visit every element in iterable, without editing the data.
    """
    for e in iterable:
        func(e)
        yield e


def chunk(iterable: Iterable[T], n: int) -> Iterator[Iterable[T]]:
    """
    Group data in fixed-length chunks.

    >>> tuple(chunk([1, 2, 3, 4, 5], 2))
    ([1, 2], [3, 4], [5])
    >>> tuple(chunk((x for x in range(1, 6)), 2))
    ((1, 2), (3, 4), (5,))

    """
    if isinstance(iterable, Sequence):
        for i in range(0, len(iterable), n):
            yield iterable[i:i + n]
    else:
        _islice = islice
        _tuple = tuple

        it = iter(iterable)
        item = _tuple(_islice(it, n))
        while item:
            yield item
            item = _tuple(_islice(it, n))


def chunk_filled(
        iterable: Iterable[T], n: int, fillvalue: Any=None
) -> Iterator[Iterable[T]]:
    """
    Group data in fixed-length chunks and fill up chunks with C{fillvalue}.

    >>> tuple(chunk_filled([1, 2, 3, 4, 5], 2))
    ((1, 2), (3, 4), (5, None))

    >>> tuple(chunk_filled([1, 2, 3, 4, 5], 2, fillvalue=0))
    ((1, 2), (3, 4), (5, 0))

    """
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


def chunk_trunc(iterable: Iterable[T], n: int) -> Iterator[Iterable[T]]:
    """
    Group data in full fixed-length chunks.

    >>> tuple(chunk_trunc([1, 2, 3, 4, 5], 2))
    ((1, 2), (3, 4))

    """
    args = [iter(iterable)] * n
    return zip(*args)
