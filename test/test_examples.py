"""Assertion based test cases for monotable.MonoTable.  Run with pytest."""

from collections import namedtuple
import datetime
import doctest
import math

import monotable
import monotable.plugin


def test_doctest_scanner_py():
    failure_count, test_count = doctest.testmod(m=monotable.scanner)
    assert test_count > 0
    assert failure_count == 0


def test_simple_data_types():
    """Simple data types.

    Automatic justification.
    Numbers are right justified, all other types are left justified.
    Headings are justified per cell type in the first row.
    Floating point format defaults to '.6f' specified by the
    class variable default_float_format_spec.
    """

    headings = ['int', 'float', 'string', 'tuple']
    t = monotable.MonoTable(headings)
    cells = [[123456789, math.pi, 'Hello World', (2, 3)],
             [2, math.e * 1000, 'another string', ('a', 'b')]]
    text = t.table(cells)
    expected = '\n'.join([
        "--------------------------------------------------",
        "      int        float  string          tuple",
        "--------------------------------------------------",
        "123456789     3.141593  Hello World     (2, 3)",
        "        2  2718.281828  another string  ('a', 'b')",
        "--------------------------------------------------",
        ])
    assert text == expected


def test_an_attribute_and_an_index_with_instance_assigned_format_func():
    """
    Show an attribute of an cell object and an item of a sequence.

    Change the instance format_func to monotable.sformat()
    by assigning it to the instance variable.

    Use align_spec '<' to left justify the title.
    Note that a cell passed to str.format() satisfies
    only the first replacement field of the Format String Syntax.
    """

    headings = ['x\nattrib.', 'y\nattrib.', '[0]\nindex', '[1]\nindex']
    formats = ['{.x}', '{.y}', '{[0]}', '{[1]}']
    t = monotable.MonoTable(headings, formats)
    t.format_func = monotable.plugin.sformat
    point = namedtuple('point', ['x', 'y'])
    cells = [[point(1, 91), point(2, 92), point(3, 93), point(4, 94)],
             [point(5, 95), point(6, 96), point(7, 97), point(8, 98)]]
    text = t.table(cells, title='<Select attribute/index.')
    expected = '\n'.join([
        "Select attribute/index.",
        "------------------------------",
        "x        y        [0]    [1]",
        "attrib.  attrib.  index  index",
        "------------------------------",
        "1        92       3      94",
        "5        96       7      98",
        "------------------------------",
       ])
    assert text == expected


def test_datetime():
    """Test formatting datetime object.

    Title is left justified '<' and textwrapped '='.
    The title shows the datetime object used for the 2 cells.
    Headings show the format string used in each column.
    """
    format_column_0 = '%Y-%m-%d--%I:%M:%S'
    format_column_1 = 'week-%U-day-%j'
    headings = ['format string\n"' + format_column_0 + '"',
                'format string\n"' + format_column_1 + '"']
    formats = [format_column_0, format_column_1]
    t = monotable.MonoTable(headings, formats)

    d = datetime.datetime(2016, 1, 10, 19, 35, 18)
    cells = [[d, d]]
    title = ('<=Formatting a datetime object '
             'datetime.datetime(2016, 1, 10, 19, 35, 18)')
    text = t.bordered_table(cells, title=title)
    expected = '\n'.join([
        "Formatting a datetime object",
        "datetime.datetime(2016, 1, 10, 19, 35, 18)",
        "+----------------------+------------------+",
        "| format string        | format string    |",
        '| "%Y-%m-%d--%I:%M:%S" | "week-%U-day-%j" |',
        "+======================+==================+",
        "| 2016-01-10--07:35:18 | week-02-day-010  |",
        "+----------------------+------------------+",
    ])
    assert text == expected


def test_template_substitution_and_multiline():
    """Show values using string.Template substitution.  Show multi-line cells.

    Use format_option_spec for the second column to specify
    monotable.tformat() for that column.
    This invokes str.Template formatting for the column.
    Format a bordered table by calling bordered_table() instead of table().
    """
    headings = ['int', 'Formatted by str.Template()']
    formats = ['', '(tformat)name= $name\nage= $age\ncolor= $favorite_color']
    t = monotable.MonoTable(headings, formats)

    cells = [[2345, dict(name='Row Zero', age=888, favorite_color='blue')],
             [6789, dict(name='Row One', age=999, favorite_color='No! Red!')]]
    text = t.bordered_table(cells, title='str.Template() Formatting.')
    expected = '\n'.join([
        "      str.Template() Formatting.",
        "+------+-----------------------------+",
        "|  int | Formatted by str.Template() |",
        "+======+=============================+",
        "| 2345 | name= Row Zero              |",
        "|      | age= 888                    |",
        "|      | color= blue                 |",
        "+------+-----------------------------+",
        "| 6789 | name= Row One               |",
        "|      | age= 999                    |",
        "|      | color= No! Red!             |",
        "+------+-----------------------------+",
    ])
    assert text == expected


