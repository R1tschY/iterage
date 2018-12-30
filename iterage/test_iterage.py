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


def createNGenerator(n):
  return (x for x in iterage.irange(n))

emptyGenerator = createNGenerator(0)

class IterageDropTests(unittest.TestCase):

  def test_simpleUseCases(self):
    for i in iterage.irange(6):
      exp = [] if i < 3 else list(iterage.irange(3, i))
      self.assertEqual(list(iterage.drop(iterage.irange(i), 3)), exp)
      self.assertEqual(list(iterage.drop(list(iterage.irange(i)), 3)), exp)
      self.assertEqual(list(iterage.drop(createNGenerator(i), 3)), exp)

  def test_emptyRange(self):
    self.assertEqual(list(iterage.drop(iterage.irange(6), 0)), list(iterage.irange(6)))
    self.assertEqual(list(iterage.drop([], 3)), [])
    self.assertEqual(list(iterage.drop([], 0)), [])

class IterageTakeTests(unittest.TestCase):

  def test_simpleUseCases(self):
    for i in iterage.irange(6):
      exp = list(iterage.irange(i)) if i < 3 else list(iterage.irange(3))
      self.assertEqual(list(iterage.take(iterage.irange(i), 3)), exp)
      self.assertEqual(list(iterage.take(list(iterage.irange(i)), 3)), exp)
      self.assertEqual(list(iterage.take(createNGenerator(i), 3)), exp)

  def test_emptyRange(self):
    self.assertEqual(list(iterage.take(iterage.irange(0), 0)), [])
    self.assertEqual(list(iterage.take([], 0)), [])
    self.assertEqual(list(iterage.take(emptyGenerator, 0)), [])

    self.assertEqual(list(iterage.take(iterage.irange(0), 3)), [])
    self.assertEqual(list(iterage.take([], 3)), [])
    self.assertEqual(list(iterage.take(emptyGenerator, 3)), [])

    self.assertEqual(list(iterage.take(iterage.irange(3), 0)), [])
    self.assertEqual(list(iterage.take([0, 1, 2], 0)), [])
    self.assertEqual(list(iterage.take(createNGenerator(3), 0)), [])

class IterageCycleTests(unittest.TestCase):

  def test_simpleUseCases(self):
    self.assertEqual(list(iterage.take(iterage.cycle(iterage.irange(2)), 6)), [0, 1, 0, 1, 0, 1])
    self.assertEqual(list(iterage.take(iterage.cycle([0, 1]), 6)), [0, 1, 0, 1, 0, 1])
    self.assertEqual(list(iterage.take(iterage.cycle(createNGenerator(2)), 6)), [0, 1, 0, 1, 0, 1])


class IterageChunkTests(unittest.TestCase):

  def test_simpleUseCases(self):
    self.assertEqual(list(iterage.chunk(iterage.irange(9), 3)), [(0, 1, 2), (3, 4, 5), (6, 7, 8)])
    self.assertEqual(list(iterage.chunk(iterage.irange(3), 3)), [(0, 1, 2)])
    self.assertEqual(list(iterage.chunk(iter([0, 1, 2]), 3)), [(0, 1, 2)])

  def test_emptyRange(self):
    self.assertEqual(list(iterage.chunk(iterage.irange(0), 3)), [])
    self.assertEqual(list(iterage.chunk((), 3)), [])

  def test_unsuitableRange(self):
    self.assertEqual(list(iterage.chunk(iterage.irange(8), 3)), [(0, 1, 2), (3, 4, 5), (6, 7)])
    self.assertEqual(list(iterage.chunk(iterage.irange(1), 3)), [(0,)])


if __name__ == "__main__":
  suite = unittest.TestLoader().loadTestsFromModule(iterage)
  unittest.TextTestRunner(verbosity=2).run(suite)

