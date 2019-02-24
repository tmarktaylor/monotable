"""Assertion based test cases for monotable.table.MonoTable for pytest."""

from collections import namedtuple
import datetime
import doctest
import math
import pytest    # todo- mypy error no stub file

# For experimental type checking this file was annotated such that the command
# mypy test/test_examples.py --strict doesn't produce
# any output.  The :type ignore directive was added to prevent mypy errors
# that I was not able to fix.

# These imports are for PEP484, PYPI package mypy static type checking.
try:
    from typing import List, Any, Tuple, Iterable, Sequence
except ImportError:
    pass

import monotable.alignment
import monotable.plugin
import monotable.scanner
import monotable.table


def test_doctest_scanner_py():    # type: () -> None

    # mypy is expecting module=monotable.scanner, py -2 expects m=.
    failure_count, test_count = doctest.testmod(m=monotable.scanner)
    assert test_count > 0
    assert failure_count == 0


def test_py2_mono_extra_keyword_args():    # type: () -> None
    """
    Expect TypeError on unsupported keyword only arg 'bogus'.
    This test is only required for Python 2.7 code that manually tests for
    extra keyword only arguments.
    """

    with pytest.raises(TypeError) as exc_info:
        _ = monotable.mono(
            headings=(),
            formats=(),
            cellgrid=((),),
            title='',
            bogus='yes')
    print(exc_info.value)
    assert 'keyword' in str(exc_info.value)
    assert 'bogus' in str(exc_info.value)


def test_py2_monocol_extra_keyword_args():    # type: () -> None
    """
    Expect TypeError on unsupported keyword only arg 'bogus'.
    This test is only required for Python 2.7 code that manually tests for
    extra keyword only arguments.
    """

    column = ('', '', ())
    columns = (column, column)

    with pytest.raises(TypeError) as exc_info:
        _ = monotable.monocol(
            column_tuples=columns,
            title='',
            bogus='yes')
    print(exc_info.value)
    assert 'keyword' in str(exc_info.value)
    assert 'bogus' in str(exc_info.value)


def test_py2_mono_misspelled_cellgrid_keyword_arg():    # type: () -> None
    """
    Expect TypeError on keyword cells when intended to use cellgrid.
    This test is only required for Python 2.7 code that manually tests for
    extra keyword only arguments.
    """

    with pytest.raises(TypeError) as exc_info:
        _ = monotable.mono(
            headings=(),
            formats=(),
            cells=((),),    # error should be cellgrid
            title='')
    assert 'keyword' in str(exc_info.value)
    assert 'cells' in str(exc_info.value)


def test_simple_data_types():    # type: () -> None
    """Simple data types.

    Automatic justification.
    Numbers are right justified, all other types are left justified.
    Headings are justified per cell type in the first row.
    Floating point format defaults to '.6f' specified by the
    class variable default_float_format_spec.
    """

    headings = ['int', 'float', 'string', 'tuple']
    cells = [[123456789, math.pi, 'Hello World', (2, 3)],
             [2, math.e * 1000, 'another string', ('a', 'b')]]
    text = monotable.table.table(headings, [], cells)
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
    # type: () -> None
    """
    Show an attribute of an cell object and an item of a sequence.

    Change the instance format_func to monotable.plugin.sformat()
    by assigning it to the instance variable.

    Use align_spec '<' to left justify the title.
    Note that a cell passed to str.format() satisfies
    only the first replacement field of the Format String Syntax.
    """

    headings = ['x\nattrib.', 'y\nattrib.', '[0]\nindex', '[1]\nindex']
    formats = ['{.x}', '{.y}', '{[0]}', '{[1]}']
    t = monotable.table.MonoTable()
    # Could not get mypy to accept the class var format_func
    # so using ignore below.
    t.format_func = monotable.plugin.sformat    # type: ignore
    point = namedtuple('point', ['x', 'y'])
    cells = [[point(1, 91), point(2, 92), point(3, 93), point(4, 94)],
             [point(5, 95), point(6, 96), point(7, 97), point(8, 98)]]
    text = t.table(headings, formats, cells, title='<Select attribute/index.')
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

def test_float_and_boolean_formatting():    # type: () -> None
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
             [999.87654321,  1660,  None, False]]    # type: List[List[object]]

    title = 'Float, thousands, datetime, boolean formatting.'
    text = monotable.table.table(headings, formats, cells,
        title=title)

    expected = '\n'.join([
        "Float, thousands, datetime, boolean formatting.",
        "----------------------------------------------",
        "    float",
        "precision   units of  datetime         bool to",
        "        3  thousands  9/16/16           yes/no",
        "----------------------------------------------",
        "    1.235       35.2  week-37-day-260      yes",
        "  999.877        1.7                        no",
        "----------------------------------------------"
        ])
    assert text == expected

    text2 = monotable.mono(headings, formats, cells, title=title)
    assert text2 == expected


def test_malformed_boolean_format_spec():    # type: () -> None
    headings = ['boolean\nno comma', 'boolean\n2 commas']
    formats = ['(boolean)missing-comma', '(boolean)yes,no,maybe']
    cells = [[True, False], [False, True]]
    title = 'Messed up format specs.'
    text = monotable.table.table(headings, formats, cells, title=title)

    # Missing or extra comma in the boolean format spec is silently ignored.
    expected = '\n'.join([
        "Messed up format specs.",
        "------------------",
        " boolean   boolean",
        "no comma  2 commas",
        "------------------",
        "   fspec    !fspec",
        "  !fspec     fspec",
        "------------------"
        ])

    assert text == expected

    text2 = monotable.mono(headings, formats, cells, title=title)
    assert text2 == expected


def test_boolean_on_non_boolean_type_cells():    # type: () -> None
    """
    Check boolean format function directive with non-boolean cell type.

    True and False are
    """
    headings = ['', 'bad\nformat\ndirective']
    formats = ['>(boolean)on,off', '>(boolean)yes,no']
    empty_list = []
    non_empty_dict = {'spam': False}    # True truth value since non-empty dict
    cells = [[1,   empty_list],
             [0.0, non_empty_dict]]
    title = 'Non boolean cells.'
    text = monotable.table.table(headings, formats, cells, title=title)

    expected = '\n'.join([
        "Non boolean cells.",
        "--------------",
        "           bad",
        "        format",
        "     directive",
        "--------------",
        " on         no",
        "off        yes",
        "--------------"
        ])

    assert text == expected

    text2 = monotable.mono(headings, formats, cells, title=title)
    assert text2 == expected


