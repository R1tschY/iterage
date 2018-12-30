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

import timeit

import iterage
import benchmarks as bench


def baselinerepeat(obj, times=None):
  if times is None:
    while True:
      yield obj
  else:
    for _ in iterage.ntimes(times):
      yield obj

class RepeatBenchmark(bench.BenchmarkBase):
    def __base(self):
      return super(RepeatBenchmark, self)

    def __init__(self):
      self.__base().__init__()
      self.register('baseline', self.baseline)
      self.register('iterage', self.testiterage)
      self.register('itertools', self.testitertools)
      self.register('[e] * n', self.teststar)

    def baseline(self, args):
      return timeit.Timer(\
        setup='import iterage.benchmarks.repeat',
        stmt='list(iterage.benchmarks.repeat.baselinerepeat({element}, {n}))'.format(**args))

    def testiterage(self, args):
      return timeit.Timer(
        setup='import iterage',
        stmt='list(iterage.repeat({element}, {n}))'.format(**args))

    def testitertools(self, args):
      return timeit.Timer(
        setup='import itertools',
        stmt='list(itertools.repeat({element}, {n}))'.format(**args))

    def teststar(self, args):
      return timeit.Timer(
        setup='pass',
        stmt='list([{element}] * {n})'.format(**args))

    def run(self):
      self.__base().run(
        args={'element': 42, 'n': 1000},
        number=100)


if __name__ == "__main__":
  benchmark = RepeatBenchmark()
  benchmark.run()
  benchmark.pnt()
