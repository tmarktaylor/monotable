"""Assertion based test cases for monotable.datacls."""
from dataclasses import dataclass
from typing import Optional
import unittest

import pytest
from monotable import dataclass_format, dataclass_print

unittest_testcase = unittest.TestCase()
unittest_testcase.maxDiff = None

def test_not_a_dataclass():
    """Test example that has field spec=callable on field whose value is dataclass."""
    class A:
        pass
    a = A()
    with pytest.raises(AssertionError):
        dataclass_print(a)
    with pytest.raises(AssertionError):
        text = dataclass_format(a)


def test_revisited_dataclass():
    """Test a dataclass is visited more than once.  Test nested dataclasses."""

    @dataclass
    class A:
        a: int
        link: Optional["A"] = None
        next_value: int = 0

    start = A(1)
    middle = A(2)
    next_to_last = A(3)
    last = A(4)
    start.link = middle
    start.next_value = start.link.a

    middle.link = next_to_last
    middle.next_value = middle.link.a

    next_to_last.link = last
    next_to_last.next_value = next_to_last.link.a

    last.link = start  # This link creates a cycle
    last.next_value = last.link.a

    text = dataclass_format(start)
    # Look for the '...' for link in the bottom table.
    expected = """\
      A
-------------
a           1
link        A
next_value  2
-------------

    A.link : A
  -------------
  a           2
  link        A
  next_value  3
  -------------

    A.link.link : A
    -------------
    a           3
    link        A
    next_value  4
    -------------

      A.link.link.link : A
      -----------------
      a               4
      link        A ...
      next_value      1
      -----------------"""
    unittest_testcase.assertEqual(expected, text)