def test_mapping_and_multiline():
    """Show values from a mapping using mformat().  Show multi-line cells.

    Use format_option_spec for the second column to specify
    monotable.mformat() for that column.
    Note the age fixed precision formatting.  This is not possible with
    template substitution.
    Format a bordered table by calling bordered_table() instead of table().
    """
    headings = ['int', 'Formatted by mformat()']
    f1 = '(mformat)name= {name}\nage= {age:.1f}\ncolor= {favorite_color}'
    formats = ['', f1]
    cells = [[2345,
              dict(name='Row Zero', age=888.000, favorite_color='blue')],
             [6789,
              dict(name='Row One', age=999.111, favorite_color='No! Red!')]]
    t = monotable.MonoTable(headings, formats)
    text = t.bordered_table(cells, title='mformat() Formatting.')
    expected = '\n'.join([
        "      mformat() Formatting.",
        "+------+------------------------+",
        "|  int | Formatted by mformat() |",
        "+======+========================+",
        "| 2345 | name= Row Zero         |",
        "|      | age= 888.0             |",
        "|      | color= blue            |",
        "+------+------------------------+",
        "| 6789 | name= Row One          |",
        "|      | age= 999.1             |",
        "|      | color= No! Red!        |",
        "+------+------------------------+",
    ])
    assert text == expected


def test_printf_style_with_tuple_format_and_subclass_for_format_func():
    """Formatting with pformat printf-style String Formatting.

    Create a subclass of MonoTable that uses monotable.pformat as the
    default format function.

    Floating point format precision defaults to 6 places.
    For a tuple value printf-style formatting expects a format spec.
    for each item of the tuple.
    An empty option_spec '()' is placed before the format_spec '(%d, %d)'
    to feed an empty option_spec to the option_spec scanning logic which
    consumes everything between the initial '(' and ')' in the format string.

    Note that all the items in the printf-style format value
    must be consumed when processing the format spec.
    """

    headings = ['int', 'float', 'string', 'tuple']
    formats = ['%d', '%f', '%s', '()(%d, %d)']

    class CustomMonoTable(monotable.MonoTable):
        format_func = staticmethod(monotable.plugin.pformat)

    t = CustomMonoTable(headings, formats)

    cells = [[123456789, math.pi, 'Hello World', (1, 2)],
             [2, math.e * 1000, 'another string', (3, 4)]]
    text = t.table(cells)
    expected = '\n'.join([
        "----------------------------------------------",
        "      int        float  string          tuple",
        "----------------------------------------------",
        "123456789     3.141593  Hello World     (1, 2)",
        "        2  2718.281828  another string  (3, 4)",
        "----------------------------------------------",
    ])
    assert text == expected


def test_horizontal_and_vertical_guidelines_and_indent():
    """Test horizontal and vertical rules, and table indent.

    Test the following:
    - Row starting with a HR.  The HR row has one cell.
    - Custom sep to create vertical rule after the first column specified
      by the option_spec of the first column.
    - Indent string placed at the start of every line.
    """

    headings = ['col-0', 'col-1']
    formats = ['(sep= | )']  # specify sep=' | ' between 1st and 2nd columns
    t = monotable.MonoTable(headings, formats, indent='*****')

    cells = [['time', '12:45'],
             ['place', 'home'],
             [monotable.HR],
             ['sound', 'bell'],
             ['volume', 'very loud']]
    text = t.table(cells)
    expected = '\n'.join([
        "*****------------------",
        "*****col-0  | col-1",
        "*****------------------",
        "*****time   | 12:45",
        "*****place  | home",
        "*****------------------",
        "*****sound  | bell",
        "*****volume | very loud",
        "*****------------------",
    ])
    assert text == expected


def test_width_format_option():
    """Limit the width of a column using width format option."""

    headings = ['Id Number', 'Duties', 'Start Date']
    formats = ['', '(width=15)']
    t = monotable.MonoTable(headings, formats)
    cells = [[1, 'President and CEO', '06/02/2016'],
             [2, 'Raise capital', '06/10/2016'],
             [3, 'Oversee day to day operations', '06/21/2016']]
    text = t.table(cells, title='Limit center column to 15 characters.')
    expected = '\n'.join([
        "Limit center column to 15 characters.",
        "--------------------------------------",
        "Id Number  Duties           Start Date",
        "--------------------------------------",
        "        1  President an...  06/02/2016",
        "        2  Raise capital    06/10/2016",
        "        3  Oversee day ...  06/21/2016",
        "--------------------------------------",
    ])
    assert text == expected


def test_width_fixed_format_option():
    """Fix the width of a column using width format option.

    Look for 5 extra spaces after 1234567890123 and Raise capital."""

    headings = ['Id Number', 'Duties', 'Start Date']
    formats = ['', '(width=18;fixed)']
    t = monotable.MonoTable(headings, formats)
    cells = [[1, '1234567890123', '06/02/2016'],
             [2, 'Raise capital', '06/10/2016'],
             [3, 'Oversee day', '06/21/2016']]
    text = t.table(cells, title='Fixed center column to 15 characters.')
    expected = '\n'.join([
        "  Fixed center column to 15 characters.",
        "-----------------------------------------",
        "Id Number  Duties              Start Date",
        "-----------------------------------------",
        "        1  1234567890123       06/02/2016",
        "        2  Raise capital       06/10/2016",
        "        3  Oversee day         06/21/2016",
        "-----------------------------------------",
    ])
    assert text == expected


def test_width_fixed_format_option_with_none_and_missing_cells():
    """Fix the width of a column using width and fixed format options.

    Show that cell of value None and the empty cells added to a
    row that was missing cells are handled.
    Look for 5 extra spaces before 1234567890123 ."""

    headings = ['Id Number', 'Duties', 'Start Date']
    formats = ['', '>(width=18;fixed)']
    t = monotable.MonoTable(headings, formats)
    cells = [[1, '1234567890123', '06/02/2016'],
             [2, None, '06/10/2016'],
             [3]]
    text = t.table(cells, title='Fixed center column to 15 characters.')
    expected = '\n'.join([
        "  Fixed center column to 15 characters.",
        "-----------------------------------------",
        "Id Number              Duties  Start Date",
        "-----------------------------------------",
        "        1       1234567890123  06/02/2016",
        "        2                      06/10/2016",
        "        3",
        "-----------------------------------------",
    ])
    assert text == expected


