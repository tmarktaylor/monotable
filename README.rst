.. This file is used by Sphinx and for the setup.py long_description.
.. The examples are doctested by Sphinx.
.. The doctest directives here are replaced when setup.py creates
.. the setup() argument long_description.

.. |apache| image:: https://img.shields.io/pypi/l/monotable.svg
   :target: http://www.apache.org/licenses/LICENSE-2.0
   :alt: License: Apache 2.0

.. |py_versions| image:: https://img.shields.io/pypi/pyversions/monotable.svg
    :target: https://pypi.python.org/pypi/monotable
    :alt: Python versions supported

.. |pypi_version| image:: https://img.shields.io/pypi/v/monotable.svg
   :target: https://pypi.python.org/pypi/monotable
   :alt: PyPI version

.. _Format Specification Mini-Language:
   https://docs.python.org
   /3/library/string.html#format-specification-mini-language
.. _Format String Syntax:
   https://docs.python.org/3/library/string.html#format-string-syntax
.. _Template Strings:
   https://docs.python.org/3/library/string.html#template-strings
.. _Printf Style:
   https://docs.python.org
   /3/library/stdtypes.html#printf-style-string-formatting
.. _Apache 2.0:
   http://www.apache.org/licenses/LICENSE-2.0
.. _Documentation:
   http://monotable.readthedocs.io/en/latest//index.html
.. _More Examples:
   http://monotable.readthedocs.io/en/latest/more_examples.html
.. _Read the Docs:
   https://readthedocs.org
.. _Repository:
   https://github.com/tmarktaylor/monotable
.. _Issue Tracker:
   https://github.com/tmarktaylor/monotable/issues
.. _Python Package Index/monotable:
   https://pypi.python.org/pypi/monotable
.. _Master branch build status:
   https://github.com/tmarktaylor/monotable/blob/master/README.md

Introduction
============

|apache| |pypi_version| |py_versions|

monotable is a Python library that generates an ASCII table from
tabular data that looks *pretty* when printed in a monospaced font.

monotable eliminates the need to pre-format
your data objects before generating the table.

monotable will do the formatting for you using your format function
or one of its own general purpose format functions; on a per column basis.

monotable handles multi-line content.

monotable is *thoroughly* documented and tested.

First Example
-------------

.. testcode::

    import monotable
    headings = ['int', 'percent']
    formats = [',', '.1%']
    t1 = monotable.MonoTable(headings, formats)
    cells = [[123456789, 0.33], [2345678, 0.995]]
    print(t1.table(cells,
                   title='=Comma and percent formats.'))

.. testoutput::

     Comma and percent
          formats.
    --------------------
            int  percent
    --------------------
    123,456,789    33.0%
      2,345,678    99.5%
    --------------------

- The built-in function **format(value, format_spec)** is used by default
  for each column.
- The string in the list **formats** is passed as format_spec for the column.
- To write a format_spec, consult Python's
  `Format Specification Mini-Language`_.

Installation
------------

::

    pip install monotable


Links to License, Docs, Repos, Issues, PYPI page
------------------------------------------------
- License: `Apache 2.0`_
- Full `Documentation`_ on `Read the Docs`_
- `Repository`_
- `Issue Tracker`_
- `Python Package Index/monotable`_
- `Master branch build status`_

Description
-----------

You can specify the format spec and the format function on a per column
basis as needed.

These format functions are available:

   - The default is built-in function **format**\ (value, format_spec).
   - An unlimited number of user defined plug-in format functions.
   - An adapter to standard library string.format().
   - An adapter to pass a mapping to string.format().
   - An adapter to percent operator % formatting.
   - An adapter to standard library Template.substitute().

When custom formatting code is needed for an object type,
put it in a plug-in format function and reuse it in other tables that
process the same type.

monotable supports multi-line content in headings, formatted cells,
and titles.

monotable can limit column width on a per column basis and
truncates or wraps the text to fit.  Maximum cell height
is configurable.  A more marker is placed to show where text was omitted.

monotable auto-aligns each column.  Auto-alignment is overridden by
using one of ``'<'``, ``'^'``, ``'>'`` prefixes
on a heading string, format string, or title.

monotable does not do the following:

    - Produce terminal graphics characters.  Try PYPI terminaltables.
    - Produce markup source text.  Try PYPI tabulate instead.
    - Handle CJK wide characters.
    - Handle ANSI escape terminal color sequences. Try PYPI terminaltables.

However, monotable does make the output of its formatting and
alignment engine available in list form.  Please look for the function
**MonoTable.row_strings()** in the API documentation.

More features are described in the documentation section
'Full List of Features'.

.. Reserved for recognizing contributors
.. Contributors
.. ============

.. Reserved for change log
.. Recent Changes
.. ==============

Examples
========

Per column formatting with format spec
--------------------------------------

In the example below formats is a list of format strings, one for each column.
Format strings are assigned to columns from left to right.

