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

from collections import deque
import itertools

import iterage


# a sentinal - do not use as value in any iterable
SENTINEL = object()


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
  >>> consume(iterage.visit([1, 2, 3], lambda x: list.append("/" + str(x))))
  >>> list
  ['/1', '/2', '/3']

  """
  # Use functions that consume iterators at C speed.
  if n is None:
    # feed the entire iterator into a zero-length deque
    deque(iterator, maxlen=0)
  else:
    # advance to the empty slice starting at position n
    next(itertools.islice(iterator, n, n), None)


def foreach(function, *iterables):
  consume(iterage.imap(function, *iterables))


def icount(iterable):
  """
  copyied from zuo: http://stackoverflow.com/a/15112059/1188453

  >>> icount([1, 2, 3])
  3

  """
  if hasattr(iterable, '__len__'):
    return len(iterable)

  counter = itertools.count()
  deque(iterage.izip(iterable, counter), maxlen=0)
  return next(counter)


def icount_if(iterable, pred=bool):
  """
  Count how many times the predicate is true.

  >>> icount_if(x < 5 for x in range(10))
  5
  >>> icount_if(range(10), lambda x: x < 5)
  5

  """
  return icount(iterage.ifilter(pred, iterable))


def all_equal(iterable):
  """
  Returns True if all the elements are equal to each other

  >>> all_equal((5, 5, 5))
  True

  """
  g = itertools.groupby(iterable)
  return next(g, True) and not next(g, False)


def find_first(iterable, pred=bool, default=None):
  """
  Find the first value that matches predicate pred
  @todo: find fastest: https://stackoverflow.com/questions/2361426/what-is-the-best-way-to-get-the-first-item-from-an-iterable-matching-a-condition

  >>> find_first((0, 1, 2))
  1
  >>> find_first((0, 1, 2), lambda x: x > 5, default=-1)
  -1

  """
  return next(iterage.ifilter(pred, iterable), default)


def find_first_not(iterable, pred=bool, default=None):
  """
  Find the first value that not matches predicate C{pred}.

  >>> find_first_not((True, 0, 2))
  0
  >>> find_first_not((0, 1, 2), lambda x: x <= 2, default=-1)
  -1

  """
  return next(iterage.ifilterfalse(pred, iterable), default)


def is_empty(iterable):
  """
  Returns True if iterable contains no elements
  @todo: test performance: https://stackoverflow.com/questions/661603/how-do-i-know-if-a-generator-is-empty-from-the-start

  >>> is_empty(())
  True
  >>> is_empty(x for x in range(5) if x > 42)
  True

  """
  _SENTINEL = SENTINEL
  return next(iter(iterable), _SENTINEL) is _SENTINEL


def iall(iterable):
  """
  Returns True if all values are True

  >>> iall([True, 1, 42])
  True

  """
  return all(iterable)


def iany(iterable):
  """
  Returns True if all values are True

  >>> iany([True, 0, False])
  True

  """
  return any(iterable)


def inone(iterable):
  """
  Returns True if all values are True

  >>> inone([False, 0, [], None, ""])
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
  try:
    it = iter(iterable)
    item = next(it)
    try:
      next(it)
    except StopIteration:
      return item
  except StopIteration:
    pass

  raise ValueError()


def imax(iterable, key):
  """
  Returns the largest item in the iterable.
  @note: equivalent to: max(iterable[, key])
  """
imax = max


def imin(iterable, key):
  """
  Returns the smallest item in the iterable.
  @note: equivalent to: min(iterable[, key])
  """
imin = min
