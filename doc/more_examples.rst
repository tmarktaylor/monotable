More Examples
==============

User defined format function
----------------------------

Set a user defined format function for the 3rd column.

The user defined format function directive is plugged in to the table by
passing a mapping to **mono()** or **monocol()** as keyword only argument
format_func_map.  The mapping contains the name of the format function as
the key and function object as the value.

The keys in the mapping become format directive function names.

.. testcode::

    from monotable import mono

    # User defined format function.
    def fulfill_menu_request(value, spec):
        _, _ = value, spec          # avoid unused variable nag
        return 'Spam!'              # ignore both args

    my_functions = {'fulfill_menu_request': fulfill_menu_request}

    headings = ['Id Number', 'Duties', 'Meal\nPreference']
    formats = ['', '', '(fulfill_menu_request)']

    cells = [[1, 'President and CEO', 'steak'],
             [2, 'Raise capital', 'eggs'],
             [3, 'Oversee day to day operations', 'toast']]

    print(mono(
        headings, formats, cells,
        title='>User defined format function.',
        format_func_map=my_functions))

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
- Keys in the dictionary **my_functions** become directive names,
- The Duties column auto-aligns to the left since the cells
  are strings.
- The headings auto-align to the alignment of the cell in the first row.
- The title starts with an ``'>'`` align_spec_char which right aligns
  the title over the table.

Change or omit the guidelines
-----------------------------

.. testcode::

    from monotable import mono

    headings = ['purchased\nparrot\nheart rate', 'life\nstate']

    # > is needed to right align None cell since it auto-aligns to left.
    # monotable uses empty string to format the second column.
    formats = ['>(none=rest).0f']
    cells = [[0, 'demised'],
             [0.0, 'passed on'],
             [None, 'is no more'],
             [-1],
             [0, 'ceased to be']]

    print(mono(
        headings, formats, cells,
        title='Complaint\n(registered)',

        # top guideline is equals, heading is period, bottom is omitted.
        guideline_chars='=. '))

.. testoutput::

           Complaint
          (registered)
    ========================
     purchased
        parrot  life
    heart rate  state
    ........................
             0  demised
             0  passed on
          rest  is no more
            -1
             0  ceased to be

Limit column width
------------------

Here we employ the format directive **(width=15)** to limit the width of
the second column to 15 characters or less.  The **more_marker** '...'
shows where text was omitted.

The width=N format directive applies only to the cells, not the heading.

