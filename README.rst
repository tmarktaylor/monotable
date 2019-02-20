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

Introduction, Installation
==========================

Monotable is a Python library that generates an ASCII table from
tabular cell data that looks *pretty* in a monospaced font.

Monotable offers formatting directives to reduce messy table
pre-formatting code.  You can set directives for each column.
You can also write and plug in your own format function directives.

Here is a list of some of the things Monotable does:

- Allows multi-line title, heading, and cell strings.
- Supports column oriented cell data.
- Generate a table with borders.
- Directives to limit column width and text wrap.
- Add horizontal and vertical rules.
- `List of format directives`_.
- `List of format function directives`_.
- Is *thoroughly* documented and tested.

Installation
------------

::

    pip install monotable

Examples
========

Per column format specifications
--------------------------------

Specify format string for each column.

.. testcode::

    from monotable import mono
    headings = ['comma', 'percent']
    formats = [',', '.1%']
    cells = [[123456789, 0.33], [2345678, 0.995]]
    print(mono(
        headings, formats, cells, title="',' and '%' formats."))

.. testoutput::

    ',' and '%' formats.
    --------------------
          comma  percent
    --------------------
    123,456,789    33.0%
      2,345,678    99.5%
    --------------------

- List **formats** contains the format directives.
  They are assigned to columns from left to right.
- Here the format directives are just format specifications.
- For each cell in the column, it and the format specification is passed
  to the built-in function **format(value, format_spec)**.
- To write a format_spec, consult Python's
  `Format Specification Mini-Language`_.
- The cells are organized as a list of rows where each row is a list
  of cells.

zero and none format directives
-------------------------------

Special handling for zero values and cell type None.

.. testcode::

    from datetime import datetime
    from monotable import mono

    headings = [
        'hour',
        '24 hour\ntemp\nchange',
        'wind\nspeed',
        ]

    formats = [
        '%H',
        '(zero=same)+.0f',
        '(zero=calm;none=offline).0f',
        ]

    h7 = datetime(2019, 2, 28, 7, 0, 0)
    h8 = datetime(2019, 2, 28, 8, 0, 0)
    h9 = datetime(2019, 2, 28, 9, 0, 0)

    cells = [
        [h7, -2.3,   11],
        [h8,  0.1,    0],
        [h9,    5, None]
        ]

    print(mono(
        headings, formats, cells, title='=Formatting directives.'))

.. testoutput::

    Formatting directives.
    ----------------------
          24 hour
             temp     wind
    hour   change    speed
    ----------------------
    07         -2       11
    08       same     calm
    09         +5  offline
    ----------------------

- The ``'%H'`` format gets passed by built-in function **format()** to
  datetime.__format__().
- The ``'(zero=same)+.0f'`` format string is split into two parts.

  - ``(zero=same)`` selects the zero directive with the value ``same``.
  - ``+.0f`` gets passed to the format function as format_spec.

- The zero= format directive applies when the cell is a Number and the
  formatted text contains no non-zero digits.  The characters after zero= are
  the formatted text for the cell.
- Format directives are enclosed by ``(`` and ``)``.
- Separate multiple format directives with ``;``.
- The none= format directive formats the cell value None as the characters
  after none=.

parentheses format directive
----------------------------

Enclose negative numbers with parentheses.

.. testcode::

    from monotable import mono, HR_ROW

    headings = ['Description', 'Amount']
    formats = ['', '(zero=n/a;parentheses),']

    cells = [
        ['receivables', 51],
        ['other assets', 9050],
        ['gifts', 0],
        ['pending payments',  -75],
        ['other liabilities', -623]
        ]

    print(mono(
        headings, formats, cells, title='parentheses directive.'))

.. testoutput::

      parentheses directive.
    -------------------------
    Description        Amount
    -------------------------
    receivables           51
    other assets       9,050
    gifts                n/a
    pending payments     (75)
    other liabilities   (623)
    -------------------------

Format function directives
--------------------------

Format function directives select the format function used for the column.
These are useful for scaling numbers, showing truth values, and changing
the format function.

.. testcode::

    import datetime
    from monotable import mono

    d = datetime.datetime(2016, 9, 16)

    headings = [
        'units of\nthousands',
        'bool to\nyes/no'
        ]

    formats = [
        '(thousands).1f',
        '(boolean)yes,no'
        ]

    cells = [
        [35200, True],
        [1660, False]
        ]

    print(mono(
        headings, formats, cells, title='Format function directives.'))

.. testoutput::

    Format function directives.
    ------------------
     units of  bool to
    thousands   yes/no
    ------------------
         35.2      yes
          1.7       no
    ------------------

- Note the format function directives thousands and boolean.
- '(thousands)' divides the cell value by 1000.0 and then calls **format()**.
- '(boolean)yes,no' formats the cells that test True as 'yes'
  and False as 'no'.
- You can substitute any text you want for 'yes,no' for example 'on,off'.
- You can also write and plug in an unlimited number of custom format
  function directives.
- The format function directives are implemented in the file plugin.py.


Column oriented input with vertical rule column
-----------------------------------------------