def test_width_fixed_right_justified_format_option():
    """Fix the width of a column using width and fixed format options.

    Look for 5 extra spaces before 1234567890123 and Raise capital."""

    headings = ['Id Number', 'Duties', 'Start Date']
    formats = ['', '>(width=18;fixed)']
    t = monotable.MonoTable(headings, formats)
    cells = [[1, '1234567890123', '06/02/2016'],
             [2, 'Raise capital', '06/10/2016'],
             [3, 'Oversee day', '06/21/2016']]
    text = t.table(cells, title='Fixed center column to 15 characters.')
    expected = '\n'.join([
        "  Fixed center column to 15 characters.",
        "-----------------------------------------",
        "Id Number              Duties  Start Date",
        "-----------------------------------------",
        "        1       1234567890123  06/02/2016",
        "        2       Raise capital  06/10/2016",
        "        3         Oversee day  06/21/2016",
        "-----------------------------------------",
    ])
    assert text == expected


def test_wrap_format_option():
    """Limit the width of a column using width and wrap format options.

    Note that the center column actually occupies 11 characters since no
    lines in the column wrapped to the full 12 characters.
    This looks reasonable without borders because the cell vertical align
    default is TOP.
    """

    headings = ['Id Number', 'Duties', 'Start Date']
    formats = ['', '(width=12;wrap)']
    t = monotable.MonoTable(headings, formats)
    cells = [[1, 'President and CEO', '06/02/2016'],
             [2, 'Raise capital', '06/10/2016'],
             [3, 'Oversee day to day operations', '06/21/2016']]
    text = t.table(cells,
                   title='Wrap center column to a maximum of 12 characters.')
    expected = '\n'.join([
        "Wrap center column to a maximum of 12 characters.",
        "----------------------------------",
        "Id Number  Duties       Start Date",
        "----------------------------------",
        "        1  President    06/02/2016",
        "           and CEO",
        "        2  Raise        06/10/2016",
        "           capital",
        "        3  Oversee day  06/21/2016",
        "           to day",
        "           operations",
        "----------------------------------",
    ])
    assert text == expected


def test_fixed_wrap_format_option():
    """Limit the width of a column using width and wrap format options.

    Note that without the fixed option the center column wraps to 9
    characters.  Three spaces were added to pad out to 12 characters.
    """

    headings = ['Id Number', '123456789', 'Start Date']
    formats = ['', '(width=12;wrap;fixed)']
    t = monotable.MonoTable(headings, formats)
    cells = [[1, 'President President', '06/02/2016'],
             [2, 'Raise capital', '06/10/2016'],
             [3, 'Oversee Oversee', '06/21/2016']]
    text = t.table(cells,
                   title='Wrap center column to a fixed width 12 characters.')
    expected = '\n'.join([
        "Wrap center column to a fixed width 12 characters.",
        "-----------------------------------",
        "Id Number  123456789     Start Date",
        "-----------------------------------",
        "        1  President     06/02/2016",
        "           President",
        "        2  Raise         06/10/2016",
        "           capital",
        "        3  Oversee       06/21/2016",
        "           Oversee",
        "-----------------------------------",
    ])
    assert text == expected


def test_fixed_wrap_right_justified_format_option():
    """Limit the width of a column using width and wrap format options.

    Note that without the fixed option the center column wraps to 9
    characters.  Three spaces were added at the start of the column
    to pad out to 12 characters.
    """

    headings = ['Id Number', '123456789', 'Start Date']
    formats = ['', '>(width=12;wrap;fixed)']
    t = monotable.MonoTable(headings, formats)
    cells = [[1, 'President President', '06/02/2016'],
             [2, 'Raise capital', '06/10/2016'],
             [3, 'Oversee Oversee', '06/21/2016']]
    text = t.table(cells,
                   title=('Wrap center column to a fixed width 12 '
                          'characters.  right.'))
    expected = '\n'.join([
        "Wrap center column to a fixed width 12 characters.  right.",
        "-----------------------------------",
        "Id Number     123456789  Start Date",
        "-----------------------------------",
        "        1     President  06/02/2016",
        "              President",
        "        2         Raise  06/10/2016",
        "                capital",
        "        3       Oversee  06/21/2016",
        "                Oversee",
        "-----------------------------------",
    ])
    print(text)
    assert text == expected


def test_width_fixed_format_option_missing_cells():
    """Do fixed width on a column that is missing cells.

    Leave out the heading too and center justify.  Result should be an
    all space column that is 15 spaces wide.
    """

    headings = ['Id Number', 'Duties', 'Start Date']
    formats = ['', '(width=15)', '^(width=15;fixed)']
    t = monotable.MonoTable(headings, formats)
    # third column of cells is missing
    cells = [[1, 'President and CEO'],
             [2, 'Raise capital'],
             [3, 'Oversee day to day operations']]
    text = t.table(cells, title='<Limit center column to 15 characters.')
    expected = '\n'.join([
        "Limit center column to 15 characters.",
        "-------------------------------------------",
        "Id Number  Duties              Start Date",
        "-------------------------------------------",
        "        1  President an...",
        "        2  Raise capital",
        "        3  Oversee day ...",
        "-------------------------------------------",
    ])
    assert text == expected


