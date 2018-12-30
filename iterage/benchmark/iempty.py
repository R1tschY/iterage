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

import iterage.benchmark as bench
import iterage.reduce

SENTINEL = object()

def baseline(iterable):
  return iterage.reduce.icount(iterable) > 0

def v1(iterable):
  try:
    next(iter(iterable))
    return False
  except StopIteration:
    return True

def v2(iterable):
  return next(iter(iterable), SENTINEL) is SENTINEL

def v3(iterable):
  _SENTINEL = object()
  return next(iter(iterable), _SENTINEL) is _SENTINEL

def v4(iterable):
  _SENTINEL = SENTINEL
  return next(iter(iterable), _SENTINEL) is _SENTINEL

class ICountIfBenchmark(bench.BenchmarkBase):
  def __init__(self):
    super(ICountIfBenchmark, self).__init__()

    self.registerTests([
      ("baseline", (
        'import iterage.benchmark.iempty',
        'iterage.benchmark.iempty.baseline({iterable})'
      )),

      ("v1", (
        'import iterage.benchmark.iempty',
        'iterage.benchmark.iempty.v1({iterable})'
      )),

      ("v2", (
        'import iterage.benchmark.iempty',
        'iterage.benchmark.iempty.v2({iterable})'
      )),

                            ("v3", (
        'import iterage.benchmark.iempty',
        'iterage.benchmark.iempty.v3({iterable})'
      )),

                              ("v4", (
        'import iterage.benchmark.iempty',
        'iterage.benchmark.iempty.v4({iterable})'
      )),
    ])

  def run(self):
    self._run(args={'iterable': '(x for x in xrange(8))'}, number=100000)
    self._run(args={'iterable': '(x for x in xrange(64))'}, number=10000)
    self._run(args={'iterable': '(x > 4 for x in xrange(8))'}, number=100000)
    self._run(args={'iterable': '(x > 32 for x in xrange(64))'}, number=10000)
    self._run(args={'iterable': '(x > 100 for x in xrange(64))'}, number=10000)
    self._run(args={'iterable': 'xrange(0)'}, number=10000)
    self._run(args={'iterable': 'xrange(5)'}, number=10000)
    self._run(args={'iterable': '[]'}, number=10000)
    self._run(args={'iterable': '[1,2,3,4]'}, number=10000)


if __name__ == "__main__":
  benchmark = ICountIfBenchmark()
  benchmark.run()