def test_cotable_missing_cell():    # type: () -> None
    """Column 2 only has one cell."""
    d = datetime.datetime(2016, 9, 16)

    column0 = ('float\nprecision\n3', '.3f', [1.23456789, 999.87654321])    # type: Tuple[str, str, List[object]]
    column1 = ('units of\nthousands', '(thousands).1f', [35200, 1660])    # type: Tuple[str, str, List[object]]
    column2 = ('datetime\n9/16/16', 'week-%U-day-%j', [d])    # type: Tuple[str, str, List[object]]
    column3 = ('bool to\nyes/no', '(boolean)yes,no', [True, False])    # type: Tuple[str, str, List[object]]
    columns = [column0, column1, column2, column3]   # type: List[Tuple[str, str, List[object]]]

    title = 'Float, thousands, datetime, boolean formatting.'
    text = monotable.table.cotable(columns, title=title)


    expected = '\n'.join([
        "Float, thousands, datetime, boolean formatting.",
        "----------------------------------------------",
        "    float",
        "precision   units of  datetime         bool to",
        "        3  thousands  9/16/16           yes/no",
        "----------------------------------------------",
        "    1.235       35.2  week-37-day-260      yes",
        "  999.877        1.7                        no",
        "----------------------------------------------"
    ])
    assert text == expected

    text2 = monotable.monocol(columns, title=title)
    assert text2 == expected


def test_cotable_vr_col():    # type: () -> None
    """Add a vertical rule column to previous example."""
    d = datetime.datetime(2016, 9, 16)

    column0 = ('float\nprecision\n3', '.3f', [1.23456789, 999.87654321])    # type: Tuple[str, str, Iterable[object]]
    column1 = ('units of\nthousands', '(thousands).1f', [35200, 1660])    # type: Tuple[str, str, Iterable[object]]
    column2 = ('datetime\n9/16/16', 'week-%U-day-%j', [d])    # type: Tuple[str, str, Iterable[object]]
    column3 = ('bool to\nyes/no', '(boolean)yes,no', [True, False])    # type: Tuple[str, str, Iterable[object]]
    columns = [column0, column1, monotable.VR_COL, column2, column3]   # type: List[Tuple[str, str, Iterable[object]]]

    title = 'Float, thousands, datetime, boolean formatting.'
    text = monotable.table.cotable(columns, title=title)

    expected = '\n'.join([
        "Float, thousands, datetime, boolean formatting.",
        "-----------------------------------------------",
        "    float            |",
        "precision   units of | datetime         bool to",
        "        3  thousands | 9/16/16           yes/no",
        "-----------------------------------------------",
        "    1.235       35.2 | week-37-day-260      yes",
        "  999.877        1.7 |                       no",
        "-----------------------------------------------"
    ])
    assert text == expected
    text2 = monotable.monocol(columns, title=title)
    assert text2 == expected



def test_datetime():    # type: () -> None
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
    d = datetime.datetime(2016, 1, 10, 19, 35, 18)
    cells = [[d, d]]
    title = ('<=Formatting a datetime object '
             'datetime.datetime(2016, 1, 10, 19, 35, 18)')
    text = monotable.table.bordered_table(headings, formats, cells, title=title)
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

    text2 = monotable.mono(headings, formats, cells, title=title, bordered=True)
    assert text2 == expected

def test_millions_billions_trillions_formatting():    # type: () -> None
    headings = ['units of\nmillions',
                'units of\nbillions',
                'units of\ntrillions']

    formats = ['(millions).2f',
               '(billions).3f',
               '(trillions).0f']

    cells = [[37000000, 99457000000, -98654321456123],
             [-2123123, -123777000, 654000000000],
             [0, 0.0, 0]]    # type: List[List[object]]

    text = monotable.table.table(headings, formats, cells)

    expected = '\n'.join([
        "-----------------------------",
        "units of  units of   units of",
        "millions  billions  trillions",
        "-----------------------------",
        "   37.00    99.457        -99",
        "   -2.12    -0.124          1",
        "    0.00     0.000          0",
        "-----------------------------",
    ])
    assert text == expected

    text2 = monotable.mono(headings, formats, cells)
    assert text2 == expected

def test_milli_micor_nano_pico_formatting():    # type: () -> None
    headings = ['units of\nmilli',
                'units of\nmicro',
                'units of\nnano',
                'units of\npico']

    formats = ['(milli).2f',
               '(micro).3f',
               '(nano).3f',
               '(pico).0f']

    cells = [[0.24043, 0.240323e-3, 0.340001e-6, 3.250e-9]]

    text = monotable.table.table(headings, formats, cells)

    expected = '\n'.join([
        "--------------------------------------",
        "units of  units of  units of  units of",
        "   milli     micro      nano      pico",
        "--------------------------------------",
        "  240.43   240.323   340.001      3250",
        "--------------------------------------",
    ])
    assert text == expected

    text2 = monotable.mono(headings, formats, cells)
    assert text2 == expected

def test_kibi_mebi_gibi_tebi_formatting():    # type: () -> None
    headings = ['units of\nkibi',
                'units of\nmebi',
                'units of\ngibi',
                'units of\ntebi']

    formats = ['(kibi).0f',
               '(mebi).1f',
               '(gibi).1f',
               '(tebi).3f']

    cells = [[8200, 125.70 * 2**20, 0.175 * 2**30, 91.4504 * 2 ** 40]]

    text = monotable.table.table(headings, formats, cells)

    expected = '\n'.join([
        "--------------------------------------",
        "units of  units of  units of  units of",
        "    kibi      mebi      gibi      tebi",
        "--------------------------------------",
        "       8     125.7       0.2    91.450",
        "--------------------------------------",
    ])
    assert text == expected

    text2 = monotable.mono(headings, formats, cells)
    assert text2 == expected

def test_template_substitution_and_multiline():    # type: () -> None
    """Show values using string.Template substitution.  Show multi-line cells.

    Use format_option_spec for the second column to specify
    monotable.plugin.tformat() for that column.
    This invokes str.Template formatting for the column.
    Format a bordered table by calling bordered_table() instead of table().
    """
    headings = ['int', 'Formatted by str.Template()']
    formats = ['', '(tformat)name= $name\nage= $age\ncolor= $favorite_color']
    cells = [[2345, dict(name='Row Zero', age=888, favorite_color='blue')],
             [6789, dict(name='Row One', age=999, favorite_color='No! Red!')]]
    title = 'str.Template() Formatting.'
    text = monotable.table.bordered_table(headings, formats, cells, title)
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

    text2 = monotable.mono(headings, formats, cells, title=title, bordered=True)
    assert text2 == expected


def test_mapping_and_multiline():    # type: () -> None
    """Show values from a mapping using mformat().  Show multi-line cells.

    Use format_option_spec for the second column to specify
    monotable.plugin.mformat() for that column.
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
    title = 'mformat() Formatting.'
    text = monotable.table.bordered_table(headings, formats, cells, title=title)

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

    text2 = monotable.mono(headings, formats, cells, title=title, bordered=True)
    assert text2 == expected


def test_printf_style_with_tuple_format_and_subclass_for_format_func():
    # type: () -> None
    """Formatting with pformat printf-style String Formatting.

    Create a subclass of MonoTable that uses monotable.plugin.pformat as the
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

    # Could not get mypy to accept the class var format_func
    # so using ignore below.
    class CustomMonoTable(monotable.table.MonoTable):
        format_func = staticmethod(monotable.plugin.pformat)    # type: ignore

    t = CustomMonoTable()

    cells = [[123456789, math.pi, 'Hello World', (1, 2)],
             [2, math.e * 1000, 'another string', (3, 4)]]
    text = t.table(headings, formats, cells)
    expected = '\n'.join([
        "----------------------------------------------",
        "      int        float  string          tuple",
        "----------------------------------------------",
        "123456789     3.141593  Hello World     (1, 2)",
        "        2  2718.281828  another string  (3, 4)",
        "----------------------------------------------",
    ])
    assert text == expected


