# -*- coding=utf-8 -*-
import base64
import uuid
from collections import Callable
import operator
from functools import reduce

from typing import Any, Dict, Optional


def const(c):
    def fn(*_args):
        return c
    return fn


class ExprFn:
    __slots__ = ("_exprfn_",)

    _exprfn_: Callable

    def __init__(self, fn: Callable):
        self._exprfn_ = fn

    @classmethod
    def _binop_helper(cls, a, b, op):
        if isinstance(a, ExprFn) and isinstance(b, ExprFn):
            fn = a._exprfn_
            ofn = b._exprfn_

            def result_fn(*args):
                return op(fn(*args), ofn(*args))

        elif isinstance(a, ExprFn):
            fn = a._exprfn_

            def result_fn(*args):
                return op(fn(*args), b)

        elif isinstance(b, ExprFn):
            fn = b._exprfn_

            def result_fn(*args):
                return op(a, fn(*args))

        else:
            assert False

        return cls(result_fn)

    def __call__(self, *args) -> "ExprFn":
        argfns = [
            arg._exprfn_ if isinstance(arg, ExprFn) else const(arg)
            for arg in args
        ]

        fn = self._exprfn_

        def result_fn(*aargs):
            return fn(*[argfn(*aargs) for argfn in argfns])

        return ExprFn(result_fn)

    def __eq__(self, other) -> "ExprFn":
        return self._binop_helper(self, other, operator.eq)

    def __add__(self, other) -> "ExprFn":
        return self._binop_helper(self, other, operator.add)

    def __radd__(self, other) -> "ExprFn":
        return self._binop_helper(other, self, operator.add)

    def __sub__(self, other) -> "ExprFn":
        return self._binop_helper(self, other, operator.sub)

    def __rsub__(self, other) -> "ExprFn":
        return self._binop_helper(other, self, operator.sub)

    def __mul__(self, other) -> "ExprFn":
        return self._binop_helper(self, other, operator.mul)

    def __rmul__(self, other) -> "ExprFn":
        return self._binop_helper(other, self, operator.mul)

    def __truediv__(self, other) -> "ExprFn":
        return self._binop_helper(self, other, operator.truediv)

    def __rtruediv__(self, other) -> "ExprFn":
        return self._binop_helper(other, self, operator.truediv)

    def __floordiv__(self, other) -> "ExprFn":
        return self._binop_helper(self, other, operator.floordiv)

    def __rfloordiv__(self, other) -> "ExprFn":
        return self._binop_helper(other, self, operator.floordiv)

    def __divmod__(self, other) -> "ExprFn":
        return self._binop_helper(self, other, operator.mod)

    def __rdivmod__(self, other) -> "ExprFn":
        return self._binop_helper(other, self, operator.mod)

    def __xor__(self, other) -> "ExprFn":
        return self._binop_helper(self, other, operator.xor)

    def __rxor__(self, other) -> "ExprFn":
        return self._binop_helper(other, self, operator.xor)

    def __getattr__(self, item: str) -> "ExprFn":
        if item.startswith("_"):
            raise AttributeError()

        fn = self._exprfn_

        def result_fn(*args):
            return getattr(fn(*args), item)

        return self.__class__(result_fn)

    def __getitem__(self, item: Any) -> "ExprFn":
        fn = self._exprfn_

        def result_fn(*args):
            return fn(*args)[item]

        return self.__class__(result_fn)

    # __contains__ not possible -> must always return a bool


class ExprFn1(ExprFn):
    def __getattr__(self, item: str) -> "ExprFn":
        if item.startswith("_"):
            raise AttributeError()

        if self is _:
            return self.__class__(operator.attrgetter(item))

        fn = self._exprfn_

        def result_fn(a):
            return getattr(fn(a), item)

        return self.__class__(result_fn)

    def __getitem__(self, item: Any) -> "ExprFn":
        fn = self._exprfn_

        def result_fn(a):
            return fn(a)[item]

        return self.__class__(result_fn)

    @classmethod
    def _binop_helper(cls, a, b, op):
        if isinstance(a, ExprFn) and isinstance(b, ExprFn):
            fn = a._exprfn_
            ofn = b._exprfn_

            if a is _ and b is _:
                def result_fn(x):
                    return op(x, x)
            else:
                def result_fn(x):
                    return op(fn(x), ofn(x))

        elif isinstance(a, ExprFn):
            fn = a._exprfn_

            if a is _:
                # TODO: partial?
                def result_fn(x):
                    return op(x, b)
            else:
                def result_fn(x):
                    return op(fn(x), b)

        elif isinstance(b, ExprFn):
            fn = b._exprfn_

            if b is _:
                # TODO: partial?
                def result_fn(x):
                    return op(a, x)
            else:
                def result_fn(x):
                    return op(a, fn(x))
        else:
            assert False

        return cls(result_fn)


class ExprFn2(ExprFn):

    @classmethod
    def _binop_helper(cls, a, b, op) -> "ExprFn2":
        if a is _1 and b is _2:
            return cls(op)

        return super()._binop_helper(a, b, op)


def isin(item, container):
    cls = None

    if hasattr(item, "_exprfn_"):
        itemfn = item._exprfn_
        cls = item.__class__
    else:
        itemfn = const(item)

    if hasattr(container, "_exprfn_"):
        containerfn = container._exprfn_

        if cls is not None:
            raise ValueError(
                f"Missmatching expr classes: "
                f"{cls.__name__} != {container.__class__.__name__}")

        cls = container.__class__
    else:
        containerfn = const(item)

    if cls is None:
        raise ValueError("No expr object as item or container")

    def result_fn(*args):
        return itemfn(*args) in containerfn(*args)
    return cls(result_fn)


def λ(fn: ExprFn) -> Callable:
    return fn._exprfn_


def fn(fn: ExprFn) -> Callable:
    return fn._exprfn_


@ExprFn1
def _(_):
    return _


@ExprFn2
def _1(_1, _2):
    return _1


@ExprFn2
def _2(_1, _2):
    return _2



def test_args():
    assert fn(_)(1) == 1
    assert fn(_1)(1, 2) == 1
    assert fn(_2)(1, 2) == 2


def test_eq():
    assert λ(_ == 42)(42) is True
    assert λ(_ == 42)(43) is False

    assert λ(_1 == _2)(42, 42) is True
    assert λ(_1 == _2)(42, 43) is False


def test_isin():
    assert λ(isin(42, _))([42]) is True
    assert λ(isin(43, _))([43]) is False


def test_attr():
    class A:
        value = 42

    a = A()

    assert _.value(a) == 42


def test_map():
    t = [1, 2, 3]

    assert list(map(λ(_ * 2 + 1), t)) == [3, 5, 7]


def test_sort():
    t = [3, 2, 1]

    assert sorted(t, key=λ(_)) == [1, 2, 3]
    assert sorted(t, key=λ(_ * 2)) == [1, 2, 3]


def test_reduce():
    t = [3, 2, 1]

    assert reduce(λ(_1 * _2), t, 1) == 6