.. testcode::

    import datetime
    from monotable import monocol, VR_COL

    d = datetime.datetime(2016, 9, 16)

    column0 = ('float\nprecision\n3', '.3f',[1.23456789, 999.87654321])
    column1 = ('units of\nthousands', '(thousands).1f', [35200, 1660])
    column2 = ('datetime\n9/16/16', 'week-%U-day-%j', [d])
    column3 = ('bool to\nyes/no', '(boolean)yes,no', [True, False])
    columns = [column0, column1, VR_COL, column2, column3]

    print(monocol(columns,
        title='Float, thousands, datetime, and boolean.'))


.. testoutput::

        Float, thousands, datetime, and boolean.
    -----------------------------------------------
        float            |
    precision   units of | datetime         bool to
            3  thousands | 9/16/16           yes/no
    -----------------------------------------------
        1.235       35.2 | week-37-day-260      yes
      999.877        1.7 |                       no
    -----------------------------------------------

- Note only one cell was specified for column2.
- VR_COL in the third column renders the vertical bars.
- The title is center aligned.

Horizontal and vertical rules in a row oriented table
-----------------------------------------------------

The cell row **monotable.HR_ROW** will be replaced with
a heading guideline.

The text between columns can be changed with the format directive lsep.
lsep specifies the separator between this column and the left side
neighbor column.

By default lsep is two spaces.  In this example lsep in the second
column is changed to ``' | '``.  This creates an effect approximating
a vertical rule.

The last row only has one element.  **monotable** extends short heading,
formats, and cell rows with the empty string value.  Extra format
directive strings are silently ignored.

.. testcode::

    from monotable import mono, HR_ROW

    headings = ['col-0', 'col-1']
    formats = ['', '(lsep= | )']

    cells = [['time', '12:45'],
             ['place', 'home'],
             HR_ROW,              # put a heading guideline here
             ['sound', 'bell'],
             ['volume']]          # short row is extended with empty string

    print(mono(headings, formats, cells))

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

List of format directives
=========================

Read about all the format directive syntax in "Functions" section in the
full `Documentation`_. Look for `formats` argument in
**monotable.mono()**.

none=ccc
    render cell type None as characters ccc.

zero=ccc
    render numeric cell that formats to zero to characters ccc.

parentheses
    remove minus sign and enclose negative cell value in parentheses.

lsep=ccc
    Characters ccc separate this column and the column to the left.

rsep=ccc
    Characters ccc separate this column and the column to the right.

width=N
    sets maximum width of column to N characters, content is truncated

width=N;wrap
    sets maximum width of column to N characters, content is text wrapped

width=N;fixed
    Pads or truncates content to N characters.

width=N;fixed;wrap
    Pads or text wraps content to N characters.


List of format function directives
==================================

boolean
    test cell truthiness and substitute caller's strings for True, False.
    The format_spec is ttt,fff where characters ttt are rendered for True and
    the characters fff are rendered for False.  If no format_spec is
    present, ``'T,F'`` is used.

function-name
    selects user defined function function-name.
    User can plug in an unlimited number of format functions.

thousands millions billions trillions
    divide cell value by 1000.0 (1.0e6, 1.0e9, 1,0e12).

milli micro nano pico
    multiply cell value by 1000.0 (1.0e6, 1.0e9, 1,0e12).

kibi mebi gibi tebi
    divide cell value by 1024. (1024**2, 1024**3, 1024**4).

mformat
   format cells that are mappings by selecting keys with the format_spec.

pformat
    cell is formatted by python printf-style percent operator '%'.

sformat
   format cell with str.format().

tformat
   format cell using string.Template.substitute().


Auto-alignment and how to override it
=====================================

Monotable auto-aligns the title, headings, and each column.

Auto-alignment is overridden by
using one of ``'<'``, ``'^'``, ``'>'`` prefixes
on a heading string, format directive string, or title.

Read more about auto-alignment in "Class MonoTable" section in the
full `Documentation`_. Follow the link `Auto-alignment`.


Links to License, Docs, Repos, Issues, PYPI page
================================================

- License: `Apache 2.0`_
- Full `Documentation`_ on `Read the Docs`_
- `Repository`_
- `Issue Tracker`_
- `Python Package Index/monotable`_
- `Master branch build status, coverage, testing`_

What monotable does not do
==========================

- Produce terminal graphics characters.  Try PYPI terminaltables.
- Handle CJK wide characters.
- Handle ANSI escape terminal color sequences. Try PYPI terminaltables.
- Produce arbritrary markup source text.  Try PYPI tabulate instead.
  However calling mono() or monocol() with keyword argument
  bordered=True produces valid reStructuredText grid table and
  simple table markup is possible.

Monotable does make the output of its formatting and
alignment engine available in list form.  Please look for the function
**MonoTable.row_strings()** in the API documentation.

.. Reserved for recognizing contributors
.. Contributors
.. ============

Recent Changes
==============
2.1.0 - 2019-02-21

- Add module level convenience functions mono(), monocol() and
  constants HR_ROW, VR_COL.
- Add formatting directives none, zero, parentheses, lsep, and rsep.
- Reorder/rework docs examples and other sections.
- Drop Python 3.3 and 3.4 classifiers. Drop Python 3.4 tests from Travis CI.

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