def test_width_fixed_format_option_only_none_cells():
    """Do fixed width on a column that has only None.

    Leave out the heading too and center justify.  Result should be an
    all space column that is 15 spaces wide.
    """

    headings = ['Id Number', 'Duties']
    formats = ['', '(width=15)', '^(width=15;fixed)']
    t = monotable.MonoTable(headings, formats)
    # third column of cells is None
    cells = [[1, 'President and CEO', None],
             [2, 'Raise capital', None],
             [3, 'Oversee day to day operations', None]]
    text = t.table(cells, title='<Limit center column to 15 characters.')
    expected = '\n'.join([
        "Limit center column to 15 characters.",
        "-------------------------------------------",
        "Id Number  Duties",
        "-------------------------------------------",
        "        1  President an...",
        "        2  Raise capital",
        "        3  Oversee day ...",
        "-------------------------------------------",
    ])
    assert text == expected


def test_auto_align_mixed_cell_types_in_column():
    """Check auto alignment when a column has numeric and non-numeric types."""

    headings = ['Number', 'Mixed', 'Non-Number']
    t = monotable.MonoTable(headings)
    cells = [[1, 11002233, 'a-string'],
             [2, 'Spam!', None],
             [33, 444, 'abc']]
    text = t.table(cells, 'Different cell types in middle column.')
    expected = '\n'.join([
        "Different cell types in middle column.",
        "----------------------------",
        "Number     Mixed  Non-Number",
        "----------------------------",
        "     1  11002233  a-string",
        "     2  Spam!",
        "    33       444  abc",
        "----------------------------",
    ])
    assert text == expected


def test_max_cell_height():
    """Limit the maximum height of cells in the previous table.

    This truncates the Duties column at the bottom of the table.
    Note that the center column actually occupies 11 characters since no
    lines in the column wrapped to the full 12 characters.
    """

    headings = ['Id Number', 'Duties', 'Start Date']
    formats = ['', '(width=12;wrap)']
    t = monotable.MonoTable(headings, formats)
    t.max_cell_height = 2              # override class var
    cells = [[1, 'President and CEO', '06/02/2016'],
             [2, 'Raise capital', '06/10/2016'],
             [3, 'Oversee day to day operations', '06/21/2016']]
    title = ('Wrap center column to a maximum of 12 characters.\n'
             'Limit cell height to 2 lines')
    text = t.table(cells, title=title)
    expected = '\n'.join([
        "Wrap center column to a maximum of 12 characters.",
        "Limit cell height to 2 lines",
        "----------------------------------",
        "Id Number  Duties       Start Date",
        "----------------------------------",
        "        1  President    06/02/2016",
        "           and CEO",
        "        2  Raise        06/10/2016",
        "           capital",
        "        3  Oversee day  06/21/2016",
        "           to day  ...",
        "----------------------------------",
    ])
    assert text == expected


def test_bordered_format():
    """Add borders to the table from test_max_cell_height()."""

    headings = ['Id Number', 'Duties', 'Start Date']
    formats = ['', '(width=12;wrap)']
    cells = [[1, 'President and CEO', '06/02/2016'],
             [2, 'Raise capital', '06/10/2016'],
             [3, 'Oversee day to day operations', '06/21/2016']]
    t = monotable.MonoTable(headings, formats)
    t.max_cell_height = 2
    title = ('Wrap center column to a maximum of 12 characters.\n'
             'Limit cell height to 2 lines.\n'
             'Format with borders.')
    text = t.bordered_table(cells, title=title)
    expected = '\n'.join([
        "Wrap center column to a maximum of 12 characters.",
        "Limit cell height to 2 lines.",
        "Format with borders.",
        "+-----------+-------------+------------+",
        "| Id Number | Duties      | Start Date |",
        "+===========+=============+============+",
        "|         1 | President   | 06/02/2016 |",
        "|           | and CEO     |            |",
        "+-----------+-------------+------------+",
        "|         2 | Raise       | 06/10/2016 |",
        "|           | capital     |            |",
        "+-----------+-------------+------------+",
        "|         3 | Oversee day | 06/21/2016 |",
        "|           | to day  ... |            |",
        "+-----------+-------------+------------+",
    ])
    assert text == expected


def test_user_defined_format_function():
    """Set a user defined format function in the 3rd column.

    Right justify the title by prefixing with '>'.
    """

    def show_last_four(value, format_spec):
        _ = format_spec
        return '*' * (len(value) - 4) + value[-4:]

    myformatfuncmap = {'show_last_four': show_last_four}
    headings = ['Id Number', 'Duties', 'Sensitive\nInfo']
    formats = ['', '', '(show_last_four)']

    class CustomMonoTable(monotable.MonoTable):
        format_func_map = myformatfuncmap
    t = CustomMonoTable(headings, formats)
    cells = [[1, 'President and CEO', '123'],
             [2, 'Raise capital', '12345'],
             [3, 'Oversee day to day operations', '123-45-6789']]
    text = t.table(cells, title='>User defined format function.')
    expected = '\n'.join([
        "                        User defined format function.",
        "-----------------------------------------------------",
        "                                          Sensitive",
        "Id Number  Duties                         Info",
        "-----------------------------------------------------",
        "        1  President and CEO              123",
        "        2  Raise capital                  *2345",
        "        3  Oversee day to day operations  *******6789",
        "-----------------------------------------------------",
    ])
    assert text == expected


