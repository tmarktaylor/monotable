"""Assertion based test cases for monotable.table.MonoTable for pytest."""

from collections import namedtuple
from os import path
import re

import pytest

import monotable
import monotable.plugin
import monotable.table


def read_file(*path_components):
    """Read a text file from the source tree into a string.

    The path is relative to the directory containing this file.
    """
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, *path_components)) as f:
        return f.read()


class TestConsistentVersionStrings:
    """Verify same release version string in all places.

    Obtain the version string from various places in the source tree
    and check that they are all the same.
    This test does not prove the version is correct.

    Whitespace around the equals sign in the version statement IS significant.
    """
    auth_version = monotable.__version__    # authoritative

    def test_setup_py_version(self):
        # -------------------------------------------------------
        # setup.py
        # example: version='0.1.0',
        setup_text = read_file('..', 'setup.py')
        match = re.search(r" *version=['\"]([^'\"]*)['\"]", setup_text, re.M)
        assert match.group(1) == self.auth_version

    def test_conf_py_version_and_release(self):
        # -------------------------------------------------------
        # conf.py
        # example:
        # # The short X.Y version.
        # version = u'0.1.0'
        conf_text = read_file('..', 'doc', 'conf.py')
        match = re.search(r"^version = u['\"]([^'\"]*)['\"]", conf_text, re.M)
        assert match.group(1) == self.auth_version

        # conf.py
        # example:
        # # The full version, including alpha/beta/rc tags.
        # release = u'0.1.0'
        match = re.search(r"^release = u['\"]([^'\"]*)['\"]", conf_text, re.M)
        assert match.group(1) == self.auth_version

    def test_index_rst_version(self):
        # -------------------------------------------------------
        # index.rst
        # example:
        # monotable version 1.0.1.
        # Note the final period is required.
        index_text = read_file('..', 'doc', 'index.rst')
        version_re = re.compile(r"monotable version (\d+\.\d+\.\d+)\.", re.M)
        match = version_re.search(index_text)
        assert match.group(1) == self.auth_version

        """make sure we properly match possible future versions."""
        v1 = 'monotable version 10.0.1.'
        m1 = version_re.search(v1)
        assert m1.group(1) == '10.0.1'

        v2 = 'monotable version 1.11.1.'
        m2 = version_re.search(v2)
        assert m2.group(1) == '1.11.1'

        v3 = 'monotable version 1.0.11.'
        m3 = version_re.search(v3)
        assert m3.group(1) == '1.0.11'

        v4 = 'monotable version 12.34.56.'
        m4 = version_re.search(v4)
        assert m4.group(1) == '12.34.56'

        # make sure we don't match bogus version strings.
        v5 = 'monotable version 12.34.56'  # no period
        m5 = version_re.search(v5)
        assert m5 is None

        v6 = 'monotable version .34.56'  # missing major version
        m6 = version_re.search(v6)
        assert m6 is None

        v7 = 'monotable version 1.Z.56'  # non numeric
        m7 = version_re.search(v7)
        assert m7 is None


#
# Test handling of empty lists and default constructor arguments.
#


def test_no_headings_no_formats_no_title_empty_cells():
    """No headings, formats, title, and no cells in the cellgrid.

    Test with both default argument values and empty lists."""

    tbl = monotable.table.MonoTable()    # default args for headings, formats
    text = tbl.table()
    assert text == ''

    text = tbl.table(cellgrid=[[]])
    assert text == ''

    text = monotable.table.cotable()
    assert text == ''

    text = tbl.bordered_table()
    assert text == ''

    text = tbl.bordered_table(cellgrid=[[]])
    assert text == ''

    row_strings = tbl.row_strings()
    assert row_strings == [[]]

    row_strings = tbl.row_strings(cellgrid=[[]])
    assert row_strings == [[]]

def test_empty_headings_empty_formats_empty_cells():
    """Empty headings, empty formats, and no cells in the cellgrid."""

    expected_title = 'My Title is a Good Title'
    tbl = monotable.table.MonoTable()
    text = monotable.table.table([], [], cellgrid=[[]], title=expected_title)
    assert text == expected_title

    text = monotable.table.bordered_table([], [], cellgrid=[[]],
                                          title=expected_title)
    assert text == expected_title


