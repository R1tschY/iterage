# -*- coding=utf-8 -*-

import unittest

from itr import itr


class ItrTests(unittest.TestCase):

    def test_iter(self):
        self.assertEqual(list(itr([1, 2])), [1, 2])
        self.assertEqual([i for i in itr([1, 2])], [1, 2])

        self.assertEqual(list(itr(iter([1, 2]))), [1, 2])
        self.assertEqual(list(itr(range(1, 3))), [1, 2])

    def test_take(self):
        self.assertEqual(list(itr([1, 2]).take(0)), [])
        self.assertEqual(list(itr([1, 2]).take(1)), [1])
        self.assertEqual(list(itr([1, 2]).take(2)), [1, 2])
        self.assertEqual(list(itr([1, 2]).take(3)), [1, 2])

        with self.assertRaises(ValueError):
            itr([1, 2]).take(-1)
        with self.assertRaises(ValueError):
            itr([1, 2]).take("1")

    def test_drop(self):
        self.assertEqual(list(itr([1, 2]).drop(0)), [1, 2])
        self.assertEqual(list(itr([1, 2]).drop(1)), [2])
        self.assertEqual(list(itr([1, 2]).drop(2)), [])
        self.assertEqual(list(itr([1, 2]).drop(3)), [])

        with self.assertRaises(ValueError):
            itr([1, 2]).take(-1)
        with self.assertRaises(ValueError):
            itr([1, 2]).take("1")
