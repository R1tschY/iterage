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

# a sentinal - do not use as value in iterable
SENTINEL = object()

# Executors
# - go through a iterable
#
# TODO:
# - for_each/foreach(iterable, func)
# - consume - run only through iterable
# Reduce

def icount(iterable):
  """
  copyied from zuo: http://stackoverflow.com/a/15112059/1188453
  """
  if hasattr(iterable, '__len__'):
    return len(iterable)

  counter = itertools.count()
  deque(itertools.izip(iterable, itertools.count()), maxlen=0)
  return next(counter)

def icount_if(iterable, pred=bool):
  """
  Count how many times the predicate is true.

      count_if(x < 5 for x in xrange(10))   # -> 5
      count_if(xrange(10), lambda x: x < 5) # -> 5
  """
  return icount(itertools.ifilter(pred, iterable))

def all_equal(iterable):
  """
  Returns True if all the elements are equal to each other
  """
  g = itertools.groupby(iterable)
  return next(g, True) and not next(g, False)

def find_first(iterable, pred=bool, default=None):
  """
  Find the first value that matches predicate pred
  @todo: find fastest: https://stackoverflow.com/questions/2361426/what-is-the-best-way-to-get-the-first-item-from-an-iterable-matching-a-condition
  """
  return next(itertools.ifilter(pred, iterable), default)

def find_first_not(iterable, pred=bool, default=None):
  """
  Find the first value that not matches predicate pred
  """
  return next(itertools.ifilterfalse(pred, iterable), default)

def iempty(iterable):
  """
  Returns True if iterable contains no elements
  @todo: test performance: https://stackoverflow.com/questions/661603/how-do-i-know-if-a-generator-is-empty-from-the-start
  """
  _SENTINEL = SENTINEL
  return next(iter(iterable), _SENTINEL) is _SENTINEL

def iall(iterable):
  """
  Returns True if all values are True
  """
  return all(iterable)

def iany(iterable):
  """
  Returns True if all values are True
  """
  return any(iterable)

def inone(iterable, pred=bool):
  """
  Returns True if all values are True
  """
  return not any(iterable)

def first(iterable, default=None):
  "Returns the first item or a default value"
  return next(iter(iterable), default)

def single(iterable, default=None):
  """
  Returns the first item or a default value
  @bug: raise exception if there are more than one element
  """
  return next(iter(iterable), default)

def max_element(iterable, key=None):
  """
  Returns the largest item in the iterable.
  @note: equivalent to: max(iterable[, key])
  """
  return max(iterable, key)

def min_element(iterable, key=None):
  """
  Returns the smallest item in the iterable.
  @note: equivalent to: min(iterable[, key])
  """
  return min(iterable, key)