def test_empty_headings_empty_formats_empty_cells_no_title():
    """Empty headings, empty formats, no title, and no cells in cellgrid."""

    text = monotable.table.table([], [], cellgrid=[[]])
    assert text == ''


def test_only_title():
    tbl = monotable.table.MonoTable()

    text = tbl.table(cellgrid=[[]], title='Table Title')
    assert text == 'Table Title'

    text = tbl.table(title='Table Title')
    assert text == 'Table Title'

    text = tbl.table(title='<Table Title')
    assert text == 'Table Title'

    text = tbl.table(title='^Table Title')
    assert text == 'Table Title'

    text = tbl.table(title='>Table Title')
    assert text == 'Table Title'

    # repeat for bordered tables
    text = tbl.bordered_table(cellgrid=[[]], title='Table Title')
    assert text == 'Table Title'

    text = tbl.bordered_table(title='Table Title')
    assert text == 'Table Title'

    text = tbl.bordered_table(title='<Table Title')
    assert text == 'Table Title'

    text = tbl.bordered_table(title='^Table Title')
    assert text == 'Table Title'

    text = tbl.bordered_table(title='>Table Title')
    assert text == 'Table Title'

    # repeat for column oriented tables
    text = monotable.table.cotable([], 'Table Title')
    assert text == 'Table Title'

    text = monotable.table.cobordered_table([], 'Table Title')
    assert text == 'Table Title'

def test_only_wrapped_title():
    """Try to wrap a title on an empty table.

    No wrapping is done since table width is 0.
    """

    tbl = monotable.table.MonoTable()

    text = tbl.table(title='=Wrapped Title')
    assert text == 'Wrapped Title'

    text = tbl.table(title='<=Wrapped Title')
    assert text == 'Wrapped Title'

    text = tbl.table(title='>=Wrapped Title')
    assert text == 'Wrapped Title'

    text = tbl.table(title='^=Wrapped Title')
    assert text == 'Wrapped Title'

    # repeat for bordered tables
    text = tbl.bordered_table(title='=Wrapped Title')
    assert text == 'Wrapped Title'

    text = tbl.bordered_table(title='<=Wrapped Title')
    assert text == 'Wrapped Title'

    text = tbl.bordered_table(title='>=Wrapped Title')
    assert text == 'Wrapped Title'

    text = tbl.bordered_table(title='^=Wrapped Title')
    assert text == 'Wrapped Title'


def test_one_column_table():
    headings = ['Choices']
    cells = [['Spam'], ['Spam'], ['Spam'], ['Spam']]
    text = monotable.table.table(headings, [], cells)
    expected = '\n'.join([
        "-------",
        "Choices",
        "-------",
        "Spam",
        "Spam",
        "Spam",
        "Spam",
        "-------",
    ])
    assert text == expected


def test_one_column_cotable():
    column = ('Choices', '', ['Spam', 'Spam', 'Spam', 'Spam'])
    text = monotable.table.cotable([column])
    expected = '\n'.join([
        "-------",
        "Choices",
        "-------",
        "Spam",
        "Spam",
        "Spam",
        "Spam",
        "-------",
    ])
    assert text == expected


def test_one_column_bordered_table():
    headings = ['Choices']
    cells = [['Spam'], ['Spam'], ['Spam'], ['Spam']]
    text = monotable.table.bordered_table(headings, [], cells)
    expected = '\n'.join([
        "+---------+",
        "| Choices |",
        "+=========+",
        "| Spam    |",
        "+---------+",
        "| Spam    |",
        "+---------+",
        "| Spam    |",
        "+---------+",
        "| Spam    |",
        "+---------+",
    ])
    assert text == expected


