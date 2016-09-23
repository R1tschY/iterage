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
import unittest

import iterage


class IterageTakeTests(unittest.TestCase):

  def test_simpleUseCases(self):
    self.assertEqual(list(iterage.take(range(6), 3)), [0, 1, 2])

  def test_emptyRange(self):
    self.assertEqual(list(iterage.take(range(0), 3)), [])

  def test_smallRange(self):
    self.assertEqual(list(iterage.take(range(2), 3)), [0, 1])

class IterageChunkTests(unittest.TestCase):

  def test_simpleUseCases(self):
    self.assertEqual(list(iterage.chunk(range(9), 3)), [(0, 1, 2), (3, 4, 5), (6, 7, 8)])
    self.assertEqual(list(iterage.chunk(range(3), 3)), [(0, 1, 2)])

  def test_emptyRange(self):
    self.assertEqual(list(iterage.chunk(range(0), 3)), [])

  def test_unsuitableRange(self):
    self.assertEqual(list(iterage.chunk(range(8), 3)), [(0, 1, 2), (3, 4, 5), (6, 7)])
    self.assertEqual(list(iterage.chunk(range(1), 3)), [(0,)])


if __name__ == "__main__":
  suite = unittest.TestLoader().loadTestsFromModule(iterage)
  unittest.TextTestRunner(verbosity=2).run(suite)

