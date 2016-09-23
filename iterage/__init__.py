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

import iterage.generate


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
    secound cycle the elements of the copy. So it uses significant auxiliary
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
    for _ in xrange(n):
      yield i

def unique(iterable, key=None):
  """
  List unique elements, preserving order. Remember only the element just seen.
  """
  return itertools.imap(next, itertools.imap(operator.itemgetter(1), itertools.groupby(iterable, key)))

def unique_v2(iterable, key=None):
  """
  List unique elements, preserving order. Remember only the element just seen.
  """
  return itertools.imap(operator.itemgetter(0), itertools.groupby(iterable, key))

def ifilter(iterable, pred=bool):
  """
  @todo: x for x in iterable if pred(x) faster?
  """
  return itertools.ifilter(pred, iterable)

def ifilter_not(iterable, pred=bool):
  """
  @todo: x for x in iterable if not pred(x) faster?
  """
  return itertools.ifilterfalse(pred, iterable)

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
  return itertools.imap(func, iterable)

def imap(func, *iterables):
  return itertools.imap(func, iterables)

def chunk(iterable, n):
  iterator = iter(iterable)
  while True:
    a = tuple(itertools.islice(iterator, n))
    if len(a) == n:
      yield a
    else:
      if len(a) > 0:
        yield a
      return

def chunk_filled(iterable, n, fillvalue=None):
  args = [iter(iterable)] * n
  return itertools.izip_longest(fillvalue=fillvalue, *args)

def chunk_trunc(iterable, n, fillval=None):
  args = [iter(iterable)] * n
  return itertools.izip(*args)