def test_one_column_cobordered_table():
    column = ('Choices', '', ['Spam', 'Spam', 'Spam', 'Spam'])
    text = monotable.table.cobordered_table([column])
    expected = '\n'.join([
        "+---------+",
        "| Choices |",
        "+=========+",
        "| Spam    |",
        "+---------+",
        "| Spam    |",
        "+---------+",
        "| Spam    |",
        "+---------+",
        "| Spam    |",
        "+---------+",
    ])
    assert text == expected


#
# Show that headings, formats, cellgrid rows, and each row
# can be a sequence or immutable sequence rather than a list.
# Show the callers args are not modified.
#
# Show that a cellgrid that is not a sequence of sequences is handled
# properly if it is an iterable of iterables.
# Show error handling for a row that can't be iterated.
#
def test_cellgrid_is_tuples():
    cells = ((1, 2, 3), (4, 5, 6), (7, 8, 9))  # all tuples
    text = monotable.table.table([], [], cells)
    expected = '\n'.join([
        "-------",
        "1  2  3",
        "4  5  6",
        "7  8  9",
        "-------",
    ])
    assert text == expected


def test_column_oriented_cells_are_tuples():
    column0 = ('', '', (1, 4, 7))
    column1 = ('', '', (2, 5, 8))
    column2 = ('', '', (3, 6, 9))
    text = monotable.table.cotable([column0, column1, column2])
    expected = '\n'.join([
        "-------",
        "1  2  3",
        "4  5  6",
        "7  8  9",
        "-------",
    ])
    assert text == expected


def test_column_oriented_bordered_table_cells_are_tuples():
    column0 = ('', '', (1, 4, 7))
    column1 = ('', '', (2, 5, 8))
    column2 = ('', '', (3, 6, 9))
    text = monotable.table.cobordered_table([column0, column1, column2])
    expected = '\n'.join([
        "+---+---+---+",
        "| 1 | 2 | 3 |",
        "+---+---+---+",
        "| 4 | 5 | 6 |",
        "+---+---+---+",
        "| 7 | 8 | 9 |",
        "+---+---+---+",
    ])
    assert text == expected


def test_rows_are_ranges():
        cells = (range(11, 14), range(14, 17), range(17, 20))
        text = monotable.table.table([], [], cells)    # no headings, no formats
        expected = '\n'.join([
            "----------",
            "11  12  13",
            "14  15  16",
            "17  18  19",
            "----------",
        ])
        assert text == expected


def test_headings_formats_cells_are_tuples_and_missing_items():
    headings = ('a', 'b')         # missing heading
    formats = ('', '', '', '')    # extra format
    cells = ((1, 2, 3), (4, 5, 6), (7, 8))  # missing last cell
    text = monotable.table.table(headings, formats, cells)
    expected = '\n'.join([
        "-------",
        "a  b",
        "-------",
        "1  2  3",
        "4  5  6",
        "7  8",
        "-------",
    ])
    assert text == expected


def test_cell_rows_are_named_tuples():
    row = namedtuple('Row', ['column0', 'column1', 'column2'])
    cells = (row(column0=1, column1=2, column2=3),
             row(column0=11, column1=12, column2=13))
    text = monotable.table.table([], [], cells)
    expected = '\n'.join([
        "----------",
        " 1   2   3",
        "11  12  13",
        "----------",
    ])
    assert text == expected


def test_add_column_of_row_numbers():
    """Demonstrates a way to add a column of row numbers."""

    def transpose(grid):
        """Swap rows for columns or columns for rows."""

        return list(zip(*grid))

    headings = ['row\nnum', 'X', 'Y', 'Z']
    cells = (('A', 'B', 'C'), ('D', 'E', 'F'), ('G', 'H', 'I'))
    row_numbers = range(1, len(cells) + 1)
    cell_columns = transpose(cells)
    transposed_row_numbered = [row_numbers] + cell_columns
    row_numbered = transpose(transposed_row_numbered)
    text = monotable.table.table(headings, [], row_numbered)
    expected = '\n'.join([
        "------------",
        "row",
        "num  X  Y  Z",
        "------------",
        "  1  A  B  C",
        "  2  D  E  F",
        "  3  G  H  I",
        "------------",
    ])
    assert text == expected


