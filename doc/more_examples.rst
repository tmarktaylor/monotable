More Examples
==============

Limit column width
------------------

Here we employ the option_spec **(width=15)** to limit the width of the second
column to 15 characters or less.  The **more_marker** '...' shows where text
was omitted.

.. testcode::

    import monotable.table

    headings = ['Id Number', 'Duties', 'Start Date']
    formats = ['', '(width=15)']
    cells = [[1, 'President and CEO', '06/02/2016'],
             [2, 'Raise capital', '06/10/2016'],
             [3, 'Oversee day to day operations', '06/21/2016']]

    print(monotable.table.table(headings, formats, cells,
            title='Limit center column to 15 characters.'))

.. testoutput::

    Limit center column to 15 characters.
    --------------------------------------
    Id Number  Duties           Start Date
    --------------------------------------
            1  President an...  06/02/2016
            2  Raise capital    06/10/2016
            3  Oversee day ...  06/21/2016
    --------------------------------------

- Note that there is no format string for the third column.  Missing
  format strings default to the empty string.
- The width=N format option applies only to the cells, not the heading.

Wrap a column and limit cell height
-----------------------------------

The second column is wrapped to a maximum width of 12 characters.

.. testcode::

    import monotable.table

    headings = ['Id Number', 'Duties', 'Start Date']
    formats = ['', '(width=12;wrap)']
    t3 = monotable.table.MonoTable()
    t3.max_cell_height = 2              # override class var

    cells = [[1, 'President and CEO', '06/02/2016'],
             [2, 'Raise capital', '06/10/2016'],
             [3, 'Oversee day to day operations', '06/21/2016']]

    title = ('Wrap center column to a maximum of 12 characters.\n'
             'Limit cell height to 2 lines')

    print(t3.table(headings, formats, cells, title=title))

.. testoutput::

    Wrap center column to a maximum of 12 characters.
    Limit cell height to 2 lines
    ----------------------------------
    Id Number  Duties       Start Date
    ----------------------------------
            1  President    06/02/2016
               and CEO
            2  Raise        06/10/2016
               capital
            3  Oversee day  06/21/2016
               to day  ...
    ----------------------------------

- Limiting the maximum cell height to 2 lines affects
  the Duties cell in the bottom row.  The **more_marker** '...' is placed
  at the end of the cell to indicate text was omitted.
- The default **max_cell_height** is None which means unlimited.
- **max_cell_height** is applied to every cell in the table.
- Changing **max_cell_height** to 1 assures there will be no multi-line
  cells in the table.
- The second column ended up wrapping to 11 characters wide,
  one character less than the format string (width=12;wrap) specified.  This
  behaviour is a side affect of using Python textwrap to implement the
  format option.

Fix column width
----------------

Add **;fixed** after **(width=11)** to fix the column width.  The
formatted text will be padded or truncated to the exact width.

**fixed** can also be used with **wrap** like this: **(width=N;fixed;wrap)**.

.. testcode::

    import monotable.table

    headings = ['left\ncol', 'mid\ncol', 'right\ncol']
    formats = ['', '^(width=11;fixed)']
    cells = [['A',   1, 'x'],
             ['B', 222, 'y'],
             ['C',   3, 'z']]

    title = 'Middle column is fixed width.'

    print(monotable.table.table(headings, formats, cells, title=title))

.. testoutput::

    Middle column is fixed width.
    ------------------------
    left      mid      right
    col       col      col
    ------------------------
    A          1       x
    B         222      y
    C          3       z
    ------------------------

- The align_spec_prefix '^' of the formats[1] center justifies the column.

Selecting attributes or elements
--------------------------------

Here one attribute of a cell object is selected
for formatting in the first column.  The second column selects
the element indexed by [1] from a sequence.

.. testcode::

    import monotable.table

    headings = ['x\nattrib.', '[1]\nindex']
    formats = ['(sformat){.x}', '(sformat){[1]}']

    class MyCell:
        def __init__(self, x, y):
             self.x = x
             self.y = y

    cells = [[MyCell(1, 91), ['a', 'bb']],
             [MyCell(2, 92), ['c', 'dd']]]

    print(monotable.table.table(headings, formats, cells,
                                title='<Select attribute/index.'))

.. testoutput::

    Select attribute/index.
    --------------
    x        [1]
    attrib.  index
    --------------
    1        bb
    2        dd
    --------------

- Set the option_spec to '(sformat)' to select **monotable.plugin.sformat()**
  as the format function.  It is an adapter to string.format().
- The format_spec ``'{.x}'`` selects the attribute named 'x' of the cell.
- The format_spec ``'{[1]}'`` selects the element at index 1 of the cell.
- Note that a cell passed to str.format() satisfies
  only the first replacement field of the Python Format String Syntax.  You
  can only use one replacement field with the sformat format option.