def test_default_float_format_spec():
    """Change default_float_format_spec.

    Do a different float precision in each column.
    Rounding occurs in the last two columns.
    """

    cells = [[9.1234567] * 4]
    headings = ['.1f', '.3f', '.5f', 'default=.4f']
    formats = ['.1f', '.3f', '.5f']
    t = monotable.MonoTable(headings, formats)
    t.default_float_format_spec = '.4f'
    text = t.table(cells, title='Different float precision in each column.')
    expected = '\n'.join([
        "Different float precision in each column.",
        "--------------------------------",
        ".1f    .3f      .5f  default=.4f",
        "--------------------------------",
        "9.1  9.123  9.12346       9.1235",
        "--------------------------------",
    ])
    assert text == expected


def test_disable_default_float_format_spec():
    """Disable default_float_format_spec feature by setting to ''.

    The 4th column has the same float precision as the cell value.
    """

    cells = [[9.1234567] * 4]
    headings = ['.1f', '.3f', '.5f', 'disable\ndefault_float_format_spec']
    formats = ['.1f', '.3f', '.5f']
    t = monotable.MonoTable(headings, formats)
    t.default_float_format_spec = ''
    text = t.table(cells, title='<Disable default in last column.')
    expected = '\n'.join([
        "Disable default in last column.",
        "----------------------------------------------",
        "                                       disable",
        ".1f    .3f      .5f  default_float_format_spec",
        "----------------------------------------------",
        "9.1  9.123  9.12346                  9.1234567",
        "----------------------------------------------",
    ])
    assert text == expected


def test_heading_left_align_spec_and_format_left_align_spec():
    """Test align_specs.

    This test uses the same cellgrid as test_default_float_format_spec().
    Test heading align follows format left align_spec in column 2.
    Test heading align follows heading left align_spec in column 3.
    Note the < align_spec of the format '<.3f' causes the decimal points
    to misalign in the second column.
    """

    row0 = [9.1234567] * 4
    row1 = [88.1] * 4
    cells = [row0, row1]
    headings = ['.1f', '.3f', '<.5f', 'default=.4f']
    formats = ['.1f', '<.3f', '.5f']
    t = monotable.MonoTable(headings, formats)
    t.default_float_format_spec = '.4f'
    text = t.table(cells, title='Different float precision in each column.')
    expected = '\n'.join([
        "Different float precision in each column.",
        "-----------------------------------",
        " .1f  .3f     .5f       default=.4f",
        "-----------------------------------",
        " 9.1  9.123    9.12346       9.1235",
        "88.1  88.100  88.10000      88.1000",
        "-----------------------------------",
    ])
    assert text == expected


def test_heading_center_align_spec_and_format_center_align_spec():
    """Test center align_spec.

    Test heading align follows format center align_spec in column 2.
    Test heading align follows heading center align_spec in column 3.
    """

    cells = [[9.1234567] * 4]
    headings = ['.1f', '.3f', '^.5f', 'default=.4f']
    formats = ['.1f', '^.3f', '.5f']
    t = monotable.MonoTable(headings, formats)
    t.default_float_format_spec = '.4f'
    text = t.table(cells, title='Different float precision in each column.')
    expected = '\n'.join([
        "Different float precision in each column.",
        "--------------------------------",
        ".1f   .3f     .5f    default=.4f",
        "--------------------------------",
        "9.1  9.123  9.12346       9.1235",
        "--------------------------------",
    ])
    assert text == expected


def test_heading_and_format_right_align_spec():
    """Show default_float_format_spec with right align_spec.

    Subclass MonoTable and override the class var default_float_format_spec.
    Note the headings are right justified.
    """
    cells = [[9.1234567] * 4]
    headings = ['.1f', '.3f', '>.5f', 'default=.4f']
    formats = ['.1f', '>.3f', '.5f']

    class FloatPoint4MonoTable(monotable.MonoTable):
        default_float_format_spec = '.4f'
    t = FloatPoint4MonoTable(headings, formats)
    text = t.table(cells, title='Different float precision in each column.')
    expected = '\n'.join([
        "Different float precision in each column.",
        "--------------------------------",
        ".1f    .3f      .5f  default=.4f",
        "--------------------------------",
        "9.1  9.123  9.12346       9.1235",
        "--------------------------------",
    ])
    assert text == expected


def test_override_align_spec_chars():
    """Change the class var align_spec_chars on an instance.

    This works as long as noe of the headings, formats, and title start
    with one of the new align_spec_chars.
    """

    cells = [[123, 'import', 4567, 'this']]
    headings = ['an int', 'string', 'another int', 'another string']
    formats = ['R', '', 'L', 'C']
    t = monotable.MonoTable(headings, formats)
    t.align_spec_chars = 'LCR'
    text = t.table(cells, title='RUser align_spec_chars.')
    expected = '\n'.join([
        "                     User align_spec_chars.",
        "-------------------------------------------",
        "an int  string  another int  another string",
        "-------------------------------------------",
        "   123  import  4567              this",
        "-------------------------------------------",
    ])
    assert text == expected


def test_override_title_wrap_spec_char():
    """Change the class var wrap_spec_char on an instance.

    The [wrap_spec] in the title selects textwrap.
    The table title is interpreted as [align_spec][wrap_spec]string.
    """

    cells = [[123, 'import']]
    headings = ['an int', 'a string']
    t = monotable.MonoTable(headings)
    t.wrap_spec_char = '$'
    text = t.table(cells,
                   title='<$User wrap_spec_char changed on an instance.')
    expected = '\n'.join([
        "User",
        "wrap_spec_char",
        "changed on an",
        "instance.",
        "----------------",
        "an int  a string",
        "----------------",
        "   123  import",
        "----------------",
    ])
    assert text == expected