.. testcode::

    from monotable import mono

    headings = ['Id Number', 'Duties', 'Start Date']
    formats = ['', '(width=15)']
    cells = [[1, 'President and CEO', '06/02/2016'],
             [2, 'Raise capital', '06/10/2016'],
             [3, 'Oversee day to day operations', '06/21/2016']]

    print(mono(headings, formats, cells,
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

Wrap a column and limit cell height
-----------------------------------

The second column is wrapped to a maximum width of 12 characters.

Here we customize an instance of class MonoTable in order to change
the class variable max_cell_height.  We call MonoTable's table() method.

.. testcode::

    from monotable import MonoTable

    headings = ['Id Number', 'Duties', 'Start Date']
    formats = ['', '(width=12;wrap)']
    t3 = MonoTable()
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
  one character less than the format directive (width=12;wrap) specified.
  This behaviour is a side affect of using Python textwrap to implement the
  format directive.

Fix column width
----------------

Add **;fixed** after **(width=11)** to fix the column width.  The
formatted text will be padded or truncated to the exact width.

**fixed** can also be used with **wrap** like this: **(width=N;fixed;wrap)**.

.. testcode::

    from monotable import mono

    headings = ['left\ncol', 'mid\ncol', 'right\ncol']
    formats = ['', '^(width=11;fixed)']
    cells = [['A',   1, 'x'],
             ['B', 222, 'y'],
             ['C',   3, 'z']]

    title = 'Middle column is fixed width.'

    print(mono(headings, formats, cells, title=title))

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

Selecting keys from a dictionary and table borders
--------------------------------------------------

This example sets the format function of the second column.
A format string has the form:

    ``[align_spec][directives][format_spec]``

align_spec is one of the characters '<', '^', '>' to override auto-alignment.
align_spec is not used in this example.

directives is one or more format directives enclosed by ``'('``
and ``')'`` separated by ``';'``.  In the second column the directive
is ``(mformat)``.
mformat selects the function **monotable.plugin.mformat()**
as the format function.

This example also shows formatted cells with newlines.

.. testcode::

    from monotable import mono

    headings = ['int', 'Formatted by mformat()']
    formats = ['',
        '(mformat)name= {name}\nage= {age:.1f}\ncolor= {favorite_color}']
    cells = [[2345, dict(name='Row Zero',
                         age=888.000,
                         favorite_color='blue')],

             [6789, dict(name='Row One',
                         age=999.111,
                         favorite_color='No! Red!')]]

    print(mono(headings, formats, cells,
               title='mformat() Formatting.',
               bordered=True))

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

Selecting attributes or elements
--------------------------------

Here one attribute of a cell object is selected
for formatting in the first column.  The second column selects
the element indexed by [1] from a sequence.

.. testcode::

    from monotable import mono

    headings = ['x\nattrib.', '[1]\nindex']
    formats = ['(sformat){.x}', '(sformat){[1]}']

    class MyCell:
        def __init__(self, x, y):
             self.x = x
             self.y = y

    cells = [[MyCell(1, 91), ['a', 'bb']],
             [MyCell(2, 92), ['c', 'dd']]]

    print(mono(headings, formats, cells,
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

- Set the format directive to '(sformat)' to select
  **monotable.plugin.sformat()**
  as the format function.  It is an adapter to string.format().
- The format_spec ``'{.x}'`` selects the attribute named 'x' of the cell.
- The format_spec ``'{[1]}'`` selects the element at index 1 of the cell.
- Note that a cell passed to str.format() satisfies
  only the first replacement field of the Python Format String Syntax.  You
  can only use one replacement field with the sformat format directive.
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
    print(mono(headings, formats, cells,
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

.. _simple-table-label:

Make a reStructuredText Simple Table
------------------------------------

The **separated_guidelines** and **guideline_chars**
class variables can be overridden to produce reStructuredText Simple Table
markup.

.. testcode::

    from monotable import MonoTable

    class SeparatedMonoTable(MonoTable):
        separated_guidelines = True
        guideline_chars = '==='

    headings = ['directive name', 'format function', 'description']
    t4 = SeparatedMonoTable()

    cells = [['mformat', 'monotable.plugin.mformat', 'mapping with str.format()'],
             ['pformat', 'monotable.plugin.pformat', 'printf style'],
             ['sformat', 'monotable.plugin.sformat', 'str.format()'],
             ['tformat', 'monotable.plugin.tformat', 'string.Template()'],
             ['function-name', '--', 'user defined function']]

    print(t4.table(headings, [], cells))

.. testoutput::

    ==============  ========================  =========================
    directive name  format function           description
    ==============  ========================  =========================
    mformat         monotable.plugin.mformat  mapping with str.format()
    pformat         monotable.plugin.pformat  printf style
    sformat         monotable.plugin.sformat  str.format()
    tformat         monotable.plugin.tformat  string.Template()
    function-name   --                        user defined function
    ==============  ========================  =========================

Which looks like this when rendered.

==============  ========================  =========================
directive name    format function           description
==============  ========================  =========================
mformat         monotable.plugin.mformat  mapping with str.format()
pformat         monotable.plugin.pformat  printf style
sformat         monotable.plugin.sformat  str.format()
tformat         monotable.plugin.tformat  string.Template()
function-name   --                        user defined function
==============  ========================  =========================

String template substitution
----------------------------

The format directive tformat is used to select keys from a
dictionary.  It is implemented by an adapter to Python standard library
string.Template.substitute().

.. testcode::

    from monotable import MonoTable

    headings = ['an\nint', 'Formatted by\nstr.Template()']
    formats = ['', '(tformat)name= $name\nage= $age\ncolor= $favorite_color']
    cells = [[2345,
              dict(name='Row Zero', age=888, favorite_color='blue')],
             [6789,
              dict(name='Row One', age=999, favorite_color='No......')]]

    print(mono(headings, formats, cells,
               title='A multi-line\nTitle.', bordered=True))

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

Tiled table of four tables
--------------------------

.. _pytest cases of examples:
   https://github.com/tmarktaylor/monotable/blob/master/test/test_examples.py

See **test_tile_four_tables_together()** near the bottom of
`pytest cases of examples`_.