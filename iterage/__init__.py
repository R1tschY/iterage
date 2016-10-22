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

import collections
import itertools
import operator
import sys

import iterage.generate


if (sys.version_info >= (3, 0)):
  # Python 3
  irange = range
  imap = map
  ifilter = filter
  ifilterfalse = itertools.filterfalse
  izip = zip
else:
  # Python 2.7
  irange = xrange
  imap = itertools.imap
  ifilter = itertools.ifilter
  ifilterfalse = itertools.ifilterfalse
  izip = itertools.izip



# Adaptors
# - adapt a iterable
def take(iterable, n):
  """
  take only the first n elements of the iterable.

      list(drop(xrange(12), 10)) == [10, 11]

  """
  return itertools.islice(iterable, n)

def drop(iterable, n):
  """
  drop the first n elements of the iterable.

      list(drop(xrange(12), 10)) == [10, 11]

  @see itertools.islice
  """
  return itertools.islice(iterable, n, None)

def cycle(iterable):
  """
  Repeats iterable endless:

      list(take(cycle(xrange(1)), 5) == [0, 1, 0, 1, 0]

  @note: function is saving content of iterable in the first run and returns in
    second cycle the elements of the copy. So it uses significant auxiliary
    storage (depending on the length of the iterable).

  @see itertools.cycle
  """
  return itertools.cycle(iterable)

def irepeat(iterable, n=1):
  """
  repeat every element of iterable n times

      list(irepeat(xrange(3), 2)) == [0, 0, 1, 1, 2, 2]

  @todo: use more itertools for more speed
  """
  for i in iterable:
    for _ in irange(n):
      yield i

def unique(iterable, key=None):
  """
  List unique elements, preserving order. Remember only the element just seen.
  """
  return imap(next, imap(operator.itemgetter(1), itertools.groupby(iterable, key)))

def unique_v2(iterable, key=None):
  """
  List unique elements, preserving order. Remember only the element just seen.
  """
  return imap(operator.itemgetter(0), itertools.groupby(iterable, key))

def ifilter(iterable, pred=bool):
  """
  """
  return ifilter(pred, iterable)

def ifilter_not(iterable, pred=bool):
  """
  """
  return ifilterfalse(pred, iterable)

def visit(iterable, func):
  for e in iterable:
    func(e)
    yield e

# def visit_v2(iterable, func):
#   def __visitor(e):
#     func(e)
#     return e
#
#   return itertools.imap(__visitor, iterable)

def transform(iterable, func):
  return imap(func, iterable)

def chunk(iterable, n):
  islice = itertools.islice
  ltuple = tuple

  it = iter(iterable)
  item = ltuple(islice(it, n))
  while item:
    yield item
    item = ltuple(islice(it, n))

def chunk_filled(iterable, n, fillvalue=None):
  args = [iter(iterable)] * n
  return itertools.izip_longest(fillvalue=fillvalue, *args)

def chunk_trunc(iterable, n, fillval=None):
  args = [iter(iterable)] * n
  return izip(*args)