.. testcode::

    import datetime
    import monotable

    d = datetime.datetime(2016, 9, 16)

    headings = ['precision\n1', 'precision\n3', 'default', '9/16/16']
    formats = ['.1f', '.3f', '', 'week-%U-day-%j']
    t2 = monotable.MonoTable(headings, formats)

    cells = [[1.23456789,   1.23456789,   1.23456789, d],
             [999.87654321, 999.87654321, 999.87654321, None]]

    print(t2.table(cells, title='Different float precisions.'))

.. testoutput::

               Different float precisions.
    -------------------------------------------------
    precision  precision
            1          3     default  9/16/16
    -------------------------------------------------
          1.2      1.235    1.234568  week-37-day-260
        999.9    999.877  999.876543
    -------------------------------------------------

- For type float, when the format_spec is empty, a default format_spec
  of ``'.6f'`` is used.  This is configurable.
- Auto-alignment is right justifying a cell that is an instance of
  numbers.Number.
- Auto alignment aligns the heading the same way as the alignment of
  the cell in the first row of the column.
- The title is centered by default.


Selecting keys from a dictionary
--------------------------------

This example uses monotable's extended format string notation to set
the format function of the second column. A format string has the form:

    ``[align_spec][option_spec][format_spec]``

align_spec is one of the characters '<', '^', '>' to override auto-alignment.
align_spec is not used in this example.

option_spec is one or more monotable options enclosed by ``'('``
and ``')'`` separated by ``';'``.  In the second column the option_spec
is ``(mformat)``.
mformat selects the function **monotable.plugin.mformat()**
as the format function.
The API section MonoTable.__init__() in the docs describes the other options.

.. testcode::

    import monotable

    headings = ['int', 'Formatted by mformat()']
    formats = ['',
        '(mformat)name= {name}\nage= {age:.1f}\ncolor= {favorite_color}']
    t3 = monotable.MonoTable(headings, formats)

    cells = [[2345, dict(name='Row Zero',
                         age=888.000,
                         favorite_color='blue')],

             [6789, dict(name='Row One',
                         age=999.111,
                         favorite_color='No! Red!')]]

    print(t3.bordered_table(cells, title='mformat() Formatting.'))

.. testoutput::

          mformat() Formatting.
    +------+------------------------+
    |  int | Formatted by mformat() |
    +======+========================+
    | 2345 | name= Row Zero         |
    |      | age= 888.0             |
    |      | color= blue            |
    +------+------------------------+
    | 6789 | name= Row One          |
    |      | age= 999.1             |
    |      | color= No! Red!        |
    +------+------------------------+

- Note the age fixed precision formatting.  This is not possible with
  template substitution provided by option tformat.
- Format a bordered table by calling **bordered_table()**
  instead of **table()**.
- This example also shows formatted cells with newlines.


User defined format function
----------------------------

Set a user defined format function for the 3rd column.

The user defined function is plugged in to the table by overriding the
MonoTable class variable **format_func_map** with a dictionary that contains
the name of the function as the key and function object as the value.

The keys in **format_func_map** become option names that can be specified
in the option_spec.

.. testcode::

    import monotable

    # User defined format function.
    def fullfill_menu_request(value, spec):
        _, _ = value, spec          # avoid unused variable nag
        return 'Spam!'              # ignore both args

    # Configure MonoTable subclass with the dictionary
    # of user defined format functions.
    class FormatFuncsMonoTable(monotable.MonoTable):
        format_func_map = {'fullfill_menu_request': fullfill_menu_request}

    headings = ['Id Number', 'Duties', 'Meal\nPreference']
    formats = ['', '', '(fullfill_menu_request)']
    t4 = FormatFuncsMonoTable(headings, formats)

    cells = [[1, 'President and CEO', 'steak'],
             [2, 'Raise capital', 'eggs'],
             [3, 'Oversee day to day operations', 'toast']]

    print(t4.table(cells, title='>User defined format function.'))

.. testoutput::

                           User defined format function.
    ----------------------------------------------------
                                              Meal
    Id Number  Duties                         Preference
    ----------------------------------------------------
            1  President and CEO              Spam!
            2  Raise capital                  Spam!
            3  Oversee day to day operations  Spam!
    ----------------------------------------------------

- The user defined format function **fullfill_menu_request()**
  ignores the arguments and returns the string 'Spam!'.
- Keys in the dictionary **my_format_func_map** become option names
  that can be used in an option_spec.
- The dictionary is configured into a MonoTable subclass called
  FormatFuncsMonoTable by overriding the class variable **format_func_map**.
- Alternatively, you can override on an instance by assignment
  like this:

.. testcode::

  t4 = monotable.MonoTable(headings, formats)
  t4.format_func_map = {'fullfill_menu_request': fullfill_menu_request}

- The Duties column auto-aligns to the left since the cells
  are strings.
- The headings auto-align to the alignment of the cell in the first row.
- The title starts with an ``'>'`` align_spec_char which right aligns
  the title over the table.

.. admonition:: More ...

   If you are not already there, please continue reading
   `More Examples`_ in the `Documentation`_ on `Read the Docs`_.
