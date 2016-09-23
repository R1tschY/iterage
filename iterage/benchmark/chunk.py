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
import timeit

import iterage.benchmark as bench


def baseline(iterable, n):
  a = []
  try:
    iterators = iter(iterable)
    while True:
      a = []
      for _ in xrange(n):
        a.append(next(iterators))
      yield a

  except StopIteration:
    if len(a) > 0:
      yield a

def chunk_v1(iterable, n):
  iterator = iter(iterable)
  while True:
    a = list(itertools.islice(iterator, n))
    if len(a) == n:
      yield a
    else:
      if len(a) > 0:
        yield a
      return

def grouper(iterable, n):
  args = [iter(iterable)] * n
  return itertools.izip(*args)

class ChunkBenchmark(bench.BenchmarkBase):
    def __base(self):
      return super(ChunkBenchmark, self)

    def __init__(self):
      self.__base().__init__()
      self.register('baseline', self.baseline)
      self.register('iterage', self.testiterage)
      self.register('iterage v1', self.chunk_v1)
      self.register('chunk_filled', self.chunk_filled)
      self.register('chunk_trunc', self.chunk_trunc)

    def baseline(self, args):
      return timeit.Timer(\
        setup='import iterage.benchmark.chunk',
        stmt='list(iterage.benchmark.chunk.baseline({iterable}, {n}))'.format(**args))

    def testiterage(self, args):
      return timeit.Timer(
        setup='import iterage',
        stmt='list(iterage.chunk({iterable}, {n}))'.format(**args))

    def chunk_v1(self, args):
      return timeit.Timer(\
        setup='import iterage.benchmark.chunk',
        stmt='list(iterage.benchmark.chunk.chunk_v1({iterable}, {n}))'.format(**args))

    def chunk_filled(self, args):
      return timeit.Timer(
        setup='import iterage',
        stmt='list(iterage.chunk_filled({iterable}, {n}))'.format(**args))

    def chunk_trunc(self, args):
      return timeit.Timer(
        setup='import iterage',
        stmt='list(iterage.chunk_trunc({iterable}, {n}))'.format(**args))

    def run(self):
      self.__base().run(args={'iterable': 'xrange(1, 8)', 'n': 4}, number=100000); self.pnt(); print('')
      self.__base().run(args={'iterable': 'xrange(1, 64)', 'n': 4}, number=10000); self.pnt(); print('')
      self.__base().run(args={'iterable': 'xrange(1, 512)', 'n': 4}, number=1000); self.pnt(); print('')
      self.__base().run(args={'iterable': 'xrange(1, 4096)', 'n': 4}, number=100); self.pnt(); print('')

      self.__base().run(args={'iterable': 'xrange(1, 8)', 'n': 8}, number=100000); self.pnt(); print('')
      self.__base().run(args={'iterable': 'xrange(1, 64)', 'n': 8}, number=10000); self.pnt(); print('')
      self.__base().run(args={'iterable': 'xrange(1, 512)', 'n': 8}, number=1000); self.pnt(); print('')
      self.__base().run(args={'iterable': 'xrange(1, 4096)', 'n': 8}, number=100); self.pnt(); print('')


if __name__ == "__main__":
  benchmark = ChunkBenchmark()
  benchmark.run()