def test_horizontal_and_vertical_guidelines_and_indent():    # type: () -> None
    """Test horizontal and vertical rules, and table indent.

    Test the following:
    - Row starting with a HR.  The HR row has one cell.
    - Custom sep to create vertical rule after the first column specified
      by the option_spec of the first column.
    - Indent string placed at the start of every line.
    """

    headings = ['col-0', 'col-1']
    formats = ['(sep= | )']  # specify sep=' | ' between 1st and 2nd columns
    t = monotable.table.MonoTable(indent='*****')

    cells = [['time', '12:45'],
             ['place', 'home'],
             [monotable.table.HR],
             ['sound', 'bell'],
             ['volume', 'very loud']]    # type: List[List[object]]
    text = t.table(headings, formats, cells)
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

    text2 = monotable.mono(headings, formats, cells, indent='*****')
    assert text2 == expected


def test_width_format_option():    # type: () -> None
    """Limit the width of a column using width format option."""

    headings = ['Id Number', 'Duties', 'Start Date']
    formats = ['', '(width=15)']
    cells = [[1, 'President and CEO', '06/02/2016'],
             [2, 'Raise capital', '06/10/2016'],
             [3, 'Oversee day to day operations', '06/21/2016']]
    title = 'Limit center column to 15 characters.'
    text = monotable.table.table(headings, formats, cells, title=title)

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

    text2 = monotable.mono(headings, formats, cells, title=title)
    assert text2 == expected


def test_width_fixed_format_option():    # type: () -> None
    """Fix the width of a column using width format option.

    Look for 5 extra spaces after 1234567890123 and Raise capital."""

    headings = ['Id Number', 'Duties', 'Start Date']
    formats = ['', '(width=18;fixed)']
    cells = [[1, '1234567890123', '06/02/2016'],
             [2, 'Raise capital', '06/10/2016'],
             [3, 'Oversee day', '06/21/2016']]
    title = 'Fixed center column to 15 characters.'
    text = monotable.table.table(headings, formats, cells, title=title)
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

    text2 = monotable.mono(headings, formats, cells, title=title)
    assert text2 == expected

def test_width_fixed_format_option_with_none_and_missing_cells():    # type: () -> None
    """Fix the width of a column using width and fixed format options.

    Show that cell of value None and the empty cells added to a
    row that was missing cells are handled.
    Look for 5 extra spaces before 1234567890123 ."""

    headings = ['Id Number', 'Duties', 'Start Date']
    formats = ['', '>(width=18;fixed)']
    cells = [[1, '1234567890123', '06/02/2016'],
             [2, None, '06/10/2016'],
             [3]]    # type: List[List[object]]
    title = 'Fixed center column to 15 characters.'
    text = monotable.table.table(headings, formats, cells, title=title)
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

    text2 = monotable.mono(headings, formats, cells, title=title)
    assert text2 == expected


def test_width_fixed_right_justified_format_option():    # type: () -> None
    """Fix the width of a column using width and fixed format options.

    Look for 5 extra spaces before 1234567890123 and Raise capital."""

    headings = ['Id Number', 'Duties', 'Start Date']
    formats = ['', '>(width=18;fixed)']
    cells = [[1, '1234567890123', '06/02/2016'],
             [2, 'Raise capital', '06/10/2016'],
             [3, 'Oversee day', '06/21/2016']]
    title = 'Fixed center column to 15 characters.'
    text = monotable.table.table(headings, formats, cells, title=title)
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

    text2 = monotable.mono(headings, formats, cells, title=title)
    assert text2 == expected


def test_wrap_format_option():    # type: () -> None
    """Limit the width of a column using width and wrap format options.

    Note that the center column actually occupies 11 characters since no
    lines in the column wrapped to the full 12 characters.
    This looks reasonable without borders because the cell vertical align
    default is TOP.
    """

    headings = ['Id Number', 'Duties', 'Start Date']
    formats = ['', '(width=12;wrap)']
    cells = [[1, 'President and CEO', '06/02/2016'],
             [2, 'Raise capital', '06/10/2016'],
             [3, 'Oversee day to day operations', '06/21/2016']]
    title = 'Wrap center column to a maximum of 12 characters.'
    text = monotable.table.table(headings, formats, cells, title=title)
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

    text2 = monotable.mono(headings, formats, cells, title=title)
    assert text2 == expected

def test_fixed_wrap_format_option():    # type: () -> None
    """Limit the width of a column using width and wrap format options.

    Note that without the fixed option the center column wraps to 9
    characters.  Three spaces were added to pad out to 12 characters.
    """

    headings = ['Id Number', '123456789', 'Start Date']
    formats = ['', '(width=12;wrap;fixed)']
    cells = [[1, 'President President', '06/02/2016'],
             [2, 'Raise capital', '06/10/2016'],
             [3, 'Oversee Oversee', '06/21/2016']]
    title = 'Wrap center column to a fixed width 12 characters.'
    text = monotable.table.table(headings, formats, cells, title=title)
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

    text2 = monotable.mono(headings, formats, cells, title=title)
    assert text2 == expected


def test_fixed_wrap_right_justified_format_option():    # type: () -> None
    """Limit the width of a column using width and wrap format options.

    Note that without the fixed option the center column wraps to 9
    characters.  Three spaces were added at the start of the column
    to pad out to 12 characters.
    """

    headings = ['Id Number', '123456789', 'Start Date']
    formats = ['', '>(width=12;wrap;fixed)']
    cells = [[1, 'President President', '06/02/2016'],
             [2, 'Raise capital', '06/10/2016'],
             [3, 'Oversee Oversee', '06/21/2016']]
    title = 'Wrap center column to a fixed width 12 characters.  right.'
    text = monotable.table.table(headings, formats, cells, title=title)
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
    assert text == expected

    text2 = monotable.mono(headings, formats, cells, title=title)
    assert text2 == expected


def test_width_fixed_format_option_missing_cells():    # type: () -> None
    """Do fixed width on a column that is missing cells.

    Leave out the heading too and center justify.  Result should be an
    all space column that is 15 spaces wide.
    """

    headings = ['Id Number', 'Duties', 'Start Date']
    formats = ['', '(width=15)', '^(width=15;fixed)']
    # third column of cells is missing
    cells = [[1, 'President and CEO'],
             [2, 'Raise capital'],
             [3, 'Oversee day to day operations']]
    title = '<Limit center column to 15 characters.'
    text = monotable.table.table(headings, formats, cells, title=title)
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

    text2 = monotable.mono(headings, formats, cells, title=title)
    assert text2 == expected


def test_width_fixed_format_option_only_none_cells():    # type: () -> None
    """Do fixed width on a column that has only None.

    Leave out the heading too and center justify.  Result should be an
    all space column that is 15 spaces wide.
    """

    headings = ['Id Number', 'Duties']
    formats = ['', '(width=15)', '^(width=15;fixed)']
    # third column of cells is None
    cells = [[1, 'President and CEO', None],
             [2, 'Raise capital', None],
             [3, 'Oversee day to day operations', None]]
    title = '<Limit center column to 15 characters.'
    text = monotable.table.table(headings, formats, cells, title=title)
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

    text2 = monotable.mono(headings, formats, cells, title=title)
    assert text2 == expected