- Note that the first column auto-aligns to the left.  This is because
  auto-align senses the cell type which is class MyCell.  Only cells that
  inherit from numbers.Number are auto-aligned to the right.  MyCell does not
  inherit from numbers.Number.
- You can override auto-alignment on the first
  column by adding the align_spec ``'>'`` at the start of the format string.
- Since the heading auto-aligns to the alignment of the cell in the
  first row, you can also override auto-alignment on the first
  heading to keep it left aligned.

.. testcode::

    # Continues previous example.
    headings = ['<x\nattrib.', '[1]\nindex']
    formats = ['>(sformat){.x}', '(sformat){[1]}']
    print(monotable.table.table(headings, formats, cells,
                                title='<Select attribute/index.'))

.. testoutput::

    Select attribute/index.
    --------------
    x        [1]
    attrib.  index
    --------------
          1  bb
          2  dd
    --------------

Horizontal and vertical rules
-----------------------------

A cell row that starts with value **monotable.table.HR** will be replaced with a
heading guideline.

The text between columns can be changed with the format option sep.
By default sep is two spaces.  In this example sep after the first
column is changed to ``' | '``.  This creates an effect approximating
a vertical rule.

The last row only has one element.  **monotable** extends short heading,
formats, and cell rows with the empty string value.  Extra format
strings are silently ignored.

.. testcode::

    import monotable.table

    headings = ['col-0', 'col-1']

    # specify sep=' | ' between 1st and 2nd columns for vertical rule
    formats = ['(sep= | )']

    cells = [['time', '12:45'],
             ['place', 'home'],
             [monotable.table.HR],      # put a heading guideline here
             ['sound', 'bell'],
             ['volume']]          # short row is extended with empty string

    print(monotable.table.table(headings, formats, cells))

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

.. _simple-table-label:

Make a reStructuredText Simple Table
------------------------------------

The **separated_guidelines** and **guideline_chars**
class variables can be overridden to produce reStructuredText Simple Table
markup.

.. testcode::

    import monotable.table

    class SeparatedMonoTable(monotable.table.MonoTable):
        separated_guidelines = True
        guideline_chars = '==='

    headings = ['option name', 'format function', 'description']
    t4 = SeparatedMonoTable()

    cells = [['mformat', 'monotable.plugin.mformat', 'mapping with str.format()'],
             ['pformat', 'monotable.plugin.pformat', 'printf style'],
             ['sformat', 'monotable.plugin.sformat', 'str.format()'],
             ['tformat', 'monotable.plugin.tformat', 'string.Template()'],
             ['function-name', '\\', 'user defined function']]

    print(t4.table(headings, [], cells))

.. testoutput::

    =============  ========================  =========================
    option name    format function           description
    =============  ========================  =========================
    mformat        monotable.plugin.mformat  mapping with str.format()
    pformat        monotable.plugin.pformat  printf style
    sformat        monotable.plugin.sformat  str.format()
    tformat        monotable.plugin.tformat  string.Template()
    function-name  \                         user defined function
    =============  ========================  =========================

Which looks like this when rendered.

=============  ========================  =========================
option name    format function           description
=============  ========================  =========================
mformat        monotable.plugin.mformat  mapping with str.format()
pformat        monotable.plugin.pformat  printf style
sformat        monotable.plugin.sformat  str.format()
tformat        monotable.plugin.tformat  string.Template()
function-name  \                         user defined function
=============  ========================  =========================

String template substitution
----------------------------

The format option tformat is used to select keys from a
dictionary.  It is implemented by an adapter to Python standard library
string.Template.substitute().

.. testcode::

    import monotable.table

    headings = ['an\nint', 'Formatted by\nstr.Template()']
    formats = ['', '(tformat)name= $name\nage= $age\ncolor= $favorite_color']
    cells = [[2345,
              dict(name='Row Zero', age=888, favorite_color='blue')],
             [6789,
              dict(name='Row One', age=999, favorite_color='No......')]]

    print(monotable.table.bordered_table(headings, formats, cells,
                                         title='A multi-line\nTitle.'))

.. testoutput::

           A multi-line
              Title.
    +------+-----------------+
    |   an | Formatted by    |
    |  int | str.Template()  |
    +======+=================+
    | 2345 | name= Row Zero  |
    |      | age= 888        |
    |      | color= blue     |
    +------+-----------------+
    | 6789 | name= Row One   |
    |      | age= 999        |
    |      | color= No...... |
    +------+-----------------+

- The title auto-aligns to center justification.
- Title auto-alignment is overridden by placing an align_spec char at
  the beginning of the title string.