def test_override_heading_valign():
    """Change the class var heading_valign on an instance.

    heading_valign controls vertical alignment of headings.
    """

    cells = [[123, 'import']]
    headings = ['a\nshort\nint', 'a\nslightly\nlonger\nstring']
    t = monotable.MonoTable(headings)
    t.heading_valign = monotable.TOP
    text = t.table(cells, title='instance.heading_valign = TOP')
    expected = '\n'.join([
        "instance.heading_valign = TOP",
        "---------------",
        "    a  a",
        "short  slightly",
        "  int  longer",
        "       string",
        "---------------",
        "  123  import",
        "---------------",
    ])
    assert text == expected


def test_override_guideline_chars():
    """Change all three guideline chars."""

    cells = [[123, 'import', 4567, 'this']]
    headings = ['an int', 'string', 'another int', 'another string']
    formats = ['>', '', '<', '^']
    t = monotable.MonoTable(headings, formats)
    t.guideline_chars = 'X=*'
    text = t.table(cells, title='>User guideline_chars.')
    expected = '\n'.join([
        "                      User guideline_chars.",
        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "an int  string  another int  another string",
        "===========================================",
        "   123  import  4567              this",
        "*******************************************",
    ])
    assert text == expected


def test_override_separated_guidelines():
    class SeparatedMonoTable(monotable.MonoTable):
        separated_guidelines = True
        guideline_chars = '==='

    headings = ['option name', 'format function', 'description']
    t = SeparatedMonoTable(headings)

    cells = [['mformat', 'monotable.plugin.mformat',
              'mapping with str.format()'],
             ['pformat', 'monotable.plugin.pformat', 'printf style'],
             ['sformat', 'monotable.plugin.sformat', 'str.format()'],
             ['tformat', 'monotable.plugin.tformat', 'string.Template()'],
             ['function-name', '\\', 'user defined function']]

    text = t.table(cells)
    expected = '\n'.join([
        "=============  ========================  =========================",
        "option name    format function           description",
        "=============  ========================  =========================",
        "mformat        monotable.plugin.mformat  mapping with str.format()",
        "pformat        monotable.plugin.pformat  printf style",
        "sformat        monotable.plugin.sformat  str.format()",
        "tformat        monotable.plugin.tformat  string.Template()",
        "function-name  \                         user defined function",
        "=============  ========================  =========================",
    ])
    assert text == expected


def test_override_separated_guidelines_no_bottom_guideline():
    """Test separated guideline style with no bottom guideline."""

    class SeparatedMonoTable(monotable.MonoTable):
        guideline_chars = '== '    # disable bottom guideline
        separated_guidelines = True

    cells = [[123, 'import', 4567, 'this']]
    headings = ['an int', 'string', 'another int', 'another string']
    formats = ['>', '', '<', '^']
    t = SeparatedMonoTable(headings, formats)
    text = t.table(cells, title='>separated_guidelines = True.')
    expected = '\n'.join([
        "               separated_guidelines = True.",
        "======  ======  ===========  ==============",
        "an int  string  another int  another string",
        "======  ======  ===========  ==============",
        "   123  import  4567              this",
    ])
    assert text == expected


def test_omit_top_and_bottom_guidelines():
    """Override guideline_chars to omit top and bottom guidelines."""

    class CustomMonoTable(monotable.MonoTable):
        guideline_chars = ' = '

    cells = [[123, 'import', 4567, 'this']]
    headings = ['an int', 'string', 'another int', 'another string']
    formats = ['>', '', '<', '^']

    t = CustomMonoTable(headings, formats)
    text = t.table(cells, title='<No top, bottom guidelines.')
    expected = '\n'.join([
        "No top, bottom guidelines.",
        "an int  string  another int  another string",
        "===========================================",
        "   123  import  4567              this",
    ])
    assert text == expected


def test_top_guideline_is_dots_and_only_guideline():
    """Omit heading and bottom guidelines.  Top guideline is '.'"""

    class CustomMonoTable(monotable.MonoTable):
        guideline_chars = '.'

    cells = [[123, 'import', 4567, 'this']]
    headings = ['an int', 'string', 'another int', 'another string']
    formats = ['>', '', '<', '^']
    t = CustomMonoTable(headings, formats)
    text = t.table(cells, title='^Top guideline is .s, no others.')
    expected = '\n'.join([
        "      Top guideline is .s, no others.",
        "...........................................",
        "an int  string  another int  another string",
        "   123  import  4567              this",
    ])
    assert text == expected


def test_override_cell_vertical_alignment_to_center_top():
    """Change cell vertical alignment to CENTER_TOP."""

    class CustomMonoTable(monotable.MonoTable):
        cell_valign = monotable.CENTER_TOP

    cells = [['A\n4\nline\ncell', '3\nline\ncell', '2 line\ncell'],
             [monotable.HR],
             ['A\nfour\nline\ncell', 'three\nline\ncell', 'two line\ncell']]
    headings = ['4 line cells', '3 line cells', '2 line cells']
    t = CustomMonoTable(headings)
    text = t.table(cells, title='cell_valign=CENTER_TOP')
    expected = '\n'.join([
        "         cell_valign=CENTER_TOP",
        "----------------------------------------",
        "4 line cells  3 line cells  2 line cells",
        "----------------------------------------",
        "A             3",
        "4             line          2 line",
        "line          cell          cell",
        "cell",
        "----------------------------------------",
        "A             three",
        "four          line          two line",
        "line          cell          cell",
        "cell",
        "----------------------------------------",
    ])
    assert text == expected


