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
import iterage.reduce


def baseline(iterable, pred=bool):
  for e in iterable:
    if not pred(e):
      return False
  return True

def iall_v3(iterable, pred=bool):
  if pred == bool:
    return all(iterable)

  for e in iterable:
    if not pred(e):
      return False
  return True

def iall_v2(iterable, pred=bool):
  if pred == bool:
    return all(iterable)
  else:
    return iterage.reduce.is_empty(itertools.ifilterfalse(pred, iterable))

class IAllBenchmark(bench.BenchmarkBase):
    def __base(self):
      return super(IAllBenchmark, self)

    def __init__(self):
      self.__base().__init__()
      self.register('baseline', self.baseline)
      self.register('iterage', self.testiterage)
      self.register('iterage v2', self.testiteragev2)
      self.register('iterage v3', self.testiteragev3)

    def baseline(self, args):
      return timeit.Timer(\
        setup='import iterage.benchmark.iall',
        stmt='iterage.benchmark.iall.baseline({iterable}, pred={pred})'.format(**args))

    def testiterage(self, args):
      return timeit.Timer(
        setup='import iterage.reduce',
        stmt='iterage.reduce.iall({iterable}, pred={pred})'.format(**args))

    def testiteragev2(self, args):
      return timeit.Timer(\
        setup='import iterage.benchmark.iall',
        stmt='iterage.benchmark.iall.iall_v2({iterable}, pred={pred})'.format(**args))

    def testiteragev3(self, args):
      return timeit.Timer(\
        setup='import iterage.benchmark.iall',
        stmt='iterage.benchmark.iall.iall_v2({iterable}, pred={pred})'.format(**args))

    def run(self):
      self.__base().run(args={'iterable': 'xrange(1, 8)', 'pred': 'bool'}, number=100000); self.pnt(); print('')
      self.__base().run(args={'iterable': 'xrange(1, 64)', 'pred': 'bool'}, number=10000); self.pnt(); print('')
      self.__base().run(args={'iterable': 'xrange(1, 512)', 'pred': 'bool'}, number=1000); self.pnt(); print('')
      self.__base().run(args={'iterable': 'xrange(1, 4096)', 'pred': 'bool'}, number=100); self.pnt(); print('')

      self.__base().run(args={'iterable': 'xrange(-8, 1)', 'pred': 'lambda x: x != 0'}, number=100000); self.pnt(); print('')
      self.__base().run(args={'iterable': 'xrange(-64, 1)', 'pred': 'lambda x: x != 0'}, number=10000); self.pnt(); print('')
      self.__base().run(args={'iterable': 'xrange(-512, 1)', 'pred': 'lambda x: x != 0'}, number=1000); self.pnt(); print('')
      self.__base().run(args={'iterable': 'xrange(-4096, 1)', 'pred': 'lambda x: x != 0'}, number=100); self.pnt(); print('')


if __name__ == "__main__":
  benchmark = IAllBenchmark()
  benchmark.run()