def test_headings_are_iterable():
    """Headings is an interable, but not a sequence.  No len()."""
    headings = iter(('h1', 'h2', 'h3'))
    cells = (('A', 'B', 'C'), ('D', 'E', 'F'), ('G', 'H', 'I'))
    text = monotable.table.table(headings, [], cells,
                                 title='Headings\nfrom\nIterable')
    expected = '\n'.join([
        " Headings",
        "   from",
        " Iterable",
        "----------",
        "h1  h2  h3",
        "----------",
        "A   B   C",
        "D   E   F",
        "G   H   I",
        "----------",
    ])
    assert text == expected


def test_cellgrid_iterable_of_iterable():
    """Show indirectly that cellgrid can be an iterable of iterables.

    Create types for cellgrid and the cellgrid rows that don't support
    len().
    """
    row0 = iter((1, 2, 3))
    row1 = iter((4, 5, 6))
    row2 = iter((7, 8, 9))

    def row_generator():
        yield row0
        yield row1
        yield row2

    cells = row_generator()
    text = monotable.table.table([], {}, cells)
    expected = '\n'.join([
        "-------",
        "1  2  3",
        "4  5  6",
        "7  8  9",
        "-------",
    ])
    assert text == expected


def test_forgot_outer_list_with_one_row_cellgrid():
    """Show proper error handling for a row that can't be iterated.

    Expect an AssertionError that tells the index of the offending row.
    The int 9 in row[1] is not iterable.
    """

    cells = [1, 2, 3]   # missing outer []
    with pytest.raises(AssertionError) as exc_info:
        _ = monotable.table.table((), (), cells)
    msg = 'If one row cellgrid, likely missing outer list.'
    assert str(exc_info.value).endswith(msg)


def test_forgot_outer_list_with_one_column_of_column_tuples():
    """Show proper error handling for missing list around column tuples."""
    msg = 'Short tuple or missing enclosing list.'
    column = ('', '', (1, 4, 5))
    with pytest.raises(AssertionError) as exc_info:
        _ = monotable.table.cotable(column)    # missing outer []
    assert str(exc_info.value).endswith(msg)

    with pytest.raises(AssertionError) as exc_info:
        _ = monotable.table.cobordered_table(column)    # missing outer []
    assert str(exc_info.value).endswith(msg)


def test_too_short_column_tuple():
    """Show proper error handling for column tuple len() != 3."""
    msg = 'Short tuple or missing enclosing list.'
    column0 = ('', '', (1, 4, 7))
    column1 = ('', '', (2,))
    column2 = ('',  (3, 6, 9))    # short tuple, missing format string
    with pytest.raises(AssertionError) as exc_info:
        _ = monotable.table.cotable([column0, column1, column2])
    assert str(exc_info.value).endswith(msg)

    with pytest.raises(AssertionError) as exc_info:
        _ = monotable.table.cobordered_table([column0, column1, column2])
    assert str(exc_info.value).endswith(msg)


def test_column_oriented_left_column_shorter():
    column0 = ('', '', (1, 4))
    column1 = ('', '', (2, 5, 8))
    column2 = ('', '', (3, 6, 9))
    text = monotable.table.cotable([column0, column1, column2])
    expected = '\n'.join([
        "-------",
        "1  2  3",
        "4  5  6",
        "   8  9",
        "-------",
    ])
    assert text == expected


def test_column_oriented_right_column_shorter():
    column0 = ('', '', (1, 4, 7))
    column1 = ('', '', (2, 5, 8))
    column2 = ('', '', (3, 6))
    text = monotable.table.cotable([column0, column1, column2])
    expected = '\n'.join([
        "-------",
        "1  2  3",
        "4  5  6",
        "7  8",
        "-------",
    ])
    assert text == expected


def test_column_oriented_middle_column_shorter():
    column0 = ('', '', (1, 4, 7))
    column1 = ('', '', (2,))
    column2 = ('', '', (3, 6, 9))
    text = monotable.table.cotable([column0, column1, column2])
    expected = '\n'.join([
        "-------",
        "1  2  3",
        "4     6",
        "7     9",
        "-------",
    ])
    assert text == expected


