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
.. _Full List of Features:
   https://monotable.readthedocs.io/en/latest/features.html
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

Introduction, Installation
==========================

Monotable is a Python library that generates an ASCII table from
tabular cell data that looks *pretty* in a monospaced font.

In many applications the cell data requires pre-formatting.
Monotable offers formatting directives for individual columns.
You can also write and plug in your own formatting directives.

Here is a list of some of the things Monotable does:

- Allows multi-line title, heading, and cell strings.
- Supports column oriented cell data.
- Generate a table with borders.
- Directives to limit column width.
- Add horizontal and vertical rules.
- Is *thoroughly* documented and tested.

More features are described in `Full List of Features`_  on ReadTheDocs.


Installation
------------

::

    pip install monotable

Examples
========

Per column format specifications
--------------------------------

.. testcode::

    import monotable
    headings = ['int', 'percent']
    formats = [',', '.1%']
    cells = [[123456789, 0.33], [2345678, 0.995]]
    print(monotable.mono(headings, formats, cells,
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

- When no directive is specified is supplied
  the built-in function **format(value, format_spec)** is used.
- Format directives in the list **formats** are assigned to columns from
  left to right.
- The rest of the string after the (*) is passed to format
  function as the format_spec parameter.
- To write a format_spec, consult Python's
  `Format Specification Mini-Language`_.

Format directives
-----------------


.. testcode::

    import datetime
    import monotable


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

    print(monotable.mono(headings, formats, cells,
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

- Note the format directives (thousands) and (boolean).
- '(thousands)' divides the cell value by 1000.0.
- '(boolean)yes,no' formats the cell value True as 'yes' and False as 'no'.
- You can substitute any text you want for 'yes,no' for example 'on,off'.


Column oriented input
---------------------

The input is specified as a list of tuples, one per column:
``(heading string, format directive, list of cells)``.

.. testcode::

    import datetime
    import monotable

    d = datetime.datetime(2016, 9, 16)

    column0 = ('float\nprecision\n3', '.3f',[1.23456789, 999.87654321])
    column1 = ('units of\nthousands', '(thousands).1f', [35200, 1660])
    column2 = ('datetime\n9/16/16', 'week-%U-day-%j', [d])
    column3 = ('bool to\nyes/no', '(boolean)yes,no', [True, False])
    columns = [column0, column1, column2, column3]

    print(monotable.monocol(columns,
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


Column oriented input with vertical rule column
-----------------------------------------------

- In the previous example insert monotable.VR_COL as the third column in
  ``columns =`` below.

.. testcode::

    import datetime
    import monotable

    d = datetime.datetime(2016, 9, 16)

    column0 = ('float\nprecision\n3', '.3f',[1.23456789, 999.87654321])
    column1 = ('units of\nthousands', '(thousands).1f', [35200, 1660])
    column2 = ('datetime\n9/16/16', 'week-%U-day-%j', [d])
    column3 = ('bool to\nyes/no', '(boolean)yes,no', [True, False])
    columns = [column0, column1, monotable.VR_COL, column2, column3]

    print(monotable.monocol(columns,
        title='Float, thousands, datetime, boolean formatting.'))


.. testoutput::

     Float, thousands, datetime, boolean formatting.
    -------------------------------------------------
        float             |
    precision   units of  |  datetime         bool to
            3  thousands  |  9/16/16           yes/no
    -------------------------------------------------
        1.235       35.2  |  week-37-day-260      yes
      999.877        1.7  |                        no
    -------------------------------------------------


Horizontal and vertical rules in a row oriented table
-----------------------------------------------------

A cell row that starts with value **monotable.table.HR** will be replaced with a
heading guideline.

The text between columns can be changed with the format option sep.
By default sep is two spaces.  In this example sep after the first
column is changed to ``' | '``.  This creates an effect approximating
a vertical rule.

The last row only has one element.  **monotable** extends short heading,
formats, and cell rows with the empty string value.  Extra format
directive strings are silently ignored.

.. testcode::

    import monotable

    headings = ['col-0', 'col-1']

    # specify sep=' | ' between 1st and 2nd columns for vertical rule
    formats = ['(sep= | )']

    cells = [['time', '12:45'],
             ['place', 'home'],
             monotable.HR_ROW,      # put a heading guideline here
             ['sound', 'bell'],
             ['volume']]          # short row is extended with empty string

    print(monotable.mono(headings, formats, cells))

.. testoutput::

    --------------
    col-0  | col-1
    --------------
    time   | 12:45
    place  | home
    --------------
    sound  | bell
    volume |
    --------------


`Documentation`_ on `Read the Docs`_

`More Examples`_


Some useful format directives
=============================

(boolean)
    substitutes caller's strings for True, False

(thousands)
    divide cell value by 1000.0

(milli)
    multiply cell value by 1000.0

(pformat)
    cell is formatted by python printf-style percent operator '%'

(function-name)
    directive is implemented by configuring class MonoTable with user defined
    function.

(width=N)
    sets maximum width of column to N characters, content is truncated

(width=N;wrap)
    sets maximum width of column to N characters, content is text wrapped

(width=N;fixed)
    Pads or truncates content to N characters.

(width=N;fixed;wrap)
    Pads or text wraps content to N characters.

There are 12 number scaling directives: thousands, millions, billions,
trillions, milli, micro, nano, pico, kibi, mebi, gibi, tebi.

There are 4 directives that select alternate Python format functions:
mformat, pformat, sformat, tformat.  These are useful for selecting items
from containers.

Read more about format directive syntax in "Functions" section in the
full `Documentation`_. Look for `formats` argument in
**monotable.mono.mono()**.

Auto-alignment and how to override it
=====================================

Monotable auto-aligns the title, headings, and each column.

Auto-alignment is overridden by
using one of ``'<'``, ``'^'``, ``'>'`` prefixes
on a heading string, format directive string, or title.

Read more about auto-alignment in "Class Monotable" section in the
full `Documentation`_. Follow the link `Auto-alignment`.


Links to License, Docs, Repos, Issues, PYPI page
================================================

- License: `Apache 2.0`_
- Full `Documentation`_ on `Read the Docs`_
- `Repository`_
- `Issue Tracker`_
- `Python Package Index/monotable`_
- `Master branch build status, coverage, testing`_

What Monotable does not do
==========================

- Produce terminal graphics characters.  Try PYPI terminaltables.
- Handle CJK wide characters.
- Handle ANSI escape terminal color sequences. Try PYPI terminaltables.
- Produce arbritrary markup source text.  Try PYPI tabulate instead.
  However monotable.table.bordered_table() produces valid
  reStructuredText grid table and simple table markup is possible.

Monotable does make the output of its formatting and
alignment engine available in list form.  Please look for the function
**MonoTable.row_strings()** in the API documentation.

.. Reserved for recognizing contributors
.. Contributors
.. ============

Recent Changes
==============
2.1.0 - TBD

- Add module level convenience functions mono(), monocol() and
  constants HR, HR_ROW, VR_COL.  Update pytests.
- Rename 'format strings' to 'format directive strings' in docs.
- Reorder/rework README.rst examples and other sections.

2.0.1 - 2018-05-12

- Bugfix- MonoTableCellError on str below float in a column.
- Bugfix- Incorrect format spec reported in MonoTableCellError.

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

.. admonition:: More ...

   If you are not already there, please continue reading
   `More Examples`_ in the `Documentation`_ on `Read the Docs`_.
