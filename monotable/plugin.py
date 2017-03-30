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

#
# Format functions selectable by a format option of the same name.
# These are also useful to override the class variable MonoTable.format_func
# or on an instance.


def mformat(mapping, format_spec):
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


def pformat(value, format_spec):
    """Format function adapter to percent operator %.

    The exact number % replacements in the printf-style format spec must
    be satisfied by items from value.
    """

    return format_spec % value


def sformat(value, format_spec):
    """Format function adapter to str.format().

    Please keep in mind that only a single replacement field can be used.
    """

    return format_spec.format(value)


def tformat(value, format_spec):
    """Format function adapter to string.Template.substitute()."""

    template = string.Template(format_spec)
    return template.substitute(value)


#
# Format function error callbacks for use with MonoTable().
#

def raise_it(cell_error_exception):
    """Format function error callback.  Exception is raised."""

    raise cell_error_exception


def print_it(cell_error_exception):
    """Format function error callback.  Prints exception. Returns '???'."""

    print(cell_error_exception)
    if sys.version_info > (3,):
        print('{} raised after catching:'.format(cell_error_exception.name))
        print(cell_error_exception.trace_text)
    return '???'


def ignore_it(_):
    """Format function error callback.  No action taken.  Returns '???'."""

    return '???'