def test_bordered_column_oriented_left_column_shorter():
    column0 = ('', '', (1, 4))
    column1 = ('', '', (2, 5, 8))
    column2 = ('', '', (3, 6, 9))
    text = monotable.table.cobordered_table([column0, column1, column2])
    expected = '\n'.join([
        "+---+---+---+",
        "| 1 | 2 | 3 |",
        "+---+---+---+",
        "| 4 | 5 | 6 |",
        "+---+---+---+",
        "|   | 8 | 9 |",
        "+---+---+---+",
    ])
    assert text == expected


def test_bordered_column_oriented_right_column_shorter():
    column0 = ('', '', (1, 4, 7))
    column1 = ('', '', (2, 5, 8))
    column2 = ('', '', (3, 6))
    text = monotable.table.cobordered_table([column0, column1, column2])
    expected = '\n'.join([
        "+---+---+---+",
        "| 1 | 2 | 3 |",
        "+---+---+---+",
        "| 4 | 5 | 6 |",
        "+---+---+---+",
        "| 7 | 8 |   |",
        "+---+---+---+",
    ])
    assert text == expected


def test_bordered_column_oriented_middle_column_shorter():
    column0 = ('', '', (1, 4, 7))
    column1 = ('', '', (2,))
    column2 = ('', '', (3, 6, 9))
    text = monotable.table.cobordered_table([column0, column1, column2])
    expected = '\n'.join([
        "+---+---+---+",
        "| 1 | 2 | 3 |",
        "+---+---+---+",
        "| 4 |   | 6 |",
        "+---+---+---+",
        "| 7 |   | 9 |",
        "+---+---+---+",
    ])
    assert text == expected


class TestMonoTableExceptionCallback:
    """Try out each of the exception callback functions."""

    headings = ['column0', 'column1']
    formats = ['', 'd']  # d is bad format for the string 'label1'
    cells = [[0, 9999], [1, 'label1']]

    def test_raise_it(self):
        with pytest.raises(monotable.table.MonoTableCellError) as exc_info:
            _ = monotable.table.table(self.headings, self.formats, self.cells)
        exc = exc_info.value
        assert exc.row == 1
        assert exc.column == 1
        assert exc.format_spec == 'd'

        # trace_text is generated by the Python installation and is subject
        # to change.  Just check for presence of the text.
        assert len(exc.trace_text) > 0
        assert exc.name == 'MonoTableCellError'

        expected_str = "MonoTableCellError: cell[1][1], format_spec= d"
        assert expected_str in str(exc)

    def test_bordered_raise_it(self):
        with pytest.raises(monotable.table.MonoTableCellError) as exc_info:
            _ = monotable.table.bordered_table(self.headings, self.formats,
                                               self.cells)
        exc = exc_info.value
        assert exc.row == 1
        assert exc.column == 1
        assert exc.format_spec == 'd'
        assert len(exc.trace_text) > 0
        assert exc.name == 'MonoTableCellError'

        expected_str = "MonoTableCellError: cell[1][1], format_spec= d"
        assert expected_str in str(exc)

    def test_bordered_format_ignore_it(self):
        tbl = monotable.table.MonoTable()

        tbl.format_exc_callback = monotable.plugin.ignore_it
        text = tbl.bordered_table(self.headings, self.formats, self.cells)
        # Each item in column not overridden by an align_spec
        # is aligned by type(item).
        # Since cell[1,1] = 'label1', a string, it auto-aligns to the left.
        expected = '\n'.join([
            "+---------+---------+",
            "| column0 | column1 |",
            "+=========+=========+",
            "|       0 |    9999 |",
            "+---------+---------+",
            "|       1 | ???     |",
            "+---------+---------+",
        ])
        assert text == expected

    def test_user_supplied_ignore_it(self):
        def my_ignore_it(_):
            return '!!!!!!!!!!!'

        class MyIgnoreItMonoTable(monotable.table.MonoTable):
            format_exc_callback = staticmethod(my_ignore_it)

        tbl = MyIgnoreItMonoTable()

        text = tbl.table(self.headings, self.formats, self.cells)
        expected = '\n'.join([
            "--------------------",
            "column0      column1",
            "--------------------",
            "      0         9999",
            "      1  !!!!!!!!!!!",
            "--------------------",
        ])
        assert text == expected


