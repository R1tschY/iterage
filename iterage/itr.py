# -*- coding=utf-8 -*-

import collections
import collections.abc
from collections import deque, Collection
from functools import reduce, singledispatch
from itertools import *
from typing import Any, Callable, Generic, Iterable, Iterator, Optional, Tuple, \
    TypeVar, Union, ClassVar, Sequence, Sized, Dict, List, Counter

from iterage import all_equal, chunk, chunk_filled, chunk_trunc, dedup, \
    find_first, ilen, single, uniq, to_optional

__all__ = ("itr", "Itr")

T = TypeVar("T")
U = TypeVar("U")

_nothing = object()
_sentinal = object()


def sliding(iterable, length):
    iterator = iter(iterable)

    _tuple = tuple
    _next = next
    sentinal = _sentinal

    queue = deque(islice(iterator, length), length)
    yield _tuple(queue)

    while True:
        e = _next(iterator, sentinal)
        if e is sentinal:
            break
        queue.append(e)
        yield _tuple(queue)


def partial_reduce(op, iterable):
    iterator = iter(iterable)

    r = next(iterator, _sentinal)
    if r is _sentinal:
        return

    yield r
    for v in iterator:
        r = op(r, v)
        yield r


class Itr(Iterable[T]):
    """

    :note: Do not reuse a instance of Itr: Do not make more than one call to
        a Itr instance. Every thing other than is will end in unexpected
        results. If you have the do multiple operations on the same data, use
        toList or better toTuple and then create to new instances.

    >>> t = itr(range(5)).to_tuple()
    >>> itr(t).map(...)
    >>> itr(t).map(...)

    """

    _itr = ...  # type: Iterable[T]

    def __init__(self, itr):
        self._itr = itr

    # generators

    @classmethod
    def repeat(cls, v: T, n: int) -> "Itr[T]":
        """
        return a iterable with n elements.

        >>> "".join(Itr.repeat("A", 3))
        'AAA'

        """
        return cls(repeat(v, n))

    @classmethod
    def ntimes(cls, n: int) -> "Itr[None]":
        """
        return a iterable with n elements.

        >>> for i in Itr.ntimes(3):
        ...   print(i)
        None
        None
        None

        :see: Itr.ntimes
        """
        return cls(repeat(None, n))

    @classmethod
    def empty(cls) -> "Itr[T]":
        """
        Create an empty iterable.

        >>> Itr.empty().to_list()
        []

        """
        return cls(())

    @classmethod
    def from_optional(cls, v: Optional[T]) -> "Itr[T]":
        """
        Make a iterable from a optional

        >>> Itr.from_optional(None).map(lambda x: x / 2).to_optional()
        >>> Itr.from_optional(4).map(lambda x: x / 2).to_optional()
        2.0
        """
        return cls.empty() if v is None else cls((v,))

    # selecting

    def take(self, n: int) -> "Itr[T]":
        """
        Pass through only n elements.

        >>> itr(range(1000)).take(2).to_list()
        [0, 1]
        >>> itr(range(1000)).take(0).to_list()
        []
        >>> itr(range(1)).take(100).to_list()
        [0]

        :see: Itr.drop, Itr.take_while
        """
        return self.__class__(islice(self._itr, n))

    def take_while(self, pred):
        """
        Pass through only elements until pred is ´false´

        >>> itr(range(1000)).take_while(lambda x: x < 2).to_list()
        [0, 1]

        :see: Itr.drop_while, Itr.take
        """
        return self.__class__(takewhile(pred, self._itr))

    def take_last(self, n: int) -> "Itr[T]":
        """
        take only the last n elements of the iterable.

        >>> itr(range(1000)).take_last(3).to_list()
        [997, 998, 999]
        >>> itr(range(2)).take_last(3).to_list()
        [0, 1]

        """
        return self.__class__(deque(self._itr, maxlen=n))

    def drop(self, n: int) -> "Itr[T]":
        """
        Skip the first ´n´ elements

        >>> itr(range(4)).drop(2).to_list()
        [2, 3]
        >>> itr(range(4)).drop(6).to_list()
        []

        """
        return self.__class__(islice(self._itr, n, None))

    def drop_while(self, pred):
        """
        Skip elements until pred is ´false´

        >>> itr(range(4)).drop_while(lambda x: x < 2).to_list()
        [2, 3]

        :see: Itr.take_while, Itr.drop
        """
        return self.__class__(dropwhile(pred, self._itr))

    def slice(self, *args):
        """
        Slice elements

        >>> itr(range(4)).slice(1, 3).to_list()
        [1, 2]
        >>> itr(range(4)).slice(1, None).to_list()
        [1, 2, 3]
        >>> itr(range(4)).slice(1).to_list()
        [0]
        >>> itr(range(4)).slice(None, 2).to_list()
        [1, 2]
        >>> itr(range(4)).slice(None, None).to_list()
        [0, 1, 2, 3]

        """
        return self.__class__(islice(self._itr, *args))

    def where(self, fn: Callable[[T], U]) -> "Itr[T]":
        """
        Pass through only elements where `fn(x)` returns `true`

        >>> itr(range(4)).where(lambda x: x % 2 == 0).to_list()
        [0, 2]

        """
        return self.__class__(filter(fn, self._itr))

    def where_not(self, fn: Callable[[T], U]) -> "Itr[T]":
        return self.__class__(filterfalse(fn, self._itr))

    def drop_elements(self, t: T) -> "Itr[T]":
        return self.__class__(e for e in self._itr if e == t)

    def drop_na(self) -> "Itr[T]":
        return self.__class__(e for e in self._itr if e is not None)

    # ordering

    def sort(self, key: Optional[Callable[[T], U]] = None) -> "Itr[T]":
        if key is None:
            return self.__class__(sorted(self._itr))
        else:
            return self.__class__(sorted(self._itr, key=key))

    def reverse(self) -> "Itr[T]":
        try:
            return self.__class__(reversed(self._itr))
        except TypeError:
            return self.__class__(reversed(list(self._itr)))

    # unique

    def uniq(self, key: Optional[Callable[[T], U]]=None) -> "Itr[T]":
        return self.__class__(uniq(self._itr, key))

    def dedup(self, key: Optional[Callable[[T], U]]=None) -> "Itr[T]":
        return self.__class__(dedup(self._itr, key))

    # mapping

    def map(self, fn: Callable[[T], U]) -> "Itr[U]":
        return self.__class__(map(fn, self._itr))

    def star_map(self, fn: Callable[..., U]) -> "Itr[U]":
        return self.__class__(starmap(fn, self._itr))

    def flat_map(self, fn: Callable[[T], Iterable[U]]) -> "Itr[U]":
        return self.__class__(chain.from_iterable(map(fn, self._itr)))

    def flatten(self) -> "Itr":
        return self.__class__(chain.from_iterable(self._itr))

    def chunk(self, n: int) -> "Itr[Sequence[T]]":
        return self.__class__(chunk(self._itr, n))

    def chunk_filled(
            self, n: int, fillvalue: Any=None) -> "Itr[Sequence[T]]":
        return self.__class__(chunk_filled(self._itr, n, fillvalue))

    def chunk_trunc(self, n: int) -> "Itr[Sequence[T]]":
        return self.__class__(chunk_trunc(self._itr, n))

    def zip(
            self, other: Iterable[U]
    ) -> "Itr[Tuple[T, U]]":
        return self.__class__(zip(self._itr, other))

    def zip_longest(
            self, other: Iterable[U], fillvalue: Any=None
    ) -> "Itr[Tuple[T, U]]":
        return self.__class__(zip_longest(self._itr, other, fillvalue))

    def enumerate(self, start=0) -> "Itr[Tuple[int, T]]":
        return self.__class__(enumerate(self._itr, start))

    def sliding(self, length):
        return self.__class__(sliding(self._itr, length))

    def accumulate(self):
        return self.__class__(accumulate(self._itr))

    def group_by(self, key: Callable[[T], U]) -> Dict[U, List[T]]:
        result = {}
        for item in self._itr:
            k = key(item)
            if k in result:
                result[k].append(item)
            else:
                result[k] = [item]
        return result

    # composing

    def prelude(self, prelude: Iterable[T]) -> Iterable[T]:
        return self.__class__(chain(prelude, self._itr))

    def postlude(self, postlude: Iterable[T]) -> Iterable[T]:
        return self.__class__(chain(self._itr, postlude))

    def cycle(self):
        return self.__class__(cycle(self._itr))

    # combinatoric

    def product(self, repeat):
        return self.__class__(product(self._itr, repeat))

    def permutations(self, r=None):
        return self.__class__(permutations(self._itr, r))

    def combinations(self, r):
        return self.__class__(combinations(self._itr, r))

    def combinations_with_replacement(self, r):
        return self.__class__(combinations_with_replacement(self._itr, r))

    # reduce

    def reduce(self, f: Callable[[T, T], T], *args):
        return reduce(f, self._itr, *args)

    def to_string(self, sep: str):
        return sep.join(map(str, self._itr))

    def to_list(self):
        return list(self._itr)

    def to_tuple(self):
        return tuple(self._itr)

    def to_dict(self):
        return dict(self._itr)

    def to_set(self):
        return set(self._itr)

    def collect(self, cls: Callable[[Iterable[T]], U]) -> U:
        return cls(self._itr)

    def to_optional(self) -> Optional[T]:
        """
        >>> itr(range(1)).to_optional()
        0
        >>> itr(range(0)).to_optional()
        >>> itr(range(2)).to_optional()
        Traceback (most recent call last):
        LookupError
        """
        return to_optional(self._itr)

    def consume(self) -> None:
        deque(self._itr, maxlen=0)

    def foreach(self, fn: Callable[[T], None]) -> None:
        self.map(fn).consume()

    def sum(self) -> T:
        return sum(self._itr)

    def all(self) -> bool:
        return all(self._itr)

    def any(self) -> bool:
        return any(self._itr)

    def none(self) -> bool:
        return not any(self._itr)

    def max(self, *args, **kwargs) -> T:
        return max(self._itr, *args, **kwargs)

    def min(self) -> T:
        return min(self._itr)

    def len(self) -> int:
        return ilen(self._itr)

    def find_first(self, pred, default=_nothing):
        return find_first(self._itr, pred, default)

    def is_empty(self) -> bool:
        return next(iter(self._itr), _sentinal) is _sentinal

    def all_equal(self) -> bool:
        return all_equal(self._itr)

    def first(self, default: T = None) -> T:
        return next(iter(self._itr), default)

    def single(self) -> T:
        return single(self._itr)

    def nth(self, n: int, default=None) -> T:
        if n < 0:
            raise ValueError("n must be greater than or equal 0")
        return next(islice(self._itr, n - 1, None), default)

    def count(self, t: T) -> int:
        return sum(e == t for e in self._itr)

    def exists(self, t: Callable[[T], bool]) -> bool:
        return any(map(t, self._itr))

    def quantities(self) -> Counter[T]:
        return collections.Counter(self._itr)

    # integration

    def __iter__(self) -> Iterator[T]:
        return iter(self._itr)

    def __repr__(self):
        return f"Itr({repr(self._itr)})"

    def __str__(self):
        return f"Itr({str(self._itr)})"

    # TODO:
    #  sliding(n: int)
    #  sliding(n: int, step: int)
    #  partition -> (Itr, Itr)
    #  reduce/fold
    #  min(key)/max(key)/average(key)
    #  permutations
    #  nth/exactly_n/at_least
    #  length_compare
    #  slice
    #  transpose: zip(*iterable)
    #  chunk: iter(partial(take, n, iter(iterable)), [])
    #  last
    #  iterate: while True: yield start; start = func(start)
    #  interleave/interleave_longest (round robin?)
    #  fill/padded
    #  split_at
    #  split_into
    #  split
    #  unzip -> Iterable[Itr]
    #  replace
    #  fill_na
    #  sample
    #  shuffle
    #  choose
    #  search
    #  rotate
    #  iota/range
    #  std::inner_product/std::adjacent_difference/std::partial_sum


def itr(iterable: Iterable[T]) -> "Itr[T]":
    """
    Create Itr class from a iterable.

    >>> itr(range(3)).to_list()
    [0, 1, 2]
    >>> itr([56]).to_list()
    [56]
    >>> itr(x + 2 for x in range(3)).to_list()
    [2, 3, 4]

    """
    return Itr(iterable)
