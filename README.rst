.. This file is used by Sphinx and for the setup.py long_description.
.. The examples are doctested by Sphinx.
.. The doctest directives here are replaced when setup.py creates
.. the setup() argument long_description.

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
   https://monotable.readthedocs.io/en/latest//index.html
.. _More Examples:
   https://monotable.readthedocs.io/en/latest/more_examples.html
.. _Read the Docs:
   https://readthedocs.org
.. _Repository:
   https://github.com/tmarktaylor/monotable
.. _Issue Tracker:
   https://github.com/tmarktaylor/monotable/issues
.. _Python Package Index/monotable:
   https://pypi.python.org/pypi/monotable
.. _Master branch build status, coverage, testing:
   https://github.com/tmarktaylor/monotable/blob/master/README.md

Introduction, Installation, and First Examples
==============================================

monotable is a Python library that generates an ASCII table from
tabular data that looks *pretty* in a monospaced font.

In many applications the tabular data requires pre-formatting.
monotable can do the formatting for you using one
of its general purpose format functions on a per column basis.
You can also plug in an unlimited number of custom format functions.

monotable is *thoroughly* documented and tested.

Installation
------------

::

    pip install monotable


Example - Per column format specifications
------------------------------------------

.. testcode::

    import monotable.table
    headings = ['int', 'percent']
    formats = [',', '.1%']
    cells = [[123456789, 0.33], [2345678, 0.995]]
    print(monotable.table.table(headings, formats, cells,
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
- Format strings in the list **formats** are assigned to columns from
  left to right.
- The string passed as format_spec for the column.
- To write a format_spec, consult Python's
  `Format Specification Mini-Language`_.

Example - float, thousands, datetime, and boolean formatting
------------------------------------------------------------


.. testcode::

    import datetime
    import monotable.table

    d = datetime.datetime(2016, 9, 16)

    headings = ['float\nprecision\n3',
                'units of\nthousands',
                'datetime\n9/16/16',
                'bool to\nyes/no']

    formats = ['.3f',
               '(thousands).1f',
               'week-%U-day-%j',
               '(boolean)yes,no']

    cells = [[1.23456789,   35200,    d, True],
             [999.87654321,  1660,  None, False]]

    print(monotable.table.table(headings, formats, cells,
        title='Float, thousands, datetime, boolean formatting.'))

.. testoutput::

    Float, thousands, datetime, boolean formatting.
    ----------------------------------------------
        float
    precision   units of  datetime         bool to
            3  thousands  9/16/16           yes/no
    ----------------------------------------------
        1.235       35.2  week-37-day-260      yes
      999.877        1.7                        no
    ----------------------------------------------

- A format string is: ``[align_spec][option_spec][format_spec]``.  All three
  parts are optional.

  - align_spec is one of ``'<'``, ``'^'``, ``'>'``.
  - option_spec is one or more options separated by ``';'``.
    between ``'('`` and ``')'``.
  - format_spec is passed to the format function.

- '(thousands)' invokes monotable.plugin.thousands() as the format function
  for the column.
- '(boolean)yes,no' invokes monotable.plugin.boolean() with the
  format_spec 'yes,no' which formats True as 'yes' and False as 'no'.
- The 12 integrated number scaling format functions are:  thousands, millions,
  billions, trillions, milli, micro, nano, pico, kibi, mebi, gibi, tebi.
- The float and thousands cells are auto-aligned to the right since
  they are numbers.
- Override auto-alignment by adding an align_spec.

`Skip ahead to examples.`_

Links to License, Docs, Repos, Issues, PYPI page
================================================

- License: `Apache 2.0`_
- Full `Documentation`_ on `Read the Docs`_
- `Repository`_
- `Issue Tracker`_
- `Python Package Index/monotable`_
- `Master branch build status, coverage, testing`_

Description
===========

These are the format functions integrated into monotable:

   - The default is built-in function **format**\ (value, format_spec).
   - Boolean value formatter boolean().
   - 12 number scaling functions including thousands(), mebi(), and micro().
   - Adapters to standard library string.format(), Template.substitute(),
     and printf-style formatting.
   - An unlimited number of user defined plug-in format functions.

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
on a heading string, format string, or title as ``[align_spec]``.

monotable accepts table data that is organized by columns.

monotable does not do the following:

    - Produce terminal graphics characters.  Try PYPI terminaltables.
    - Handle CJK wide characters.
    - Handle ANSI escape terminal color sequences. Try PYPI terminaltables.
    - Produce arbritrary markup source text.  Try PYPI tabulate instead.
      However monotable.table.bordered_table() produces valid
      reStructuredText grid table and simple table markup is possible.

monotable does make the output of its formatting and
alignment engine available in list form.  Please look for the function
**MonoTable.row_strings()** in the API documentation.

More features are described in the full documentation section
'Full List of Features'.

.. Reserved for recognizing contributors
.. Contributors
.. ============

Recent Changes
==============

2.0.0 - 2017-06-16

- Changed the API: headings and formats parameters are now passed to table(),
  bordered_table().
- Added to class MonoTable 2 member functions that take table data
  organized as columns.
- Added convenience functions to module monotable.table.
  They call class MonoTable public member functions.
- Added 13 new plugin format functions and the corresponding format options:
  boolean, thousands, millions, billions, trillions, milli, micro, nano,
  pico, kibi, mebi, gibi, tebi.
- Removed 'from MonoTable import' statements from __init__.py.

1.0.2 - 2017-04-06

- Bug fix, incorrect cell auto-alignment when mixed types in a column.
- Bug fix, format_none_as cell ignoring column format string's align_spec.
- Remove and re-add files to git index so stored with LFs.
- Add complexity inspections to CI.
- Refactor 2 functions to reduce McCabe complexity.
- Code inspection fixes.  Docs and comments fixed.

1.0.1 - 2017-03-26

- MANIFEST.in and doc fixes.


.. _`Skip ahead to examples.`:

Examples
========

Column Oriented Input
---------------------

The input is specified as a list of tuples, one per column:
``(heading string, format string, list of cells)``.

.. testcode::

    import datetime
    import monotable.table

    d = datetime.datetime(2016, 9, 16)

    column0 = ('float\nprecision\n3', '.3f',[1.23456789, 999.87654321])
    column1 = ('units of\nthousands', '(thousands).1f', [35200, 1660])
    column2 = ('datetime\n9/16/16', 'week-%U-day-%j', [d])
    column3 = ('bool to\nyes/no', '(boolean)yes,no', [True, False])
    columns = [column0, column1, column2, column3]

    print(monotable.table.cotable(columns,
        title='Float, thousands, datetime, boolean formatting.'))

.. testoutput::

    Float, thousands, datetime, boolean formatting.
    ----------------------------------------------
        float
    precision   units of  datetime         bool to
            3  thousands  9/16/16           yes/no
    ----------------------------------------------
        1.235       35.2  week-37-day-260      yes
      999.877        1.7                        no
    ----------------------------------------------

- Note only one cell was specified for column2.
- The output is identical to that from the earlier example.


User defined format function
----------------------------

Set a user defined format function for the 3rd column.

The user defined function is plugged in to the table by overriding the
MonoTable class variable **format_func_map** with a dictionary that contains
the name of the function as the key and function object as the value.

The keys in **format_func_map** become option names that can be specified
in the option_spec.

.. testcode::

    import monotable.table

    # User defined format function.
    def fulfill_menu_request(value, spec):
        _, _ = value, spec          # avoid unused variable nag
        return 'Spam!'              # ignore both args

    # Configure MonoTable subclass with the dictionary
    # of user defined format functions.
    class FormatFuncsMonoTable(monotable.table.MonoTable):
        format_func_map = {'fulfill_menu_request': fulfill_menu_request}

    headings = ['Id Number', 'Duties', 'Meal\nPreference']
    formats = ['', '', '(fulfill_menu_request)']
    t1 = FormatFuncsMonoTable()

    cells = [[1, 'President and CEO', 'steak'],
             [2, 'Raise capital', 'eggs'],
             [3, 'Oversee day to day operations', 'toast']]

    print(t1.table(headings, formats, cells,
                   title='>User defined format function.'))

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

- The user defined format function **fulfill_menu_request()**
  ignores the arguments and returns the string 'Spam!'.
- Keys in the dictionary **my_format_func_map** become option names
  that can be used in an option_spec.
- The dictionary is configured into a MonoTable subclass called
  FormatFuncsMonoTable by overriding the class variable **format_func_map**.
- Alternatively, you can override on an instance by assignment
  like this:

.. testcode::

  t2 = monotable.table.MonoTable()
  t2.format_func_map = {'fulfill_menu_request': fulfill_menu_request}

- The Duties column auto-aligns to the left since the cells
  are strings.
- The headings auto-align to the alignment of the cell in the first row.
- The title starts with an ``'>'`` align_spec_char which right aligns
  the title over the table.

Selecting keys from a dictionary and table borders
--------------------------------------------------

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

    import monotable.table

    headings = ['int', 'Formatted by mformat()']
    formats = ['',
        '(mformat)name= {name}\nage= {age:.1f}\ncolor= {favorite_color}']
    cells = [[2345, dict(name='Row Zero',
                         age=888.000,
                         favorite_color='blue')],

             [6789, dict(name='Row One',
                         age=999.111,
                         favorite_color='No! Red!')]]

    print(monotable.table.bordered_table(headings, formats, cells,
                                         title='mformat() Formatting.'))

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

.. admonition:: More ...

   If you are not already there, please continue reading
   `More Examples`_ in the `Documentation`_ on `Read the Docs`_.
