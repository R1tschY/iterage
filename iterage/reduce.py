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

import itertools

# Executors
# - go through a iterable
#
# TODO:
# - for_each/foreach(iterable, func)
# - consume - run only through iterable

# Reduce

def count(iterable):
  return len(iterable)

def count_if(iterable, pred=bool):
  """
  Count how many times the predicate is true.

      count_if(xrange(10), lambda x: x < 5) -> 5
  """
  return sum(itertools.imap(pred, iterable))

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

def is_empty(iterable):
  """
  Returns True if iterable contains no elements
  @todo: test performance: https://stackoverflow.com/questions/661603/how-do-i-know-if-a-generator-is-empty-from-the-start
  """
  try:
    next(iterable)
    return False
  except StopIteration:
    return True

def iall(iterable, pred=bool):
  """
  Returns True if all values are True
  """
  if pred == bool:
    return all(iterable)
  else:
    return all(itertools.imap(pred, iterable))

def iany(iterable, pred=bool):
  """
  Returns True if all values are True
  """
  if pred == bool:
    return any(iterable)
  else:
    return any(itertools.imap(pred, iterable))


def inone(iterable, pred=bool):
  """
  Returns True if all values are True
  """
  if pred == bool:
    return not any(iterable)
  else:
    return not any(itertools.imap(pred, iterable))

def first(iterable, default=None):
  "Returns the first item or a default value"
  return next(iterable, default)

def single(iterable, default=None):
  """
  Returns the first item or a default value
  @bug: raise exception if there are more than one element
  """
  return next(iterable, default)

def max_element(iterable, key=bool):
  """
  Returns the largest item in the iterable.
  @note: equivalent to: max(iterable, key)
  """
  return max(iterable, key)

def min_element(iterable, key=bool):
  """
  Returns the smallest item in the iterable.
  @note: equivalent to: min(iterable, key)
  """
  return min(iterable, key)