def test_override_cell_vertical_alignment_to_center_bottom():
    """Change cell vertical alignment to CENTER_BOTTOM."""

    class CustomMonoTable(monotable.MonoTable):
        cell_valign = monotable.CENTER_BOTTOM

    cells = [['A\n4\nline\ncell', '3\nline\ncell', '2 line\ncell'],
             [monotable.HR],
             ['A\nfour\nline\ncell', 'three\nline\ncell', 'two line\ncell']]
    headings = ['4 line cells', '3 line cells', '2 line cells']

    t = CustomMonoTable(headings)
    text = t.table(cells, title='cell_valign=CENTER_BOTTOM')
    expected = '\n'.join([
        "       cell_valign=CENTER_BOTTOM",
        "----------------------------------------",
        "4 line cells  3 line cells  2 line cells",
        "----------------------------------------",
        "A",
        "4             3             2 line",
        "line          line          cell",
        "cell          cell",
        "----------------------------------------",
        "A",
        "four          three         two line",
        "line          line          cell",
        "cell          cell",
        "----------------------------------------",
    ])
    assert text == expected


def test_override_more_marker_override_max_cell_height_option_max_width():
    """Show truncation of too long lines and too tall cell.

    Change the more_marker to '**'.
    Limit cell height to 2 lines.  Limit column 2 width to 2 characters.
    Note that a column width is max(widest heading line, width=N).  In other
    words a wide heading for a column supersedes a width=N specified width.
    Bottom center cell first line is truncated to 3 characters.  The 4
    cells in the first and second columns are limited to two line height.
    """

    class CustomMonoTable(monotable.MonoTable):
        more_marker = '**'
        max_cell_height = 2

    cells = [['A\n4\nline\ncell', '3\nline\ncell', '2 line\ncell'],
             [monotable.HR],
             ['A\nfour\nline\ncell', 'three\nline\ncell', 'two line\ncell']]
    headings = ['4 line', '3', '2 line']
    formats = ['', '(width=3)', '']

    t = CustomMonoTable(headings, formats)
    text = t.table(cells, title="max_cell_height=2, more_marker='**'")
    expected = '\n'.join([
        "max_cell_height=2, more_marker='**'",
        "---------------------",
        "4 line  3    2 line",
        "---------------------",
        "A       3    2 line",
        "4   **  l**  cell",
        "---------------------",
        "A       t**  two line",
        "four**  l**  cell",
        "---------------------",
    ])
    assert text == expected


def test_comma_format_spec():
    """Center title, multi-line headings and cell, and more.

    The comma format spec is new in Python 2.7.
    The title is center justified by default.
    Use multi-line headings.
    Use multi-line cell "Hello\nWorld".
    Use a float format in the second column to change precision.
    Use , format to the numbers (New in Python 2.7).
    Drop the 2 formats.  A short row of formats is OK.
    Drop the last cell in 2nd row.  A short row of cells is no problem.
    """

    pi = 3.141592653589793   # math.pi
    e = 2.718281828459045    # math.e
    headings = ['an\nint', 'the\nfloat', 'string', 'tuple']
    formats = [',', ',.2f']
    t = monotable.MonoTable(headings, formats)
    cells = [[123456789, pi, 'Hello\nWorld', (2, 3)],
             [2, e * 1000, 'another string']]
    text = t.table(cells, title='Centered Title Line.')
    expected = '\n'.join([
        "             Centered Title Line.",
        "---------------------------------------------",
        "         an       the",
        "        int     float  string          tuple",
        "---------------------------------------------",
        "123,456,789      3.14  Hello           (2, 3)",
        "                       World",
        "          2  2,718.28  another string",
        "---------------------------------------------",
    ])
    assert text == expected


def test_default_when_override_border_chars_to_empty_string():
    """Override class var border_chars to empty string.

    '+' is the hard coded default used for missing border_chars.
    """
    headings = ['one\ndigit\nint', 'another\nint', 'floats']
    t = monotable.MonoTable(headings)
    t.border_chars = ''
    cells = [[1, 29, 3.5], [4, 5, 16.34]]
    text = t.bordered_table(cells, '^centered caption\njust 2 lines')
    expected = '\n'.join([
        "        centered caption",
        "          just 2 lines",
        "+++++++++++++++++++++++++++++++",
        "+   one +         +           +",
        "+ digit + another +           +",
        "+   int +     int +    floats +",
        "+++++++++++++++++++++++++++++++",
        "+     1 +      29 +  3.500000 +",
        "+++++++++++++++++++++++++++++++",
        "+     4 +       5 + 16.340000 +",
        "+++++++++++++++++++++++++++++++",
    ])
    assert text == expected


