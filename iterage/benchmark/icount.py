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

def baseline(iterable):
  return sum(1 for __ in iterable)

def icount_v1(iterable):
  """
  copyied from zuo: http://stackoverflow.com/a/15112059/1188453
  """
  counter = itertools.count()
  deque(itertools.izip(iterable, itertools.count()), maxlen=0)
  return next(counter)

def icount_v2(iterable):
  """
  copied from cardinality library

  Copyright © 2015, Wouter Bolsterlee

  All rights reserved.

  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.
    * Neither the name of the author nor the names of its contributors may be
      used to endorse or promote products derived from this software without
      specific prior written permission.

  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS”
  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
  SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
  OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
  """

  d = deque(enumerate(iterable, 1), maxlen=1)
  return d[0][0] if d else 0

class ICountBenchmark(bench.BenchmarkBase):
  def __init__(self):
    super(ICountBenchmark, self).__init__()

    self.registerTests([
      ("baseline", (
        'import iterage.benchmark.icount',
        'iterage.benchmark.icount.baseline({iterable})'
      )),

      ("v1", (
        'import iterage.benchmark.icount',
        'iterage.benchmark.icount.icount_v1({iterable})'
      )),

      ("cardinality", (
        'import iterage.benchmark.icount',
        'iterage.benchmark.icount.icount_v2({iterable})'
      )),
    ])

  def run(self):
    self._run(args={'iterable': 'xrange(1, 8)'}, number=100000)
    self._run(args={'iterable': 'xrange(1, 64)'}, number=10000)
    self._run(args={'iterable': 'xrange(1, 512)'}, number=1000)
    self._run(args={'iterable': 'xrange(1, 4096)'}, number=100)

    self._run(args={'iterable': '(x for x in xrange(8))'}, number=100000)
    self._run(args={'iterable': '(x for x in xrange(64))'}, number=10000)
    self._run(args={'iterable': '(x for x in xrange(8) if x > 4)'}, number=100000)
    self._run(args={'iterable': '(x for x in xrange(64) if x > 100)'}, number=10000)


if __name__ == "__main__":
  benchmark = ICountBenchmark()
  benchmark.run()
