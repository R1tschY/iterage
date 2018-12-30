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

import math
# from tabulate import tabulate
import timeit


si_scaler = ['n', 'p', 'u', 'm', '', 'k', 'M', 'G', 'T', 'P']
def humanize(x):
  exp3 = int(math.log(x, 1000)) - 1
  quotient = float(x) / 1000 ** exp3
  unit = si_scaler[exp3 + 4]
  return '{:5.2f}{}'.format(quotient, unit)

class TestFactory(object):
  def __init__(self, setup, stmt):
    self.setup = setup
    self.stmt = stmt

  def __call__(self, args):
    return timeit.Timer(setup=self.setup, stmt=self.stmt.format(**args))

class BenchmarkBase(object):

  def __init__(self):
    self.funcs = []
    self.results = []
    self.headers = ["Name", "Executions", "Time / Execution"]

  def register(self, name, factory):
    self.funcs.append((name, factory))

  def registerTests(self, tests):
    for k, v in tests:
      self.register(k, TestFactory(v[0], v[1]))

  def run(self, args=None, number=1000000, repeat=3):
    self.results = []
    for (name, factory) in self.funcs:
      func = factory(args)
      if func:
        time = min(func.repeat(repeat=repeat, number=number))
        self.results.append((name, number, humanize(time / number) + 's'))

  def _run(self, args=None, number=1000000, repeat=3):
    self.results = []
    for (name, factory) in self.funcs:
      func = factory(args)
      if func:
        time = min(func.repeat(repeat=repeat, number=number))
        self.results.append((name, number, humanize(time / number) + 's'))

    print("\n".join(map(str, self.results)))
    # print(tabulate(self.results, headers=self.headers))
    print('')

  def pnt(self):
    print("\n".join(self.results))
    # print(tabulate(self.results, headers=self.headers))
    print('')
