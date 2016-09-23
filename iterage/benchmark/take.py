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


def takebaseline(i, n):
  it = iter(i)
  for _ in itertools.repeat(None, n):
    yield next(it)

class TakeBenchmark(bench.BenchmarkBase):
    def __base(self):
      return super(TakeBenchmark, self)

    def __init__(self):
      self.__base().__init__()
      self.register('baseline', self.baseline)
      self.register('baseline2', self.baseline2)
      self.register('iterage', self.test1)
      self.register('itertools', self.testbuildin)

    def baseline(self, args):
      return timeit.Timer(
        setup='from iterage.benchmark.take import takebaseline',
        stmt='list(takebaseline({iterable}, {n}))'.format(**args))

    def baseline2(self, args):
      return timeit.Timer(
        setup='from iterage.benchmark.take import takebaseline2',
        stmt='list(takebaseline2({iterable}, {n}))'.format(**args))

    def test1(self, args):
      return timeit.Timer(
        setup='import iterage',
        stmt='list(iterage.take({iterable}, {n}))'.format(**args))

    def testbuildin(self, args):
      return timeit.Timer(
        setup='import itertools',
        stmt='list(itertools.islice({iterable}, {n}))'.format(**args))

    def run(self):
      self.__base().run(
        args={'iterable': 'xrange(1000)', 'n': 1000 - 1},
        number=100)


if __name__ == "__main__":
  benchmark = TakeBenchmark()
  benchmark.run()
  benchmark.pnt()