def test_print_it(capsys):
    exc = monotable.table.MonoTableCellError(777, 999, 'spec',
                                             'this is the trace text')
    value = monotable.plugin.print_it(exc)
    out, err = capsys.readouterr()
    assert out == '\n'.join([
        "MonoTableCellError: cell[777][999], format_spec= spec",
        "MonoTableCellError raised after catching:",
        "this is the trace text",
        ""])

    assert value == '???'


class TestMonoTableCatchesFormatErrors:
    """Make sure format errors are caught."""
    Point = namedtuple('Point', ['x', 'y'])
    cells = [[Point(1, 91)],
             [Point(5, 95)]]

    def test_sformat_missing_attribute_error(self):
        """Callers cell object has no 'z' attribute."""
        formats = ['(sformat){.z}']   # missing attribute
        with pytest.raises(monotable.table.MonoTableCellError) as exc_info:
            _ = monotable.table.table((), formats, self.cells)
        exc = exc_info.value
        assert exc.row == 0
        assert exc.column == 0
        assert exc.format_spec == '{.z}'
        assert len(exc.trace_text) > 0
        assert exc.name == 'MonoTableCellError'

    def test_sformat_missing_index_error(self):
        """Callers cell object has no [2] index."""
        formats = ['(sformat){[2]}']  # missing index
        with pytest.raises(monotable.table.MonoTableCellError) as exc_info:
            _ = monotable.table.table((), formats, self.cells)
        exc = exc_info.value
        assert exc.row == 0
        assert exc.column == 0
        assert exc.format_spec == '{[2]}'
        assert len(exc.trace_text) > 0
        assert exc.name == 'MonoTableCellError'


def test_mformat_missing_key_error():
    """Callers dict has no value for key 'name'."""
    cells = [[dict(not_name=0)]]   # has no value for key='name'
    with pytest.raises(monotable.table.MonoTableCellError) as exc_info:
        _ = monotable.table.table([], ['(mformat)name= {name}'], cells)
    exc = exc_info.value
    assert exc.row == 0
    assert exc.column == 0
    assert exc.format_spec == 'name= {name}'
    assert len(exc.trace_text) > 0
    assert exc.name == 'MonoTableCellError'

# no test case for ArithmeticError


def test_user_defined_format_function_hides_default_format_function():
    """A plugged in format function hides default of same name."""
    def pformat(value, format_spec):
        _, _ = value, format_spec    # avoid value is not used warnings

    my_format_func_map = {'pformat': pformat}

    class MyMonoTable(monotable.table.MonoTable):
        format_func_map = my_format_func_map
    tbl = MyMonoTable()
    assert id(tbl.format_func_map['pformat']) == id(pformat)
    assert id(tbl.format_func_map['pformat']) != id(monotable.plugin.pformat)


def test_user_defined_format_function_raises_assertion_error():
    """User defined format function raises an assertion."""
    def user_defined_format_function(value, format_spec):
        _, _ = value, format_spec    # avoid value is not used warnings
        raise AssertionError('spam')

    my_format_func_map = {'my_format_function': user_defined_format_function}

    class MyMonoTable(monotable.table.MonoTable):
        format_func_map = my_format_func_map
    tbl = MyMonoTable()
    cells = [[1234]]
    with pytest.raises(monotable.table.MonoTableCellError) as exc_info:
        _ = tbl.table([], ['(my_format_function)'], cells)
    exc = exc_info.value
    assert exc.row == 0
    assert exc.column == 0
    assert exc.format_spec == ''
    assert len(exc.trace_text) > 0
    assert exc.name == 'MonoTableCellError'