def test_zero_with_numbers_arbitrary_precision():    # type: () -> None
    """Check zero processing for numbers with non-default float precision."""
    headings = ['Numbers']
    formats = ['(zero =--).4f']    # test with space before equals sign
    cells = [[0],
             [1234567],
             [0.000000e+00],
             [1e-04],
             [1e-05],
             [-0],
             [-1234567],
             [-0.000000e+00],
             [-1e-04],
             [-1e-05],
            ]    # type: List[List[object]]
    title = 'zero processing for numbers at arbitrary precision.'
    text = monotable.mono(headings, formats, cells, title)
    expected = '\n'.join([
        "zero processing for numbers at arbitrary precision.",
        "-------------",
        "      Numbers",
        "-------------",
        "           --",
        " 1234567.0000",
        "           --",
        "       0.0001",
        "           --",
        "           --",
        "-1234567.0000",
        "           --",
        "      -0.0001",
        "           --",
        "-------------",
    ])
    assert text == expected


def test_zero_with_numbers_default_precision():  # type: () -> None
    """Check zero processing for numbers at default precision.

     '...' replacement.
     """

    headings = ['Numbers']
    formats = ['(zero=...)']
    cells = [[0],
             [8901],
             [0.000000e+00],
             [1e-06],
             [1e-07],    # rounded to 0 by default_float_format_spec.
             [-0],
             [-8901],
             [-0.000000e+00],
             [-1e-06],
             [-1e-07],  # rounded to 0 by default_float_format_spec.
            ]    # type: List[List[object]]
    title = 'zero processing for numbers at default precision.'
    text = monotable.mono(headings, formats, cells, title)
    expected = '\n'.join([
        "zero processing for numbers at default precision.",
        "---------",
        "  Numbers",
        "---------",
        "      ...",
        "     8901",
        "      ...",
        " 0.000001",
        "      ...",
        "      ...",
        "    -8901",
        "      ...",
        "-0.000001",
        "      ...",
        "---------",
    ])
    assert text == expected


def test_zero_and_thousands_with_numbers():  # type: () -> None
    """Check zero processing for numbers with (thousands). Empty replacement."""

    headings = ['Numbers']
    formats = ['(thousands;zero=).6f']
    cells = [[0],
             [8901],
             [0.000000e+00],
             [1e-03],
             [1e-04],
             [1e-07]]    # type: List[List[object]]    # rounded to 0 by format_spec='.6f'    # noqa: E501
    title = 'zero processing for numbers with (thousands).'
    text = monotable.mono(headings, formats, cells, title)
    expected = '\n'.join([
        "zero processing for numbers with (thousands).",
        "--------",
        " Numbers",
        "--------",
        "",
        "8.901000",
        "",
        "0.000001",
        "",
        "",
        "--------",
    ])
    assert text == expected


def test_zero_non_with_numbers():  # type: () -> None
    """Check zero processing for mostly non numbers. '--' replacement."""

    headings = ['Non-numbers']
    # '>' align_spec needed since strings auto-align to left.
    formats = ['>(zero=--)']
    cells = [[0],
             [-321],
             ['1234567'],
             ['-0.00'],
             ['a-string'],
             [tuple([3, 4])],
             [list()],
             [None]]    # type: List[List[object]]
    title = 'zero processing for non-numbers.'
    text = monotable.mono(headings, formats, cells, title)
    expected = '\n'.join([
        "zero processing for non-numbers.",
        "-----------",
        "Non-numbers",
        "-----------",
        "         --",    # cell is a number
        "       -321",
        "    1234567",
        "      -0.00",    # cell is not a number
        "   a-string",
        "     (3, 4)",
        "         []",
        "",               # note trailing spaces were trimmed
        "-----------",
    ])
    assert text == expected


def test_parentheses_mixed():  # type: () -> None
    """Check parentheses processing for mix of () and no ()."""

    headings = ['H', 'mixed ()', 'I']
    formats = ['', '(parentheses).4f', '']
    cells = [[3, 0, 'a'],
             [4, 8901, 'b'],
             [5, -1, 'c'],
             [6, -1e-03, 'd'],
             [7, -8901, 'e'],
             [8, 1, 'f']]
    title = 'parentheses processing.'
    text = monotable.mono(headings, formats, cells, title)
    expected = '\n'.join([
        "parentheses processing.",
        "-----------------",
        "H     mixed ()  I",
        "-----------------",
        "3      0.0000   a",
        "4   8901.0000   b",
        "5     (1.0000)  c",
        "6     (0.0010)  d",
        "7  (8901.0000)  e",
        "8      1.0000   f",
        "-----------------",
    ])
    assert text == expected


def test_parentheses_all():  # type: () -> None
    """Check parentheses processing for all ()."""

    headings = ['H', 'all ()', 'I']
    formats = ['', '(parentheses).4f', '']
    cells = [[3, -10, 'a'],
             [4, -8901, 'b'],
             [5, -1, 'c'],
             [6, -1e-03, 'd'],
             [7, -8901, 'e'],
             [8, -1, 'f']]
    title = 'parentheses processing all ().'
    text = monotable.mono(headings, formats, cells, title)
    expected = '\n'.join([
        "parentheses processing all ().",
        "-----------------",
        "H       all ()  I",
        "-----------------",
        "3    (10.0000)  a",
        "4  (8901.0000)  b",
        "5     (1.0000)  c",
        "6     (0.0010)  d",
        "7  (8901.0000)  e",
        "8     (1.0000)  f",
        "-----------------",
    ])
    assert text == expected


def test_parentheses_none():  # type: () -> None
    """Check parentheses processing for no ()."""

    headings = ['H', 'no ()', 'I']
    formats = ['', '(parentheses).4f', '']
    cells = [[3, 10, 'a'],
             [4, 8901, 'b'],
             [5, 1, 'c'],
             [6, 1e-03, 'd'],
             [7, 8901, 'e'],
             [8, 1, 'f']]
    title = 'parentheses processing no ().'
    text = monotable.mono(headings, formats, cells, title)
    expected = '\n'.join([
        "parentheses processing no ().",
        "---------------",
        "H      no ()  I",
        "---------------",
        "3    10.0000  a",
        "4  8901.0000  b",
        "5     1.0000  c",
        "6     0.0010  d",
        "7  8901.0000  e",
        "8     1.0000  f",
        "---------------",
    ])
    assert text == expected


def test_parentheses_ignores_string_numeric_literals():  # type: () -> None
    """Check parentheses processing ignores strings that look like numbers.

    Note that the (9) auto-aligns to the right since the cell type is a number.
    """

    headings = ['H', 'str', 'I']
    formats = ['', '(parentheses)', '']
    cells = [[3, '-10', 'a'],
             [4, '8901', 'b'],
             [5, -9, 'c'],
             [6, '-1e-03', 'd'],
             [7, '-8901', 'e'],
             [8, '1', 'f']]
    title = 'parentheses processing strings.'
    text = monotable.mono(headings, formats, cells, title)
    expected = '\n'.join([
        "parentheses processing strings.",
        "------------",
        "H  str     I",
        "------------",
        "3  -10     a",
        "4  8901    b",
        "5     (9)  c",
        "6  -1e-03  d",
        "7  -8901   e",
        "8  1       f",
        "------------",
    ])
    assert text == expected


