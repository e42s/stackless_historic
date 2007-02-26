#!/usr/bin/env python

"""Unit tests for the keyword only argument specified in PEP 3102."""

__author__ = "Jiwon Seo"
__email__ = "seojiwon at gmail dot com"

import unittest
from test.test_support import run_unittest

def posonly_sum(pos_arg1, *arg, **kwarg):
    return pos_arg1 + sum(arg) + sum(kwarg.values())
def keywordonly_sum(*, k1=0, k2):
    return k1 + k2
def keywordonly_nodefaults_sum(*, k1, k2):
    return k1 + k2
def keywordonly_and_kwarg_sum(*, k1, k2, **kwarg):
    return k1 + k2 + sum(kwarg.values())
def mixedargs_sum(a, b=0, *arg, k1, k2=0):
    return a + b + k1 + k2 + sum(arg)
def mixedargs_sum2(a, b=0, *arg, k1, k2=0, **kwargs):
    return a + b + k1 + k2 + sum(arg) + sum(kwargs.values())

def sortnum(*nums, reverse=False):
    return sorted(list(nums), reverse=reverse)

def sortwords(*words, reverse=False, **kwargs):
    return sorted(list(words), reverse=reverse)

class Foo:
    def __init__(self, *, k1, k2=0):
        self.k1 = k1
        self.k2 = k2
    def set(self, p1, *, k1, k2):
        self.k1 = k1
        self.k2 = k2
    def sum(self):
        return self.k1 + self.k2

class KeywordOnlyArgTestCase(unittest.TestCase):
    def assertRaisesSyntaxError(self, codestr):
        def shouldRaiseSyntaxError(s):
            compile(s, "<test>", "single")
        self.assertRaises(SyntaxError, shouldRaiseSyntaxError, codestr)

    def testSyntaxErrorForFunctionDefinition(self):
        self.assertRaisesSyntaxError("def f(p, *):\n  pass\n")
        self.assertRaisesSyntaxError("def f(p1, *, p1=100):\n  pass\n")
        self.assertRaisesSyntaxError("def f(p1, *k1, k1=100):\n  pass\n")
        self.assertRaisesSyntaxError("def f(p1, *, k1, k1=100):\n  pass\n")
        self.assertRaisesSyntaxError("def f(p1, *, k1, **k1):\n  pass\n")
        self.assertRaisesSyntaxError("def f(p1, *, None, **k1):\n  pass\n")
        self.assertRaisesSyntaxError("def f(p, *, (k1, k2), **kw):\n  pass\n")

    def testSyntaxForManyArguments(self):
        fundef = "def f("
        for i in range(255):
            fundef += "i%d, "%i
        fundef += "*, key=100):\n pass\n"
        self.assertRaisesSyntaxError(fundef)

        fundef2 = "def foo(i,*,"
        for i in range(255):
            fundef2 += "i%d, "%i
        fundef2 += "lastarg):\n  pass\n"
        self.assertRaisesSyntaxError(fundef2)

        # exactly 255 arguments, should compile ok
        fundef3 = "def f(i,*,"
        for i in range(253):
            fundef3 += "i%d, "%i
        fundef3 += "lastarg):\n  pass\n"
        compile(fundef3, "<test>", "single")
 
    def testSyntaxErrorForFunctionCall(self):
        self.assertRaisesSyntaxError("f(p, k=1, p2)")
        self.assertRaisesSyntaxError("f(p, *(1,2), k1=100)")

    def testRaiseErrorFuncallWithUnexpectedKeywordArgument(self):
        self.assertRaises(TypeError, keywordonly_sum, ())
        self.assertRaises(TypeError, keywordonly_nodefaults_sum, ())
        self.assertRaises(TypeError, Foo, ())
        try:
            keywordonly_sum(k2=100, non_existing_arg=200)
            self.fail("should raise TypeError")
        except TypeError:
            pass
        try:
            keywordonly_nodefaults_sum(k2=2)
            self.fail("should raise TypeError")
        except TypeError:
            pass

    def testFunctionCall(self):
        self.assertEquals(1, posonly_sum(1))
        self.assertEquals(1+2, posonly_sum(1,**{"2":2}))
        self.assertEquals(1+2+3, posonly_sum(1,*(2,3)))
        self.assertEquals(1+2+3+4, posonly_sum(1,*(2,3),**{"4":4}))

        self.assertEquals(1, keywordonly_sum(k2=1))
        self.assertEquals(1+2, keywordonly_sum(k1=1, k2=2))

        self.assertEquals(1+2, keywordonly_and_kwarg_sum(k1=1, k2=2))
        self.assertEquals(1+2+3, keywordonly_and_kwarg_sum(k1=1, k2=2, k3=3))
        self.assertEquals(1+2+3+4,
                          keywordonly_and_kwarg_sum(k1=1, k2=2,
                                                    **{"a":3,"b":4}))

        self.assertEquals(1+2, mixedargs_sum(1, k1=2))
        self.assertEquals(1+2+3, mixedargs_sum(1, 2, k1=3))
        self.assertEquals(1+2+3+4, mixedargs_sum(1, 2, k1=3, k2=4))
        self.assertEquals(1+2+3+4+5, mixedargs_sum(1, 2, 3, k1=4, k2=5))

        self.assertEquals(1+2, mixedargs_sum2(1, k1=2))
        self.assertEquals(1+2+3, mixedargs_sum2(1, 2, k1=3))
        self.assertEquals(1+2+3+4, mixedargs_sum2(1, 2, k1=3, k2=4))
        self.assertEquals(1+2+3+4+5, mixedargs_sum2(1, 2, 3, k1=4, k2=5))
        self.assertEquals(1+2+3+4+5+6,
                          mixedargs_sum2(1, 2, 3, k1=4, k2=5, k3=6))
        self.assertEquals(1+2+3+4+5+6,
                          mixedargs_sum2(1, 2, 3, k1=4, **{'k2':5, 'k3':6}))

        self.assertEquals(1, Foo(k1=1).sum())
        self.assertEquals(1+2, Foo(k1=1,k2=2).sum())

        self.assertEquals([1,2,3], sortnum(3,2,1))
        self.assertEquals([3,2,1], sortnum(1,2,3, reverse=True))

        self.assertEquals(['a','b','c'], sortwords('a','c','b'))
        self.assertEquals(['c','b','a'], sortwords('a','c','b', reverse=True))
        self.assertEquals(['c','b','a'],
                          sortwords('a','c','b', reverse=True, ignore='ignore'))

    def testKwDefaults(self):
        def foo(p1,p2=0, *, k1, k2=0):
            return p1 + p2 + k1 + k2

        self.assertEquals(2, foo.__code__.co_kwonlyargcount)
        self.assertEquals({"k2":0}, foo.__kwdefaults__)
        foo.__kwdefaults__ = {"k1":0}
        try:
            foo(1,k1=10)
            self.fail("__kwdefaults__ is not properly changed")
        except TypeError:
            pass

def test_main():
    run_unittest(KeywordOnlyArgTestCase)

if __name__ == "__main__":
    test_main()