import doctest
from importlib import import_module
import unittest


TEST_MODULES = ("iterage", "iterage.generate", "iterage.reduce")


def runtest():
  suite = unittest.TestSuite()
  for testModule in TEST_MODULES:
    suite.addTest(doctest.DocTestSuite(import_module(testModule)))

  runner = unittest.TextTestRunner(verbosity=2)
  runner.run(suite)


if __name__ == "__main__":
  runtest()