def test_none_directive():  # type: () -> None
    """Check none directive.

    Since None auto-aligns to left, add '>' align spec prefix to the
    column format string.

    The second column cells contain None items but there is no none=
    directive so None renders as empty string.
    """

    headings = ['none', 'hh']
    formats = ['>(none=n/a).2f', '']
    cells = [[None, 2],
             [0, 'ab'],
             [2134567, 0],
             [-1, None],
             [None, None],
             [987.543, -1],
             [-8901, 100],
             [None, 0]]    # type: List[List[object]]
    title = 'Check none directive.'
    text = monotable.mono(headings, formats, cells, title)
    expected = '\n'.join([
        "Check none directive.",
        "---------------",
        "      none   hh",
        "---------------",
        "       n/a    2",
        "      0.00  ab",
        "2134567.00    0",
        "     -1.00",
        "       n/a",
        "    987.54   -1",
        "  -8901.00  100",
        "       n/a    0",
        "---------------",
    ])
    assert text == expected


def test_lsep_ignored_on_first_column():  # type: () -> None
    """lsep on first column is silently ignored."""
    headings = ['h1', 'h2', 'h3']
    formats = ['(lsep=.!.)']
    cells = [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']]
    text = monotable.mono(
        headings, formats, cells, title='lsep 1st col')
    expected = '\n'.join([
        "lsep 1st col",
        "----------",
        "h1  h2  h3",
        "----------",
        "A   B   C",
        "D   E   F",
        "G   H   I",
        "----------",
    ])
    assert text == expected


def test_rsep_ignored_on_last_column():  # type: () -> None
    """rsep on last column is silently ignored."""
    headings = ['h1', 'h2', 'h3']
    formats = ['', '', '(rsep=.!.)']
    cells = [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']]
    text = monotable.mono(
        headings, formats, cells, title='lsep 1st col')
    expected = '\n'.join([
        "lsep 1st col",
        "----------",
        "h1  h2  h3",
        "----------",
        "A   B   C",
        "D   E   F",
        "G   H   I",
        "----------",
    ])
    assert text == expected


def test_lsep():  # type: () -> None
    """lsep on second column."""
    headings = ['h1', 'h2', 'h3']
    formats = ['', '(lsep=.!.)']
    cells = [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']]
    text = monotable.mono(
        headings, formats, cells, title='lsep')
    expected = '\n'.join([
        "    lsep",
        "-----------",
        "h1.!.h2  h3",
        "-----------",
        "A .!.B   C",
        "D .!.E   F",
        "G .!.H   I",
        "-----------",
    ])
    assert text == expected


def test_rsep_on_first_column():  # type: () -> None
    """rsep on first column."""
    headings = ['h1', 'h2', 'h3']
    formats = ['(rsep=-I-)']
    cells = [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']]
    text = monotable.mono(
        headings, formats, cells, title='rsep')
    expected = '\n'.join([
        "    rsep",
        "-----------",
        "h1-I-h2  h3",
        "-----------",
        "A -I-B   C",
        "D -I-E   F",
        "G -I-H   I",
        "-----------",
    ])
    assert text == expected


def test_lsep_on_last_column():  # type: () -> None
    """lsep on last column."""
    headings = ['h1', 'h2', 'h3']
    formats = ['', '', '(lsep=xDy)']
    cells = [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']]
    text = monotable.mono(
        headings, formats, cells, title='lsep')
    expected = '\n'.join([
        "    lsep",
        "-----------",
        "h1  h2xDyh3",
        "-----------",
        "A   B xDyC",
        "D   E xDyF",
        "G   H xDyI",
        "-----------",
    ])
    assert text == expected


def test_lsep_supersedes_previous_rsep():  # type: () -> None
    """rsep on first column superseded by lsep on second column."""
    headings = ['h1', 'h2', 'h3']
    formats = ['(rsep=XXXXX)', '(lsep=.!.)']
    cells = [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']]
    text = monotable.mono(
        headings, formats, cells, title='rsep<lsep')
    expected = '\n'.join([
        " rsep<lsep",
        "-----------",
        "h1.!.h2  h3",
        "-----------",
        "A .!.B   C",
        "D .!.E   F",
        "G .!.H   I",
        "-----------",
    ])
    assert text == expected


def test_lsep_and_rsep():  # type: () -> None
    """lsep and rsep on the same column (like VR_COLUMN)."""
    headings = ['h1', 'h2', 'h3']
    formats = ['', '(lsep=|| ;rsep= !!)']
    cells = [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']]
    text = monotable.mono(
        headings, formats, cells, title='lsep and rsep')
    expected = '\n'.join([
        "lsep and rsep",
        "------------",
        "h1|| h2 !!h3",
        "------------",
        "A || B  !!C",
        "D || E  !!F",
        "G || H  !!I",
        "------------",
    ])
    assert text == expected


def test_auto_align_mixed_cell_types_in_column():    # type: () -> None
    """Check auto alignment when a column has numeric and non-numeric types."""

    headings = ['Number', 'Mixed', 'Non-Number']
    cells = [[1, 11002233, 'a-string'],
             [2, 'Spam!', None],
             [33, 444, 'abc']]
    title = 'Different cell types in middle column.'
    text = monotable.table.table(headings, [], cells, title)
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

    text2 = monotable.mono(headings, [], cells, title=title)
    assert text2 == expected


def test_max_cell_height():    # type: () -> None
    """Limit the maximum height of cells in the previous table.

    This truncates the Duties column at the bottom of the table.
    Note that the center column actually occupies 11 characters since no
    lines in the column wrapped to the full 12 characters.
    """

    headings = ['Id Number', 'Duties', 'Start Date']
    formats = ['', '(width=12;wrap)']
    t = monotable.table.MonoTable()
    t.max_cell_height = 2              # override class var
    cells = [[1, 'President and CEO', '06/02/2016'],
             [2, 'Raise capital', '06/10/2016'],
             [3, 'Oversee day to day operations', '06/21/2016']]
    title = ('Wrap center column to a maximum of 12 characters.\n'
             'Limit cell height to 2 lines')
    text = t.table(headings, formats, cells, title=title)
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


def test_bordered_format():    # type: () -> None
    """Add borders to the table from test_max_cell_height()."""

    headings = ['Id Number', 'Duties', 'Start Date']
    formats = ['', '(width=12;wrap)']
    cells = [[1, 'President and CEO', '06/02/2016'],
             [2, 'Raise capital', '06/10/2016'],
             [3, 'Oversee day to day operations', '06/21/2016']]
    t = monotable.table.MonoTable()
    t.max_cell_height = 2
    title = ('Wrap center column to a maximum of 12 characters.\n'
             'Limit cell height to 2 lines.\n'
             'Format with borders.')
    text = t.bordered_table(headings, formats, cells, title=title)
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


def test_cobordered_table_missing_cell():    # type: () -> None
    """Column 2 only has one cell."""
    d = datetime.datetime(2016, 9, 16)

    column0 = ('float\nprecision\n3', '.3f',[1.23456789, 999.87654321])
    column1 = ('units of\nthousands', '(thousands).1f', [35200, 1660])
    column2 = ('datetime\n9/16/16', 'week-%U-day-%j', [d])
    column3 = ('bool to\nyes/no', '(boolean)yes,no', [True, False])
    columns = [column0, column1, column2, column3]    # type: List[Tuple[str, str, List[Any]]]

    title = 'Float, thousands, datetime, boolean formatting.'
    text = monotable.table.cobordered_table(columns, title=title)

    expected = '\n'.join([
        "   Float, thousands, datetime, boolean formatting.",
        "+-----------+-----------+-----------------+---------+",
        "|     float |           |                 |         |",
        "| precision |  units of | datetime        | bool to |",
        "|         3 | thousands | 9/16/16         |  yes/no |",
        "+===========+===========+=================+=========+",
        "|     1.235 |      35.2 | week-37-day-260 |     yes |",
        "+-----------+-----------+-----------------+---------+",
        "|   999.877 |       1.7 |                 |      no |",
        "+-----------+-----------+-----------------+---------+",
    ])
    assert text == expected

    text2 = monotable.monocol(columns, title=title, bordered=True)
    assert text2 == expected


def test_user_defined_format_function():    # type: () -> None
    """Set a user defined format function in the 3rd column.

    Right justify the title by prefixing with '>'.
    """

    def show_last_four(string_value, format_spec):
        # type: (str, str) -> str
        _ = format_spec
        formatted_text = '*' * (len(string_value) - 4) + string_value[-4:]
        return formatted_text

    myformatfuncmap = {'show_last_four': show_last_four}
    headings = ['Id Number', 'Duties', 'Sensitive\nInfo']
    formats = ['', '', '(show_last_four)']

    class CustomMonoTable(monotable.table.MonoTable):
        format_func_map = myformatfuncmap    # type: ignore
    t = CustomMonoTable()
    cells = [[1, 'President and CEO', '123'],
             [2, 'Raise capital', '12345'],
             [3, 'Oversee day to day operations', '123-45-6789']]
    text = t.table(headings, formats, cells,
                   title='>User defined format function.')
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

    text2 = monotable.mono(
        headings, formats, cells,
        title='>User defined format function.',
        format_func_map=myformatfuncmap)
    assert text2 == expected


def test_example_guideline_chars_and_right_align():    # type: () -> None
    """Omit bottom guideline, change others, right align left column.

    Right align the left column, the None cell string 'rest' should be
    right aligned.
    """

    headings = ['purchased\nparrot\nheart\nrate', 'life\nstate']
    # > is needed to right align None cell since it auto-aligns to left.
    # monotable uses empty string to format the second column.
    formats = ['>(none=rest).0f']
    cells = [[0, 'demised'],
             [0.0, 'passed on'],
             [None, 'is no more'],
             [-1],
             [0, 'ceased to be']]    # type: List[List[object]]
    text = monotable.mono(
        headings, formats, cells,
        title='Complaint\n(registered)',
        # top guideline is equals, heading is period, bottom is omitted.
        guideline_chars='=. ')
    expected = '\n'.join([
        "       Complaint",
        "      (registered)",
        "=======================",
        "purchased",
        "   parrot",
        "    heart  life",
        "     rate  state",
        ".......................",
        "        0  demised",
        "        0  passed on",
        "     rest  is no more",
        "       -1",
        "        0  ceased to be"
    ])
    assert text == expected


def test_default_float_format_spec():    # type: () -> None
    """Change default_float_format_spec.

    Do a different float precision in each column.
    Rounding occurs in the last two columns.
    """

    cells = [[9.1234567] * 4]
    headings = ['.1f', '.3f', '.5f', 'default=.4f']
    formats = ['.1f', '.3f', '.5f']
    t = monotable.table.MonoTable()
    t.default_float_format_spec = '.4f'
    title = 'Different float precision in each column.'
    text = t.table(headings, formats, cells, title=title)
    expected = '\n'.join([
        "Different float precision in each column.",
        "--------------------------------",
        ".1f    .3f      .5f  default=.4f",
        "--------------------------------",
        "9.1  9.123  9.12346       9.1235",
        "--------------------------------",
    ])
    assert text == expected


def test_disable_default_float_format_spec():    # type: () -> None
    """Disable default_float_format_spec feature by setting to ''.

    The 4th column has the same float precision as the cell value.
    """

    cells = [[9.1234567] * 4]
    headings = ['.1f', '.3f', '.5f', 'disable\ndefault_float_format_spec']
    formats = ['.1f', '.3f', '.5f']
    t = monotable.table.MonoTable()
    t.default_float_format_spec = ''
    title = '<Disable default in last column.'
    text = t.table(headings, formats, cells, title=title)
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


def test_override_format_none_as_with_auto_alignment():    # type: () -> None
    """Override class variable format_none_as."""

    class CustomMonoTable(monotable.table.MonoTable):
        format_none_as = 'NONE!'

    headings = ['number', 'Life\nState']
    t = CustomMonoTable()
    cells = [[22334455, 'demised'],
             [66, 'passed on'],
             [None, 'is no more'],
             [9, None],
             [10, 'ceased to be']]    # type: List[List[object]]
    text = t.table(headings, [], cells, '<format_none_as')
    expected = '\n'.join([
        "format_none_as",
        "----------------------",
        "          Life",
        "  number  State",
        "----------------------",
        "22334455  demised",
        "      66  passed on",
        "NONE!     is no more",
        "       9  NONE!",
        "      10  ceased to be",
        "----------------------",
    ])
    assert text == expected

def test_override_format_none_as_with_format_align_specs():    # type: () -> None
    """Override class variable format_none_as, force right align.

    Right align the left column, the None cell string should be
    right aligned.
    """

    headings = ['number', 'Life\nState']
    formats = ['>']     # force None cell to right align
    t = monotable.table.MonoTable()
    t.format_none_as = '0-0'
    cells = [[22334455, 'demised'],
             [66, 'passed on'],
             [None, 'is no more'],
             [9, None],
             [10, 'ceased to be']]    # type: List[List[object]]
    text = t.table(headings, formats, cells, '<format_none_as')
    expected = '\n'.join([
        "format_none_as",
        "----------------------",
        "          Life",
        "  number  State",
        "----------------------",
        "22334455  demised",
        "      66  passed on",
        "     0-0  is no more",
        "       9  0-0",
        "      10  ceased to be",
        "----------------------",
    ])
    assert text == expected

def test_heading_left_align_spec_and_format_left_align_spec():    # type: () -> None
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
    t = monotable.table.MonoTable()
    t.default_float_format_spec = '.4f'
    title = 'Different float precision in each column.'
    text = t.table(headings, formats, cells, title=title)
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


def test_heading_center_align_spec_and_format_center_align_spec():    # type: () -> None
    """Test center align_spec.

    Test heading align follows format center align_spec in column 2.
    Test heading align follows heading center align_spec in column 3.
    """

    cells = [[9.1234567] * 4]
    headings = ['.1f', '.3f', '^.5f', 'default=.4f']
    formats = ['.1f', '^.3f', '.5f']
    t = monotable.table.MonoTable()
    t.default_float_format_spec = '.4f'
    title = 'Different float precision in each column.'
    text = t.table(headings, formats, cells, title=title)
    expected = '\n'.join([
        "Different float precision in each column.",
        "--------------------------------",
        ".1f   .3f     .5f    default=.4f",
        "--------------------------------",
        "9.1  9.123  9.12346       9.1235",
        "--------------------------------",
    ])
    assert text == expected


def test_heading_and_format_right_align_spec():    # type: () -> None
    """Show default_float_format_spec with right align_spec.

    Subclass MonoTable and override the class var default_float_format_spec.
    Note the headings are right justified.
    """
    cells = [[9.1234567] * 4]
    headings = ['.1f', '.3f', '>.5f', 'default=.4f']
    formats = ['.1f', '>.3f', '.5f']

    class FloatPoint4MonoTable(monotable.table.MonoTable):
        default_float_format_spec = '.4f'
    t = FloatPoint4MonoTable()
    text = t.table(headings, formats, cells,
                   title='Different float precision in each column.')
    expected = '\n'.join([
        "Different float precision in each column.",
        "--------------------------------",
        ".1f    .3f      .5f  default=.4f",
        "--------------------------------",
        "9.1  9.123  9.12346       9.1235",
        "--------------------------------",
    ])
    assert text == expected


def test_override_align_spec_chars():    # type: () -> None
    """Change the class var align_spec_chars on an instance.

    This works as long as noe of the headings, formats, and title start
    with one of the new align_spec_chars.
    """

    cells = [[123, 'import', 4567, 'this']]
    headings = ['an int', 'string', 'another int', 'another string']
    formats = ['R', '', 'L', 'C']
    t = monotable.table.MonoTable()
    t.align_spec_chars = 'LCR'
    text = t.table(headings, formats, cells, title='RUser align_spec_chars.')
    expected = '\n'.join([
        "                     User align_spec_chars.",
        "-------------------------------------------",
        "an int  string  another int  another string",
        "-------------------------------------------",
        "   123  import  4567              this",
        "-------------------------------------------",
    ])
    assert text == expected


def test_override_title_wrap_spec_char():    # type: () -> None
    """Change the class var wrap_spec_char on an instance.

    The [wrap_spec] in the title selects textwrap.
    The table title is interpreted as [align_spec][wrap_spec]string.
    """

    cells = [[123, 'import']]
    headings = ['an int', 'a string']
    t = monotable.table.MonoTable()
    t.wrap_spec_char = '$'
    text = t.table(headings, [], cells,
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


def test_override_heading_valign():    # type: () -> None
    """Change the class var heading_valign on an instance.

    heading_valign controls vertical alignment of headings.
    """

    cells = [[123, 'import']]
    headings = ['a\nshort\nint', 'a\nslightly\nlonger\nstring']
    t = monotable.table.MonoTable()
    t.heading_valign = monotable.alignment.TOP
    text = t.table(headings, [], cells, title='instance.heading_valign = TOP')
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


def test_override_guideline_chars():    # type: () -> None
    """Change all three guideline chars."""

    cells = [[123, 'import', 4567, 'this']]
    headings = ['an int', 'string', 'another int', 'another string']
    formats = ['>', '', '<', '^']
    t = monotable.table.MonoTable()
    guidelines = 'X=*'
    t.guideline_chars = guidelines
    title = '>User guideline_chars.'
    text = t.table(headings, formats, cells, title=title)
    expected = '\n'.join([
        "                      User guideline_chars.",
        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "an int  string  another int  another string",
        "===========================================",
        "   123  import  4567              this",
        "*******************************************",
    ])
    assert text == expected

    text2 = monotable.mono(headings, formats, cells, title=title,
                           guideline_chars=guidelines)
    assert text2 == expected


def test_override_separated_guidelines():    # type: () -> None
    class SeparatedMonoTable(monotable.table.MonoTable):
        separated_guidelines = True
        guideline_chars = '==='

    headings = ['option name', 'format function', 'description']
    t = SeparatedMonoTable()

    cells = [['mformat', 'monotable.plugin.mformat',
              'mapping with str.format()'],
             ['pformat', 'monotable.plugin.pformat', 'printf style'],
             ['sformat', 'monotable.plugin.sformat', 'str.format()'],
             ['tformat', 'monotable.plugin.tformat', 'string.Template()'],
             ['function-name', '--', 'user defined function']]

    text = t.table(headings, [], cells)
    expected = '\n'.join([
        "=============  ========================  =========================",
        "option name    format function           description",
        "=============  ========================  =========================",
        "mformat        monotable.plugin.mformat  mapping with str.format()",
        "pformat        monotable.plugin.pformat  printf style",
        "sformat        monotable.plugin.sformat  str.format()",
        "tformat        monotable.plugin.tformat  string.Template()",
        "function-name  --                        user defined function",
        "=============  ========================  =========================",
    ])
    assert text == expected


def test_override_separated_guidelines_no_bottom_guideline():    # type: () -> None
    """Test separated guideline style with no bottom guideline."""

    class SeparatedMonoTable(monotable.table.MonoTable):
        guideline_chars = '== '    # disable bottom guideline
        separated_guidelines = True

    cells = [[123, 'import', 4567, 'this']]
    headings = ['an int', 'string', 'another int', 'another string']
    formats = ['>', '', '<', '^']
    t = SeparatedMonoTable()
    text = t.table(headings, formats, cells, title='>separated_guidelines = True.')
    expected = '\n'.join([
        "               separated_guidelines = True.",
        "======  ======  ===========  ==============",
        "an int  string  another int  another string",
        "======  ======  ===========  ==============",
        "   123  import  4567              this",
    ])
    assert text == expected


def test_omit_top_and_bottom_guidelines():    # type: () -> None
    """Override guideline_chars to omit top and bottom guidelines."""

    guidelines = ' = '
    class CustomMonoTable(monotable.table.MonoTable):
        guideline_chars = guidelines

    cells = [[123, 'import', 4567, 'this']]
    headings = ['an int', 'string', 'another int', 'another string']
    formats = ['>', '', '<', '^']

    t = CustomMonoTable()
    title = '<No top, bottom guidelines.'
    text = t.table(headings, formats,cells, title=title)

    expected = '\n'.join([
        "No top, bottom guidelines.",
        "an int  string  another int  another string",
        "===========================================",
        "   123  import  4567              this",
    ])
    assert text == expected

    text2 = monotable.mono(headings, formats, cells, title=title,
                           guideline_chars=guidelines)
    assert text2 == expected

def test_top_guideline_is_dots_and_only_guideline():    # type: () -> None
    """Omit heading and bottom guidelines.  Top guideline is '.'"""

    guidelines = '.'
    class CustomMonoTable(monotable.table.MonoTable):
        guideline_chars = guidelines

    cells = [[123, 'import', 4567, 'this']]
    headings = ['an int', 'string', 'another int', 'another string']
    formats = ['>', '', '<', '^']
    t = CustomMonoTable()
    title = '^Top guideline is .s, no others.'
    text = t.table(headings, formats, cells, title=title)

    expected = '\n'.join([
        "      Top guideline is .s, no others.",
        "...........................................",
        "an int  string  another int  another string",
        "   123  import  4567              this",
    ])
    assert text == expected

    text2 = monotable.mono(headings, formats, cells, title=title,
                           guideline_chars=guidelines)
    assert text2 == expected


def test_override_cell_vertical_alignment_to_center_top():    # type: () -> None
    """Change cell vertical alignment to CENTER_TOP."""

    class CustomMonoTable(monotable.table.MonoTable):
        cell_valign = monotable.alignment.CENTER_TOP

    cells = [['A\n4\nline\ncell', '3\nline\ncell', '2 line\ncell'],
             [monotable.table.HR],
             ['A\nfour\nline\ncell', 'three\nline\ncell', 'two line\ncell']]    # type: List[List[object]]
    headings = ['4 line cells', '3 line cells', '2 line cells']
    t = CustomMonoTable()
    text = t.table(headings, [], cells, title='cell_valign=CENTER_TOP')
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


def test_override_cell_vertical_alignment_to_center_bottom():    # type: () -> None
    """Change cell vertical alignment to CENTER_BOTTOM."""

    class CustomMonoTable(monotable.table.MonoTable):
        cell_valign = monotable.alignment.CENTER_BOTTOM

    cells = [['A\n4\nline\ncell', '3\nline\ncell', '2 line\ncell'],
             [monotable.table.HR],
             ['A\nfour\nline\ncell', 'three\nline\ncell', 'two line\ncell']]    # type: List[List[object]]
    headings = ['4 line cells', '3 line cells', '2 line cells']

    t = CustomMonoTable()
    text = t.table(headings, [], cells, title='cell_valign=CENTER_BOTTOM')
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
    # type: () -> None
    """Show truncation of too long lines and too tall cell.

    Change the more_marker to '**'.
    Limit cell height to 2 lines.  Limit column 2 width to 2 characters.
    Note that a column width is max(widest heading line, width=N).  In other
    words a wide heading for a column supersedes a width=N specified width.
    Bottom center cell first line is truncated to 3 characters.  The 4
    cells in the first and second columns are limited to two line height.
    """

    class CustomMonoTable(monotable.table.MonoTable):
        more_marker = '**'
        max_cell_height = 2

    cells = [['A\n4\nline\ncell', '3\nline\ncell', '2 line\ncell'],
             [monotable.table.HR],
             ['A\nfour\nline\ncell', 'three\nline\ncell', 'two line\ncell']]    # type: List[List[object]]
    headings = ['4 line', '3', '2 line']
    formats = ['', '(width=3)', '']

    t = CustomMonoTable()
    text = t.table(headings, formats, cells,
                   title="max_cell_height=2, more_marker='**'")
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


def test_comma_format_spec():    # type: () -> None
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
    cells = [[123456789, pi, 'Hello\nWorld', (2, 3)],
             [2, e * 1000, 'another string']]
    title = 'Centered Title Line.'
    text = monotable.table.table(headings, formats, cells, title=title)
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

    text2 = monotable.mono(headings, formats, cells, title=title)
    assert text2 == expected


def test_default_when_override_border_chars_to_empty_string():    # type: () -> None
    """Override class var border_chars to empty string.

    '+' is the hard coded default used for missing border_chars.
    """
    headings = ['one\ndigit\nint', 'another\nint', 'floats']
    t = monotable.table.MonoTable()
    t.border_chars = ''
    cells = [[1, 29, 3.5], [4, 5, 16.34]]
    text = t.bordered_table(headings, [], cells,
                            '^centered caption\njust 2 lines')
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


def test_override_border_chars():    # type: () -> None
    """Change border_chars to 'TBSCH'

    TBSCH corresponds to top, bottom, sides, corner, heading guideline.
    """

    headings = ['one\ndigit\nint', 'another\nint', 'floats']
    t = monotable.table.MonoTable()
    t.border_chars = 'TBSCH'
    cells = [[1, 29, 3.5], [4, 5, 16.34]]
    text = t.bordered_table(headings, [], cells,
                            '^centered caption\njust 2 lines')
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


def test_override_hmargin_vmargin():    # type: () -> None
    """Change class variables hmargin and vmargin in subclass."""

    class BigMarginMonoTable(monotable.table.MonoTable):
        hmargin = 3
        vmargin = 2

    headings = ['one\ndigit\nint', 'another\nint', 'floats']
    t = BigMarginMonoTable()
    cells = [[1, 29, 3.5], [4, 5, 16.34]]
    text = t.bordered_table(headings, [], cells, '<hmargin=3, vmargin=2')
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


def test_tile_four_tables_together():    # type: () -> None
    """Tile tables together.

    Create a string for each of the 3 tables.  One for upper left, one for
    upper right, and two copies of a 3rd table for the bottom row.
    Guidelines are omitted between the tiles.  The guidelines in the result
    are from the component tables ta, tb, and tc.

    Tiled table:   ta  tb
                   tc  tc
    """

    headings = ['4 line cells', '3 line cells']

    class CenterBottomMonoTable(monotable.table.MonoTable):
        cell_valign = monotable.alignment.CENTER_BOTTOM

    ta = CenterBottomMonoTable()
    cells0 = [['A\n4\nline\ncell', '3\nline\ncell'],
              [monotable.table.HR],
              ['A\nfour\nline\ncell', 'three\nline\ncell']]    # type: List[List[object]]
    taf = ta.table(headings, [], cells0, title='vertical align CENTER_BOTTOM')

    headings = ['4 line', '3', '2 line']
    formats = ['', '(width=3)', '']

    class CustomMonoTable(monotable.table.MonoTable):
        more_marker = '**'
        max_cell_height = 2

    tb = CustomMonoTable()
    cells1 = [['A\n4\nline\ncell', '3\nline\ncell', '2 line\ncell'],
              [monotable.table.HR],
              ['A\nfour\nline\ncell', 'three\nline\ncell', 'two line\ncell']]    # type: List[List[object]]
    tbf = tb.table(headings, formats, cells1, title="max_cell_height=2")

    headings = ['one\ndigit\nint', 'another\nint', 'floats']

    class BadBorderCharsFloat4fMonoTable(monotable.table.MonoTable):
        border_chars = ''
        default_float_format_spec = '.4f'

    tc = BadBorderCharsFloat4fMonoTable()
    cells2 = [[1, 29, 3.5], [4, 5, 16.34]]    # type: List[List[object]]
    tcf = tc.bordered_table(headings, [], cells2, '^centered title\n of 2 lines')

    class NoGuidelinesMonoTable(monotable.table.MonoTable):
        guideline_chars = ''
        sep = '    '

    tiled = NoGuidelinesMonoTable()
    cells3 = [[taf, tbf],
              [None, None],  # to insert space between the top and bottom rows
              # same table twice in the bottom row
              [tcf, tcf]]    # type: List[List[object]]
    text = tiled.table([], [], cells3)
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
