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

import iterage.benchmark as bench
import iterage.reduce


def baseline(iterable):
  lbool = bool
  return sum(lbool(x) for x in iterable)

def icount_if_v1(iterable):
  return sum(itertools.imap(bool, iterable))

def icount_if_v2(iterable):
  lbool = bool
  return iterage.reduce.icount(x for x in iterable if lbool(x))

def icount_if_v3(iterable):
  return iterage.reduce.icount(itertools.ifilter(bool, iterable))

def icount_if_v4(iterable, sum=sum):
  return sum(1 for x in iterable if x)

class IEmptyBenchmark(bench.BenchmarkBase):
  def __init__(self):
    super(IEmptyBenchmark, self).__init__()

    self.registerTests([
      ("baseline", (
        'import iterage.benchmark.icount_if',
        'iterage.benchmark.icount_if.baseline({iterable})'
      )),

      ("v1", (
        'import iterage.benchmark.icount_if',
        'iterage.benchmark.icount_if.icount_if_v1({iterable})'
      )),

      ("v2", (
        'import iterage.benchmark.icount_if',
        'iterage.benchmark.icount_if.icount_if_v2({iterable})'
      )),

      ("v3", (
        'import iterage.benchmark.icount_if',
        'iterage.benchmark.icount_if.icount_if_v3({iterable})'
      )),

      ("v4", (
        'import iterage.benchmark.icount_if',
        'iterage.benchmark.icount_if.icount_if_v4({iterable})'
      )),
    ])

  def run(self):
    self._run(args={'iterable': '(x for x in xrange(8))'}, number=100000)
    self._run(args={'iterable': '(x for x in xrange(64))'}, number=10000)
    self._run(args={'iterable': '(x > 4 for x in xrange(8))'}, number=100000)
    self._run(args={'iterable': '(x > 32 for x in xrange(64))'}, number=10000)
    self._run(args={'iterable': '(x > 100 for x in xrange(64))'}, number=10000)
    self._run(args={'iterable': '(x % 2 for x in xrange(8))'}, number=10000)
    self._run(args={'iterable': '(x % 2 for x in xrange(64))'}, number=10000)
    self._run(args={'iterable': '(x % 2 for x in xrange(128))'}, number=1000)
    self._run(args={'iterable': '(x % 2 for x in xrange(1024))'}, number=100)


if __name__ == "__main__":
  benchmark = IEmptyBenchmark()
  benchmark.run()