def test_init_illegal_vertical_align():
    # Note- Does not test entire exception message.
    msg = 'Expected a vertical align value, got:'

    with pytest.raises(AssertionError) as exc_info:
        tbl = monotable.table.MonoTable()
        tbl.cell_valign = -1
        _ = tbl.table([], [], [[]])
    assert str(exc_info.value).startswith(msg)

    with pytest.raises(AssertionError) as exc_info:
        tbl = monotable.table.MonoTable()
        tbl.cell_valign = 50
        _ = tbl.bordered_table([], [], [[]])
    assert str(exc_info.value).startswith(msg)


def test_bad_option_spec():
    """
    Check for AssertionError raised by code in _process_formats() due
    to a bad option in a valid option_spec.
    """
    # Note- Does not test entire exception message.
    tbl = monotable.table.MonoTable()
    cells = [['A']]

    with pytest.raises(AssertionError) as exc_info:
        _ = tbl.bordered_table([], ['(bad_option_spec)s'], cells)
    assert str(exc_info.value).startswith('cell column 0, format= ')


def test_override_option_spec_delimiters_bad_option_spec():
    """
    Change option_spec_delimiters on an instance.
    Use the same char for start and end delimiters.
    Check for AssertionError raised by code in _process_formats() due
    to a bad option in a valid option_spec.  The option_spec is still
    valid even with new delimiters.
    """
    # Note- Does not test entire exception message.

    tbl = monotable.table.MonoTable()
    tbl.option_spec_delimiters = '!;!'
    cells = [['A']]
    with pytest.raises(AssertionError) as exc_info:
        _ = tbl.bordered_table([], ['!bad_option_spec!s'], cells)
    assert str(exc_info.value).startswith('cell column 0, format= ')


def test_no_option_spec_delimiters():
    """
    Disable option spec scanning by setting option_spec_delims to
    empty string.  Format will be interpreted as a format_spec and
    cause a MonoTableCellError.
    """
    # Note- Does not test entire exception message.

    tbl = monotable.table.MonoTable()
    tbl.option_spec_delimiters = ''   # disable
    cells = [['A']]

    msg = 'MonoTableCellError: cell[0][0], format_spec= !width=10!s'
    with pytest.raises(monotable.table.MonoTableCellError) as exc_info:
        _ = tbl.table([], ['!width=10!s'], cells)
    assert str(exc_info.value).startswith(msg)


def test_override_option_spec_delimiters():
    """Test formatting with overridden option_spec_delimiters."""

    tbl = monotable.table.MonoTable()
    tbl.option_spec_delimiters = '!;!'
    cells = [['A']]
    text = tbl.table([], ['!width=10!s'], cells)
    assert text == '-\nA\n-'


def test_format_row_strings():
    row0 = [9.1234567] * 4
    row1 = [88.1] * 4
    cells = [row0, row1]
    headings = ['.1f', '.3f', '<.5f', 'default=.4f']
    formats = ['.1f', '<.3f', '.5f']

    class Float4fMonoTable(monotable.table.MonoTable):
        default_float_format_spec = '.4f'
    t = Float4fMonoTable()
    row_strings = t.row_strings(headings, formats, cells)
    assert row_strings == [[' .1f', '.3f   ', '.5f     ', 'default=.4f'],
                           [' 9.1', '9.123 ', ' 9.12346', '     9.1235'],
                           ['88.1', '88.100', '88.10000', '    88.1000']]


def test_format_to_row_strings_stripped():
    row0 = [9.1234567] * 4
    row1 = [88.1] * 4
    cells = [row0, row1]
    headings = ['.1f', '.3f', '<.5f', 'default=.4f']
    formats = ['.1f', '<.3f', '.5f']

    class Float4fMonoTable(monotable.table.MonoTable):
        default_float_format_spec = '.4f'
    t = Float4fMonoTable()
    row_strings = t.row_strings(headings, formats, cells, strip=True)
    assert row_strings == [['.1f', '.3f', '.5f', 'default=.4f'],
                           ['9.1', '9.123', '9.12346', '9.1235'],
                           ['88.1', '88.100', '88.10000', '88.1000']]
