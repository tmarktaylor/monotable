# Copyright 2020 Mark Taylor
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

Maintainers- Please add new format functions to format_functions dict below.


   Functions:
   boolean    Format function that converts the boolean values to strings.

   thousands  Format function that divides by 1.0e3.
   millions   Format function that divides by 1.0e6.
   billions   Format function that divides by 1.0e9.
   trillions  Format function that divides by 1.0e12.
   milli      Format function that multiplies by 1.0e3.
   micro      Format function that multiplies by 1.0e6.
   nano       Format function that multiplies by 1.0e9.
   pico       Format function that multiplies by 1.0e12.
   kibi       Format function that divides by 1024.
   mebi       Format function that divides by 1024^2.
   gibi       Format function that divides by 1024^3.
   tebi       Format function that divides by 1024^4.

   mformat    Format function adapter of a mapping to str.format().
   pformat    Format function adapter to % operator.
   sformat    Format function adapter to str.format().
   tformat    Format function adapter to Template.substitute().

   raise_it   Formatting error callback.  Exception is raised.
   print_it   Formatting error callback.  Exception is printed.
   ignore_it  Formatting error callback.  No action taken.
"""

import string
from typing import Any, Mapping

from monotable.cellerror import MonoTableCellError

#
# Format functions selectable by a format directive of the same name.
# These are also useful to override the class variable MonoTable.format_func
# or on an instance.


def boolean(bool_value: bool, format_spec: str = 'T,F') -> str:
    """Format function that formats the boolean values to user's strings.

    The format_spec is a string ``'true-truth-value,false-truth-value'`` of
    the true and false truth value strings joined by comma where
    true-truth-value is returned when bool_value evaluates to logical True.
    The default value for argument format_spec above is a good example.
    If fspec or !fspec is rendered check for an incorrect format_spec.
    """

    truth_values = format_spec.split(',')
    if len(truth_values) == 2:
        if bool_value:
            return truth_values[0]
        else:
            return truth_values[1]
    else:
        # the format_spec is malformed
        if bool_value:
            return 'fspec'
        else:
            return '!fspec'


# Note- For the Mypy type annotations below int and float are duck type
#       compatible with complex.  See mypy.pdf Chapter 12.

def thousands(numeric_value: complex, format_spec: str = '') -> str:
    """Format function that divides by 1.0e3."""

    return format(numeric_value / 1.0e3, format_spec)


def millions(numeric_value: complex, format_spec: str = '') -> str:
    """Format function that divides by 1.0e6."""

    return format(numeric_value / 1.0e6, format_spec)


def billions(numeric_value: complex, format_spec: str = '') -> str:
    """Format function that divides by 1.0e9."""

    return format(numeric_value / 1.0e9, format_spec)


def trillions(numeric_value: complex, format_spec: str = '') -> str:
    """Format function that divides by 1.0e12."""

    return format(numeric_value / 1.0e12, format_spec)


def milli(numeric_value: complex, format_spec: str = '') -> str:
    """Format function that multiplies by 1.0e3."""

    return format(numeric_value * 1.0e3, format_spec)


def micro(numeric_value: complex, format_spec: str = '') -> str:
    """Format function that multiplies by 1.0e6."""

    return format(numeric_value * 1.0e6, format_spec)


def nano(numeric_value: complex, format_spec: str = '') -> str:
    """Format function that multiplies by 1.0e9."""

    return format(numeric_value * 1.0e9, format_spec)


def pico(numeric_value: complex, format_spec: str = '') -> str:
    """Format function that multiplies by 1.0e12."""

    return format(numeric_value * 1.0e12, format_spec)


def kibi(numeric_value: complex, format_spec: str = '') -> str:
    """Format function that divides by 1024."""

    return format(numeric_value / 1024.0, format_spec)


def mebi(numeric_value: complex, format_spec: str = '') -> str:
    """Format function that divides by 1024^2."""

    return format(numeric_value / 1024.0**2, format_spec)


def gibi(numeric_value: complex, format_spec: str = '') -> str:
    """Format function that divides by 1024^3."""

    return format(numeric_value / 1024.0**3, format_spec)


def tebi(numeric_value: complex, format_spec: str = '') -> str:
    """Format function that divides by 1024^4."""

    return format(numeric_value / 1024.0**4, format_spec)


def mformat(mapping: Mapping[str, Any], format_spec: str = '') -> str:
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


def pformat(value: Any, format_spec: str = '') -> str:
    """Format function adapter to percent operator %.

    The exact number % replacements in the printf-style format spec must
    be satisfied by items from value.
    """

    # Added enclosing str() to prevent mypy thinking Any is returned.
    # Perhaps mypy is unable to choose between numeric modulo operator
    # and printf style formatting from the context.
    return str(format_spec % value)


def sformat(value: Any, format_spec: str = '') -> str:
    """Format function adapter to str.format().

    Please keep in mind that only a single replacement field can be used.
    """

    return format_spec.format(value)


def tformat(value: Mapping[str, Any], format_spec: str = '') -> str:
    """Format function adapter to string.Template.substitute()."""

    template = string.Template(format_spec)
    return template.substitute(value)


# Maintainers- Please add new format functions to format_functions dict.
# directive name: function
format_functions = {
    'boolean': boolean,
    'thousands': thousands,
    'millions': millions,
    'billions': billions,
    'trillions': trillions,
    'milli': milli,
    'micro': micro,
    'nano': nano,
    'pico': pico,
    'kibi': kibi,
    'mebi': mebi,
    'gibi': gibi,
    'tebi': tebi,
    'mformat': mformat,
    'pformat': pformat,
    'sformat': sformat,
    'tformat': tformat
}
"""Format functions selectable as format directives."""

#
# Format function error callbacks for use with MonoTable().
#


def raise_it(cell_error_exception: MonoTableCellError) -> None:
    """Format function error callback.  Exception is raised."""

    raise cell_error_exception


def print_it(cell_error_exception: MonoTableCellError) -> str:
    """Format function error callback.  Prints exception. Returns '???'."""

    print(cell_error_exception)
    print('{} raised after catching:'.format(cell_error_exception.name))
    print(cell_error_exception.trace_text)
    return '???'


def ignore_it(_: MonoTableCellError) -> str:
    """Format function error callback.  No action taken.  Returns '???'."""

    return '???'
