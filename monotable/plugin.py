# Copyright 2017 Mark Taylor
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This file is part of Project monotable.

"""Format functions and exception callback used by class MonoTable.

All of the format functions are used by MonoTable.
Any of the functions can be configured into a subclass of
MonoTable as the default format function or format error exception callback
function.

   Functions:
   mformat    Format function adapter of a mapping to str.format().
   pformat    Format function adapter to % operator.
   sformat    Format function adapter to str.format().
   tformat    Format function adapter to Template.substitute().
   raise_it   Formatting error callback.  Exception is raised.
   print_it   Formatting error callback.  Exception is printed.
   ignore_it  Formatting error callback.  No action taken.
"""

from __future__ import print_function

import string
import sys

# These imports are for PEP484, PYPI package mypy static type checking.
try:
    from typing import Tuple, Union, Any, Mapping, Sequence    # noqa : F401
except(ImportError):
    pass

#
# Format functions selectable by a format option of the same name.
# These are also useful to override the class variable MonoTable.format_func
# or on an instance.


def boolean(bool_value, format_spec='T,F'):
    # type: (bool, str) -> str
    """Format function that formats the boolean values to user's strings.

    The format_spec is a string ``'true-truth-value,false-truth-value'`` of
    the true and false truth value strings joined by comma where
    true-truth-value is returned when bool_value evaluates to logical True.
    """

    truth_values = format_spec.split(',')
    if len(truth_values) == 2:
        if bool_value:
            return truth_values[0]
        else:
            return truth_values[1]
    return format(bool_value)


# Note- For the Mypy type annotations below int and float are duck type
#       compatible with complex.  See mypy.pdf Chapter 12.

def thousands(numeric_value, format_spec=''):
    # type: (complex, str) -> str     # see note above.
    """Format function that divides by 1.0e3."""

    return format(numeric_value / 1.0e3, format_spec)


def millions(numeric_value, format_spec=''):
    # type: (complex, str) -> str     # see note above.
    """Format function that divides by 1.0e6."""

    return format(numeric_value / 1.0e6, format_spec)


def billions(numeric_value, format_spec=''):
    # type: (complex, str) -> str     # see note above.
    """Format function that divides by 1.0e9."""

    return format(numeric_value / 1.0e9, format_spec)


def trillions(numeric_value, format_spec=''):
    # type: (complex, str) -> str     # see note above.
    """Format function that divides by 1.0e12."""

    return format(numeric_value / 1.0e12, format_spec)


def milli(numeric_value, format_spec=''):
    # type: (complex, str) -> str     # see note above.
    """Format function that multiplies by 1.0e3."""

    return format(numeric_value * 1.0e3, format_spec)


def micro(numeric_value, format_spec=''):
    # type: (complex, str) -> str     # see note above.
    """Format function that multiplies by 1.0e6."""

    return format(numeric_value * 1.0e6, format_spec)


def nano(numeric_value, format_spec=''):
    # type: (complex, str) -> str     # see note above.
    """Format function that multiplies by 1.0e9."""

    return format(numeric_value * 1.0e9, format_spec)


def pico(numeric_value, format_spec=''):
    # type: (complex, str) -> str     # see note above.
    """Format function that multiplies by 1.0e12."""

    return format(numeric_value * 1.0e12, format_spec)


def kibi(numeric_value, format_spec=''):
    # type: (complex, str) -> str     # see note above.
    """Format function that divides by 1024."""

    return format(numeric_value / 1024.0, format_spec)


def mebi(numeric_value, format_spec=''):
    # type: (complex, str) -> str     # see note above.
    """Format function that divides by 1024^2."""

    return format(numeric_value / 1024.0**2, format_spec)


def gibi(numeric_value, format_spec=''):
    # type: (complex, str) -> str     # see note above.
    """Format function that divides by 1024^3."""

    return format(numeric_value / 1024.0**3, format_spec)


def tebi(numeric_value, format_spec=''):
    # type: (complex, str) -> str     # see note above.
    """Format function that divides by 1024^4."""

    return format(numeric_value / 1024.0**4, format_spec)


def mformat(mapping, format_spec=''):
    # type: (Mapping[str, object], str) -> str
    """Format function that selects values from a dictionary.

    In the format_spec use references to keyword arguments
    described by Python Standard Library Format String Syntax
    that are keys in mapping.

    For d = dict(key1=value1, key2=value2, ...)
    A call to mformat(d, format_spec) behaves like calling:
    format_spec.format(key1=value1, key2=value2, ...).

    Example:

    >>> format_spec = '{key1:.2f} {key2:}!'
    >>> print(format_spec.format(key1=25.9456, key2='spam'))
    25.95 spam!

    >>> from monotable.plugin import mformat
    >>> format_spec = '{key1:.2f} {key2:}!'   # same as above
    >>> d = {'key1': 25.9456, 'key2': 'spam'}
    >>> print(mformat(d, format_spec))
    25.95 spam!

    The keys must be strings but need not be valid python identifiers
    as shown here with a key that begins with a digit and
    a key containing a '-'.

    >>> from monotable.plugin import mformat
    >>> format_spec = '{0key1:.2f} {key-2:}!'   # same as above
    >>> d = {'0key1': 25.9456, 'key-2': 'spam'}
    >>> print(mformat(d, format_spec))
    25.95 spam!
    """

    formatter = string.Formatter()
    return formatter.vformat(format_spec, (), mapping)


def pformat(value, format_spec=''):
    # type: (Union[object, Tuple[object]], str) -> str
    """Format function adapter to percent operator %.

    The exact number % replacements in the printf-style format spec must
    be satisfied by items from value.
    """

    return format_spec % value


def sformat(value, format_spec=''):
    # type: (object, str) -> str
    """Format function adapter to str.format().

    Please keep in mind that only a single replacement field can be used.
    """

    return format_spec.format(value)


def tformat(value, format_spec=''):
    # type: (Mapping[str, str], str) -> str         # todo-...
    # todo- want:   type: (Mapping[str, object], str) -> str
    # monotable\plugin.py:117: error: Argument 1 to "substitute" of "Template"
    # has incompatible type Mapping[str, object]; expected Mapping[str, str]
    """Format function adapter to string.Template.substitute()."""

    template = string.Template(format_spec)
    return template.substitute(value)


#
# Format function error callbacks for use with MonoTable().
#


def raise_it(cell_error_exception):    # type: ignore
    # type: (monotable.table.MonoTableCellError) -> None
    """Format function error callback.  Exception is raised."""

    raise cell_error_exception


def print_it(cell_error_exception):    # type: ignore
    # type: (monotable.table.MonoTableCellError) -> str
    """Format function error callback.  Prints exception. Returns '???'."""

    print(cell_error_exception)
    if sys.version_info > (3,):
        print('{} raised after catching:'.format(cell_error_exception.name))
        print(cell_error_exception.trace_text)
    return '???'


def ignore_it(_):    # type: ignore
    # type: (monotable.table.MonoTableCellError) -> str
    """Format function error callback.  No action taken.  Returns '???'."""

    return '???'

# todo-
# note-  Designating type: ignore on the callbacks because...
#        When "from monotable.table import MonoTableCellError" is present
#        plugin dissappears from dir(monotable).  I am guessing this is due
#        to a circular import (table <-> plugin), but have not investigated
#        further to confirm or refute.  If true, it might indicate an
#        issue with the design.  For now, since static type checking is
#        experimental the type check is ignored and the type: comment
#        remains for the human readers.
