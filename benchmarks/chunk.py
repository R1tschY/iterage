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

import itertools

import benchmarks as bench


def baseline(iterable, n):
  a = []
  try:
    iterators = iter(iterable)
    while True:
      a = []
      for _ in range(n):
        a.append(next(iterators))
      yield a

  except StopIteration:
    if len(a) > 0:
      yield a

def chunk_v1(iterable, n):
  islice = itertools.islice
  ltuple = tuple
  llen = len

  iterator = iter(iterable)
  while True:
    a = ltuple(islice(iterator, n))
    if llen(a) == n:
      yield a
    else:
      if llen(a) > 0:
        yield a
      return

def chunk_v2(iterable, n):
  islice = itertools.islice
  ltuple = tuple
  
  it = iter(iterable)
  item = ltuple(islice(it, n))
  while item:
      yield item
      item = ltuple(islice(it, n))

def chunk_v3(iterable, n):
    it = iter(iterable)
    ltuple = tuple
    islice = itertools.islice
    return iter(lambda: ltuple(islice(it, n)), ())

def chunk_v4(iterable, n):
    iterable = iter(iterable)
    ltuple = tuple
    islice = itertools.islice
    while True:
        yield ltuple(islice(iterable, n)) or next(iterable)

def chunk_v5(iterable, n):
  iterator = iter(iterable)
  ltuple = tuple
  llen = len
  islice = itertools.islice
  while True:
    a = ltuple(islice(iterator, n))
    if llen(a) == n:
      yield a
    else:
      if llen(a) > 0:
        yield a
      return

def grouper(iterable, n):
  args = [iter(iterable)] * n
  return zip(*args)

class ChunkBenchmark(bench.BenchmarkBase):
    def __base(self):
      return super(ChunkBenchmark, self)

    def __init__(self):
      self.__base().__init__()

      self.registerTests([
        ('baseline', (
            'import iterage.benchmarks.chunk',
            'list(iterage.benchmarks.chunk.baseline({iterable}, {n}))'
          )),

          ('iterage', (
            'import iterage',
            'list(iterage.chunk({iterable}, {n}))'
          )),

          ('iterage v1', (
            'import iterage.benchmarks.chunk',
            'list(iterage.benchmarks.chunk.chunk_v1({iterable}, {n}))'
          )),

          ('iterage v2', (
            'import iterage.benchmarks.chunk',
            'list(iterage.benchmarks.chunk.chunk_v2({iterable}, {n}))'
          )),

          ('iterage v3', (
            'import iterage.benchmarks.chunk',
            'list(iterage.benchmarks.chunk.chunk_v3({iterable}, {n}))'
          )),

          ('iterage v4', (
            'import iterage.benchmarks.chunk',
            'list(iterage.benchmarks.chunk.chunk_v4({iterable}, {n}))'
          )),
                          
          ('iterage v5', (
            'import iterage.benchmarks.chunk',
            'list(iterage.benchmarks.chunk.chunk_v5({iterable}, {n}))'
          )),                          
#
#           ('chunk_filled', (
#             'import iterage',
#             'list(iterage.chunk_filled({iterable}, {n}))'
#           )),
#
#           ('chunk_trunc', (
#             'import iterage',
#             'list(iterage.chunk_trunc({iterable}, {n}))'
#           )),
      ])

    def run(self):
      self._run(args={'iterable': '(str(x) for x in xrange(1, 8))', 'n': 4}, number=10000);
      self._run(args={'iterable': '(str(x) for x in xrange(1, 64))', 'n': 4}, number=1000);
      self._run(args={'iterable': '(str(x) for x in xrange(1, 128))', 'n': 4}, number=100);

      self._run(args={'iterable': 'xrange(1, 7)', 'n': 8}, number=100000);
      self._run(args={'iterable': 'xrange(1, 63)', 'n': 8}, number=10000);
      self._run(args={'iterable': 'xrange(1, 511)', 'n': 8}, number=1000);
      self._run(args={'iterable': 'xrange(1, 4095)', 'n': 8}, number=100);


if __name__ == "__main__":
  benchmark = ChunkBenchmark()
  benchmark.run()