def test_override_border_chars():
    """Change border_chars to 'TBSCH'

    TBSCH corresponds to top, bottom, sides, corner, heading guideline.
    """

    headings = ['one\ndigit\nint', 'another\nint', 'floats']
    t = monotable.MonoTable(headings)
    t.border_chars = 'TBSCH'
    cells = [[1, 29, 3.5], [4, 5, 16.34]]
    text = t.bordered_table(cells, '^centered caption\njust 2 lines')
    expected = '\n'.join([
        "        centered caption",
        "          just 2 lines",
        "CTTTTTTTCTTTTTTTTTCTTTTTTTTTTTC",
        "S   one S         S           S",
        "S digit S another S           S",
        "S   int S     int S    floats S",
        "CHHHHHHHCHHHHHHHHHCHHHHHHHHHHHC",
        "S     1 S      29 S  3.500000 S",
        "CBBBBBBBCBBBBBBBBBCBBBBBBBBBBBC",
        "S     4 S       5 S 16.340000 S",
        "CBBBBBBBCBBBBBBBBBCBBBBBBBBBBBC",
    ])
    assert text == expected


def test_override_hmargin_vmargin():
    """Change class variables hmargin and vmargin in subclass."""

    class BigMarginMonoTable(monotable.MonoTable):
        hmargin = 3
        vmargin = 2

    headings = ['one\ndigit\nint', 'another\nint', 'floats']
    t = BigMarginMonoTable(headings)
    cells = [[1, 29, 3.5], [4, 5, 16.34]]
    text = t.bordered_table(cells, '<hmargin=3, vmargin=2')
    expected = '\n'.join([
        "hmargin=3, vmargin=2",
        "+-----------+-------------+---------------+",
        "|           |             |               |",
        "|           |             |               |",
        "|     one   |             |               |",
        "|   digit   |   another   |               |",
        "|     int   |       int   |      floats   |",
        "|           |             |               |",
        "|           |             |               |",
        "+===========+=============+===============+",
        "|           |             |               |",
        "|           |             |               |",
        "|       1   |        29   |    3.500000   |",
        "|           |             |               |",
        "|           |             |               |",
        "+-----------+-------------+---------------+",
        "|           |             |               |",
        "|           |             |               |",
        "|       4   |         5   |   16.340000   |",
        "|           |             |               |",
        "|           |             |               |",
        "+-----------+-------------+---------------+",
    ])
    assert text == expected


def test_tile_four_tables_together():
    """Tile tables together.

    Create a string for each of the 3 tables.  One for upper left, one for
    upper right, and two copies of a 3rd table for the bottom row.
    Guidelines are omitted between the tiles.  The guidelines in the result
    are from the component tables ta, tb, and tc.

    Tiled table:   ta  tb
                   tc  tc
    """

    headings = ['4 line cells', '3 line cells']

    class CenterBottomMonoTable(monotable.MonoTable):
        cell_valign = monotable.CENTER_BOTTOM

    ta = CenterBottomMonoTable(headings)
    cells = [['A\n4\nline\ncell', '3\nline\ncell'],
             [monotable.HR],
             ['A\nfour\nline\ncell', 'three\nline\ncell']]
    taf = ta.table(cells, title='vertical align CENTER_BOTTOM')

    headings = ['4 line', '3', '2 line']
    formats = ['', '(width=3)', '']

    class CustomMonoTable(monotable.MonoTable):
        more_marker = '**'
        max_cell_height = 2

    tb = CustomMonoTable(headings, formats)
    cells = [['A\n4\nline\ncell', '3\nline\ncell', '2 line\ncell'],
             [monotable.HR],
             ['A\nfour\nline\ncell', 'three\nline\ncell', 'two line\ncell']]
    tbf = tb.table(cells, title="max_cell_height=2")

    headings = ['one\ndigit\nint', 'another\nint', 'floats']

    class BadBorderCharsFloat4fMonoTable(monotable.MonoTable):
        border_chars = ''
        default_float_format_spec = '.4f'

    tc = BadBorderCharsFloat4fMonoTable(headings)
    cells = [[1, 29, 3.5], [4, 5, 16.34]]
    tcf = tc.bordered_table(cells, '^centered title\n of 2 lines')

    class NoGuidelinesMonoTable(monotable.MonoTable):
        guideline_chars = ''
        sep = '    '

    tiled = NoGuidelinesMonoTable()
    cells = [[taf, tbf],
             [None, None],  # to insert space between the top and bottom rows
             [tcf, tcf]]    # same table twice in the bottom row
    text = tiled.table(cells)
    expected = '\n'.join([
        "vertical align CENTER_BOTTOM       max_cell_height=2",
        "--------------------------       ---------------------",
        "4 line cells  3 line cells       4 line  3    2 line",
        "--------------------------       ---------------------",
        "A                                A       3    2 line",
        "4             3                  4   **  l**  cell",
        "line          line               ---------------------",
        "cell          cell               A       t**  two line",
        "--------------------------       four**  l**  cell",
        "A                                ---------------------",
        "four          three",
        "line          line",
        "cell          cell",
        "--------------------------",
        "",
        "        centered title                   centered title",
        "          of 2 lines                       of 2 lines",
        "+++++++++++++++++++++++++++++    +++++++++++++++++++++++++++++",
        "+   one +         +         +    +   one +         +         +",
        "+ digit + another +         +    + digit + another +         +",
        "+   int +     int +  floats +    +   int +     int +  floats +",
        "+++++++++++++++++++++++++++++    +++++++++++++++++++++++++++++",
        "+     1 +      29 +  3.5000 +    +     1 +      29 +  3.5000 +",
        "+++++++++++++++++++++++++++++    +++++++++++++++++++++++++++++",
        "+     4 +       5 + 16.3400 +    +     4 +       5 + 16.3400 +",
        "+++++++++++++++++++++++++++++    +++++++++++++++++++++++++++++",
    ])
    assert text == expected
