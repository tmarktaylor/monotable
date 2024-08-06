# Copyright 2020 Mark Taylor
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

"""ASCII table: per column format specs, formatting directives, multi-line.

   Formats 2D array of Python values to ASCII table format.
   The table looks pretty when printed in a monospaced font.
   See class MonoTable docstring for details.

   Classes:
   MonoTable   Format Python values to ASCII table for monospaced font.

   Functions:
   table               Convenience wrapper for MonoTable.table()
   bordered_table      Convenience wrapper for MonoTable.bordered_table()
   cotable             Convenience wrapper for MonoTable.cotable()
   cobordered_table    Convenience wrapper for MonoTable.cobordered_table()

   Exceptions:
   MonoTableCellError  Created when formatting a cell fails.

   Attributes:
   HR             In column 0 of a row, horizontal rule should be inserted.
"""


import copy
import numbers
import string
import textwrap
import traceback
from itertools import zip_longest
from typing import List, Tuple, Optional, Callable, Mapping
from typing import Union, Any, Sequence, Iterable
from typing import cast

import monotable.plugin
import monotable.scanner
from monotable.scanner import FormatScanner
from monotable.monoblock import MonoBlock
from monotable.cellerror import MonoTableCellError

from monotable.alignment import NOT_SPECIFIED
from monotable.alignment import LEFT
from monotable.alignment import RIGHT

Cell = Any
Row = Iterable[Cell]
CellGrid = Iterable[Row]
FormatFunc = Callable[[Any, str], str]
FormatFuncMap = Mapping[str, FormatFunc]
ColumnTuple = Tuple[str, str, Sequence[Any]]

# repository: https://github.com/tmarktaylor/monotable
# Docstrings are Google Style for Sphinx plugin sphinx.ext.napoleon.


def _transpose(grid: Iterable[Iterable[Any]]) -> List[Tuple[Any, ...]]:
    """Swap rows for columns or columns for rows."""
    return list(zip(*grid))


class _HR:
    """Type to distinguish a horizontal rule from other cell types."""
    pass


HR = _HR()
"""Placed in column 0 of a *row* in a cellgrid to insert a horizontal rule.

Since v2.1.0 monotable.HR_ROW can be used instead.
A row that starts with a HR is omitted from the
table and a heading guideline is inserted in its place.
"""


class MonoTable:
    """Create an aligned and formatted text table from a grid of cells.

    Call :py:meth:`~MonoTable.table` passing a sequence of heading strings,
    a sequence of format strings, a sequence of sequence of
    cells, and a title string.
    The return value is a string ready for printing.

    Call :py:meth:`~MonoTable.cotable` passing a sequence of tuples of
    (heading, format, list of cells in the column); one tuple for each
    column; and a title string.  The prefix co stands for column oriented.

    Call :py:meth:`~MonoTable.bordered_table` with the same arguments
    as table() to format a table with character borders.

    Call :py:meth:`~MonoTable.cobordered_table` with the same arguments
    as cotable() to format a table with character borders.

    Call :py:meth:`~MonoTable.row_strings` passing a sequence of heading
    strings, a sequence of format strings, a sequence of sequence of
    cells to return a tuple of lists of formatted headings and
    list of list of cells.

    Heading strings, title strings, and formatted cells may contain
    newlines.

    Cells that inherit from numbers.Number are *Auto-Aligned* to the right
    and all other cell types are auto aligned to the left.

    Definitions:

    :align_spec: One of the characters '<', '^', '>'.  The characters
        indicate left, center, and right justification.
        To configure, override the class variable
        :py:attr:`~MonoTable.align_spec_chars`.

    :Heading String: [align_spec]string

    :Format String: [align_spec][directives][format_spec]

    :Title String: [align_spec][wrap_spec]string

    * The format directive string syntax is described by the
      :py:meth:`~MonoTable.table` argument **formats** below.

    .. _alignment-label:

    **Auto-alignment:**

    * Heading alignment is determined by this decision order:

        1. align_spec if present in the heading string.
        2. align_spec if present in the format string.
        3. Auto-Alignment for the cell in the first row.

    * Cell alignment is determined by this decision order:

        1. align_spec if present in the format string.
        2. Auto-Alignment for the cell.

    * The title is auto-aligned to center.

    :note: The align_spec prefix may be omitted, but is required if the
        rest of the string starts with one of the align_spec_chars.
        Or the user can put in an empty directives for example '()'.

    :note: align_spec scanning/parsing can be disabled by setting the
        class variable :py:attr:`~MonoTable.align_spec_chars` to
        the empty string.

    There is one format string for each column of cells.

    Formatting, by default, is done by ``<built-in function format>``.

        * The user can specify a different default format function for the
          table by overriding the class variable
          :py:attr:`~MonoTable.format_func`.
        * In directives the user can specify a format function for
          a column which takes precedence over the table default format
          function.  They are listed here:
          :ref:`Format directives<format-directives-label>`.
        * Any user defined function in the dict assigned to the class variable
          :py:attr:`~MonoTable.format_func_map`
          may be selected by putting its key as a formatting directive.

    Here is the data flow through the formatting engine:

    .. code-block:: none

                            text              MonoBlock
        cell -> format_func ---> (parentheses) ------> width control,
                format_spec      (zero=)          |    justification
                                                  |      (width=)
        cell is None ------------(none=)----------+      (max)
                                                         (wrap)
                                                         (fixed)

        * format directives are shown enclosed by ().
        * format_func may be selected by a format function directive.
        * user can plug in new format function directives.

    * If cell is None an empty string is formatted.
      Configure for a column by using the `none=` format directive in
      directives.
      Configure for the whole table by overriding class variable
      :py:attr:`~MonoTable.format_none_as`.
    * If a cell is type float, and format_spec is an empty string, and the
      format function is <built-in function format>, the cell
      is formatted using class variable :py:attr:`~default_float_format_spec`.

    directives can contain the format directives `lsep=` and `rsep=`
    which sets the separator string placed before/after the column.

    If wrap_spec_char is present in table title the title is text wrapped
    to the width of the table.
    To change the wrap_spec_char or disable wrap_spec_char scanning,
    see the class variable :py:attr:`~wrap_spec_char`.
    Title is auto-aligned to center by default.

    A format error produces an exception object which identifies
    the offending cell.  Format error handling is configurable
    by overriding class variable :py:attr:`~MonoTable.format_exc_callback`.

    All the class variables can be overridden in ether a subclass or on
    an instance.  For the complete list
    please see section :ref:`class-vars-label`.
    """

    format_func = format    #: <built-in function format>
    """User defined function with signature of <built-in function format>.

    This function is selected for cell formatting except when
    a column format string directives specifies a format function.

    These :ref:`format-functions-label` can be used here.

    When overriding in a subclass definition use the result of
    Python built in function staticmethod() like this:

    >>> import monotable
    >>> def your_user_defined_format_function(value, format_spec):
    ...    pass
    >>> class SubclassMonoTable(monotable.MonoTable):
    ...     format_func = staticmethod(your_user_defined_format_function)
    >>> tbl = SubclassMonoTable()
    >>>
    >>> # When overriding on an instance do not use staticmethod like this:
    >>>
    >>> tbl = monotable.MonoTable()
    >>> tbl.format_func = your_user_defined_format_function

    .. _Docs Here:
       https://docs.python.org/3/howto/descriptor.html#functions-and-methods

    Reading Python functions and methods `Docs Here`_ helps explain when
    to use built in function staticmethod().
    """

    format_exc_callback = staticmethod(monotable.plugin.raise_it)
    """ Function called when format_func raises an exception.

    The function takes the argument MonoTableCellError and
    (if returning) returns the string to be returned by format_func.

    These :ref:`callbacks-label` can be used here.

    Please see advice at :py:attr:`~MonoTable.format_func`
    about when to use staticmethod().
    """

    default_float_format_spec = '.6f'
    """Default format specification for float type.

    Applies only to cells that satisfy all of:

    - cell value is type float
    - format function is <built-in function format>
    - format_spec is the empty string

    If the cell is not type float or a different format function is
    set, this will not apply.

    This sets the precision to align the decimal points in a column
    of floats. This is useful when a column contains floats and strings.
    The presence of strings prevents the use of a float format_spec
    for the column.

    Disable this feature by setting to the empty string.
    This feature applies to the entire table.
    """

    sep = '  '
    """String that separates columns in non-bordered tables.

    sep after a column can be overridden by the format string directive rsep.
    """

    separated_guidelines = False
    """When True guidelines will have the sep characters between columns.

    This looks good when the seps are all spaces.
    When False the guideline character is repeated for the width
    of the table.  seps refers to characters placed between heading and
    cell columns in the table.
    """
    format_func_map = None    # type: Optional[FormatFuncMap]
    """Adds format functions selectable by a format directive.

    Dictionary of format functions keyed by name.
    name, when used as a format directive in a format string,
    selects the corresponding function from the dictionary.
    If a key is one of the included format directive function
    names like 'boolean', 'mformat', etc. the included format
    directive function is hidden.
    """

    format_none_as = ''
    """Value placed in table for cell of type None."""

    more_marker = '...'
    """Inserted to indicate text has been omitted."""

    align_spec_chars = '<^>'
    """Three characters to indicate justification.

    Applies to align_spec scanning in heading, title, and format directive
    strings.
    The first character indicates left justification.  The second and third
    characters indicate center and right justification.
    Setting align_spec_chars to "" disables align_spec scanning.
    """

    wrap_spec_char = '='
    """Single character to indicate the title should be text wrapped.

    Wrapping is done to the width of the table.
    Setting wrap_spec_char to "" disables title text wrap.
    """

    option_spec_delimiters = '(;)'
    """Three characters to enclose and separate format directives.

    The first and third chars enclose the options.
    The second char separates individual options. Setting
    option_spec_delimiters to "" disables format directive scanning
    in format strings.
    """

    guideline_chars = '---'
    """String of 0 to 3 characters to specify guideline appearance.

    The first character is used for the top guideline.
    The second and third characters are used for the heading guideline
    and bottom guideline.  If the character is a space the
    guideline is omitted.  The empty string suppresses all guidelines.
    """

    heading_valign = monotable.alignment.BOTTOM
    """Alignment used for vertical justification of a multi-line heading.

    Should be one of one of :ref:`vertical-alignment-constants-label`
    TOP, CENTER_TOP, CENTER_BOTTOM, or BOTTOM.
    """

    cell_valign = monotable.alignment.TOP
    """Alignment used for vertical justification of a multi-line cell.

    Should be one of one of :ref:`vertical-alignment-constants-label`
    TOP, CENTER_TOP, CENTER_BOTTOM, or BOTTOM.
    """

    max_cell_height = None    # type: int
    """Truncates multi-line cells to this height.  None means unlimited.

    If characters are omitted, inserts **more_marker** at the end of the cell.
    Setting max_cell_height=1 will suppress multi-line cells.
    """

    border_chars = '--|+='
    """Characters used for borders in bordered tables.

    One char each: top, bottom, sides, corner, heading guideline.
    """

    hmargin = 1
    """Number of blanks inserted on each side of text between borders.

    Applies to bordered tables.
    """

    vmargin = 0
    """Number of blank lines inserted above and below formatted text.

    Applies to bordered tables.
    """

    def __init__(self, indent=''):    # type: (str) -> None
        """
        Args:
            indent (str):
                String added to the beginning of each line in the text table.

        """

        # User can override class and instance variables by assignment to
        # an instance.
        # To maintainers:
        # - No instance variables are dependent on any other
        #   instance variables.
        # - No instance variables are assigned outside of the constructor.
        #
        self.indent = indent

    def table(
            self,
            headings: Iterable[str] = (),
            formats: Iterable[str] = (),
            cellgrid: CellGrid = ((),),
            title: str = '',
    ) -> str:
        """Format printable text table.  It is pretty in monospaced font.

        Args:
            headings
                Iterable of strings for each column heading.

            formats
                Iterable of format strings of the form
                ``[align_spec][directives][format_spec]``.
                `Format directive string syntax`_

            cellgrid
                representing table cells.

            title
                ``[align_spec][wrap_spec]string``.
                Text to be aligned and printed above the text table.
                `Title string syntax`_

        Returns:
            The text table as a single string.

        Raises:
            MonoTableCellError

        Here is an example of non-bordered text table:

        .. code-block:: none

            Int, Float, String                        <-- title
            --------------------------------------    <-- top guideline
                  Int        Float  String            <-- heading row
            --------------------------------------    <-- heading guideline
            123456789     3.141593  Hello World       <-- cell row
                    2  2718.281828  another string    <-- cell row
            --------------------------------------    <-- bottom guideline

                     ^^           ^^
                      |            |
                   sep/rsep     sep/rsep

        This example has 6 sep strings of 2 spaces each.  The seps are placed
        between columns in the heading line and between the columns in
        each of the 2 cell rows.


        .. _Title string syntax:

        **Title string syntax:**

        ``[align_spec][wrap_spec]string``

        align_spec
            One of the characters '<', '^', '>' to
            override auto-alignment.

        wrap_spec
            Character '=' to indicate the title
            should be text wrapped to the width of the table.

        .. _Format directive string syntax:

        **Format directive string syntax:**

        ``[align_spec][directives][format_spec]``.

        align_spec
            One of the characters '<', '^', '>' to
            override auto-alignment.

        directives
            One or more of format directives enclosed by '(' and ')'
            separated by ';'.

        format_spec
            String passed to the format function.

        .. _format-directives-label:

        **Format directives:**

        The format string directives described here apply to all
        MonoTable methods and monotable convenience functions that
        take format strings.

        - At most, one format function directive is allowed.
        - Each directive is allowed once.
        - Spacing before '=' is always ignored.
        - Spacing after '=' is significant for none, zero, lsep, and rsep.


        width=N
            Truncate each formatted cell text line(s) to width N and
            insert the class variable :py:attr:`more_marker` if text was
            omitted.

        fixed
            Used with width=N formats text to exactly width = N columns.

        wrap
            Used with width=N does textwrap of formatted cell to width = N.

        lsep=ccc
            Characters after 'lsep=' are the column separator on the
            left hand side of the column.  Use lsep with care because it
            will silently overwrite the rsep specified for the column
            to the left.  It has no effect if specified on the left-most
            column.

        rsep=ccc
            Characters after 'rsep=' are the column separator on the
            right hand side of the column.
            It has no effect if specified on the right-most column.

        sep=ccc
            Same as rsep.  sep is an alias for rsep since version 2.1.0.
            New code should use rsep=ccc since the meaning is more explicit.

        .. _Format function directives:

        **Format function directives:**

        boolean
            Convert boolean cell truth value to one of two strings supplied
            by the format_spec.  Implemented by
            :py:func:`monotable.plugin.boolean`

        none=ccc
            Specifies the formatted text for None cell value.

        zero=ccc
            For cells that are numbers, when all digits in formatted text
            are zero replace the formatted text with ccc.  ``0.00e00 -> ccc``.

        parentheses
            For cells that are numbers, when formatted text starts with a
            minus sign, remove the minus sign and add enclosing parentheses.
            ``-100.1 -> (100.1)``.  Maintains alignment with
            numbers not enclosed by parentheses.

        thousands
            Select format function that divides by 10.0e3 before applying the
            format_spec. :py:func:`monotable.plugin.thousands`

        millions
            Select format function that divides by 10.0e6 before applying the
            format_spec. :py:func:`monotable.plugin.millions`

        billions
            Select format function that divides by 10.0e9 before applying the
            format_spec. :py:func:`monotable.plugin.billions`

        trillions
            Select format function that divides by 10.0e12 before applying the
            format_spec. :py:func:`monotable.plugin.trillions`

        milli
            Select format function that multiplies by 10.0e3 before applying
            the format_spec. :py:func:`monotable.plugin.milli`

        micro
            Select format function that multiplies by 10.0e6 before applying
            the format_spec. :py:func:`monotable.plugin.micro`

        nano
            Select format function that multiplies by 10.0e9 tbefore applying
            the format_spec. :py:func:`monotable.plugin.nano`

        pico
            Select format function that multiplies by 10.0e12 before applying
            the format_spec. :py:func:`monotable.plugin.pico`

        kibi
            Select format function that divides by 1024 before applying the
            format_spec. :py:func:`monotable.plugin.kibi`

        mebi
            Select format function that divides by 1024^2 before applying the
            format_spec. :py:func:`monotable.plugin.mebi`

        gibi
            Select format function that divides by 1024^3 before applying the
            format_spec. :py:func:`monotable.plugin.gibi`

        tebi
            Select format function that divides by 1024^4 before applying the
            format_spec. :py:func:`monotable.plugin.tebi`

        mformat
            Select format function that selects values from a dictionary.
            :py:func:`monotable.plugin.mformat`

        pformat
            Select format function adapter to percent operator %.
            :py:func:`monotable.plugin.pformat`

        sformat
            Select format function adapter to str.format().
            :py:func:`monotable.plugin.sformat`

        tformat
            Select format function adapter to string.Template.substitute().
            :py:func:`monotable.plugin.tformat`

        function-name
            Select format function with key function-name
            in the dictionary supplied by class variable
            :py:attr:`~MonoTable.format_func_map`.
        """

        # convert, format, and justify headings/cells into MonoBlock objects
        justified_headings, justified_cells, widths, seps = (
            self._format_and_justify(headings,
                                     formats,
                                     cellgrid))

        table_width = sum(widths) + sum([len(s) for s in seps])

        top_guideline, heading_guideline, bottom_guideline = (
            self._make_guidelines(table_width, widths, seps))

        lines = []    # type: List[str]

        if title:
            lines.extend(self._make_title_lines(title, table_width))

        if top_guideline:
            lines.append(top_guideline)

        # Add list of printable lines obtained from the heading MonoBlocks.
        if self._has_headings(justified_headings):
            lines.extend(
                self._monoblock_row_to_strings(justified_headings, seps))
            if heading_guideline:
                lines.append(heading_guideline)

        # Add list of printable lines obtained from each row of cell
        # MonoBlocks.
        for row in justified_cells:
            # If a row starts with a cell of type _InternalGuideline,
            # replace the entire row with the single line heading guideline.
            # It is possible heading_guideline will be the empty string
            # if it has been disabled by self.guideline_chars.  In that
            # case a blank line appears in the table.
            if isinstance(row[0], _InternalGuideline):
                lines.append(heading_guideline)
            else:
                lines.extend(self._monoblock_row_to_strings(row, seps))

        if bottom_guideline:
            lines.append(bottom_guideline)

        # strip trailing spaces
        lines = [line.rstrip() for line in lines]

        return self.indent + ('\n' + self.indent).join(lines)

    def _format_and_justify(
            self,
            headings: Iterable[str] = (),
            formats: Iterable[str] = (),
            cellgrid: CellGrid = ((),),
    ) -> Tuple[List[MonoBlock], List[Tuple[MonoBlock]], List[int], List[str]]:
        """Format, align, and justify the text table.

        headings
            Iterable of strings for each table column heading.
            See description for the constructor argument 'headings'.

        formats
            Iterable of format directives strings used to format each
            column of cells.
            See description for the constructor argument 'formats'.

        cellgrid
            Iterable of Iterable of Python values representing table cells.

        Returns tuple:
            Row of heading MonoBlocks ready to be justified.

            List of Tuple of MonoBlocks representing formatted cells.
            MonoBlocks are ready to be justified.

            List of width of each column.  The width is the length of
            the string needed to fit the widest heading line or
            formatted cell in the column.

            List of separator string (sep) placed in the row after
            each column of headings/cells.

        """

        # Assure headings, formats, and each row in cellgrid are same length
        # by adding blank headings and cells and dropping extra formats.
        xheadings, xformats, xcellgrid = (
            self._extend_short_rows(headings, formats, cellgrid))

        processed_formats = self._process_formats(xformats)

        # Format, determine alignment, convert to MonoBlock.
        formatted_cell_columns = self._format_cells_as_columns(
            xcellgrid,
            processed_formats)

        # Determine alignment, convert to MonoBlock.
        processed_headings = self._process_headings(
            xheadings,
            xformats,
            xcellgrid[0])

        widths = self._calculate_column_widths(
            processed_headings,
            formatted_cell_columns)

        # Do both horizontal and vertical justification.  (In-place).
        self._justify_headings(processed_headings, widths)
        self._justify_cell_columns(formatted_cell_columns, widths)

        # typing cast explained:
        # 1. _transpose() returns type List[Tuple[Any, ...]]
        # 2. formatted_cell_columns is type List[List[MonoBlock]]
        # 3. _format_and_justify returns a four item tuple. The second item
        #    is type List[Tuple[MonoBlock]] which is the result of the cast.
        # 4. _transpose() returns type List[Tuple[Any, ...]].
        # Here _transpose() converts the inner most type from MonoBlock
        # to the more general Any.
        # The cast changes the inner most type back to MonoBlock.
        return (
            processed_headings,
            cast(List[Tuple[MonoBlock]], _transpose(formatted_cell_columns)),
            widths,
            self._make_list_of_seps(processed_formats)
            )

    @staticmethod
    def _extend_short_rows(
            headings: Iterable[str] = (),
            formats: Iterable[str] = (),
            cellgrid: CellGrid = ((),),
            ) -> Tuple[List[str], List[str], List[List[Cell]]]:
        """Create new headings, formats, and cellgrid so rows are equal length.

        Returns new lists of headings, formats, and a new cellgrid.

        headings and formats must be Iterables.  cellgrid must be
        a Iterable of Iterable.  Sequences are fine as well.
        Extend too short headings or too short cell rows.
        Don't extend anything if too many formats, silently discard instead.

        headings and formats are extended with the empty string.
        cellgrid rows are extended with a single instance of MonoBlock.
        MonoBlock instances receive special handling during formatting.
        """

        # Convert cellgrid to list of lists in order to determine the length
        # of each row.  Also test that each row is iterable.
        xcellgrid = []    # type: List[List[Cell]]
        for row in cellgrid:
            try:
                xcellgrid.append(list(row))  # copy and convert row to list
            except TypeError as exc:
                msg = 'If one row cellgrid, likely missing outer list.'
                assert False, 'Exception "{}". {}'.format(str(exc), msg)

        # Convert from Iterable to List.
        xheadings = list(headings)
        num_columns = max([len(xheadings)] + [len(row) for row in xcellgrid])

        # extend any short rows in xcellgrid
        for row in xcellgrid:
            row.extend([MonoBlock()] * (num_columns - len(row)))
            # It is OK to extend with same instance of MonoBlock because
            # of special handling later by _format_cells_as_columns().

        # Extend by more than needed, truncate to len() = num_columns.
        xheadings.extend([''] * num_columns)
        xheadings = xheadings[:num_columns]

        # Make copy and convert to list.
        # Extend by more than needed, truncate to len() = num_columns.
        xformats = list(formats)
        xformats.extend([''] * num_columns)
        xformats = xformats[:num_columns]

        return xheadings, xformats, xcellgrid

    def _process_headings(
            self,
            headings: Iterable[str],
            formats: Iterable[str],
            cellgrid_row: Row
            ) -> List[MonoBlock]:
        """Determine align for each heading, convert to MonoBlocks."""

        heading_monoblocks = []     # type: List[MonoBlock]
        for heading, format_str, cell in zip(headings, formats, cellgrid_row):
            align, text = monotable.alignment.split_up(
                heading, self.align_spec_chars)
            format_align, _ = monotable.alignment.split_up(
                format_str, self.align_spec_chars)

            # alignment for headings is determined by presence of
            # heading align_spec, format align_spec or by type (numeric or
            # all other) of the cell in the column.
            default = self._halign_suggestion(cell)    # type: int
            head_align = align or format_align or default    # type: int
            heading_monoblocks.append(MonoBlock(text, head_align))
        return heading_monoblocks

    @staticmethod
    def _halign_suggestion(item: Cell) -> int:
        """
        Return horizontal alignment enum value determined from the item type.
        """
        if isinstance(item, numbers.Number):
            return RIGHT
        else:
            return LEFT

    def _process_formats(self, formats: List[str]) -> List[FormatScanner]:
        """Scan format for align_spec, format_spec, and format options.

        Return list of FormatScanner instances that describe
        information scanned from the format directive string.
        """

        processed_formats = []    # type: List[FormatScanner]

        # Copy class vars to pass to monotable.scanner.FormatScanner().
        # option_spec_delimiters refers to the delimiters for the
        # format directives.
        instance_config = monotable.scanner.MonoTableConfig(
            align_spec_chars=self.align_spec_chars,
            sep=self.sep,
            format_func=self.format_func,
            format_func_map=self.format_func_map,
            option_spec_delimiters=self.option_spec_delimiters)

        for column_index, format_str in enumerate(formats):
            formatobj = monotable.scanner.FormatScanner(
                format_str,
                instance_config
                )
            if formatobj.error_text:
                fmt = 'cell column {:d}, format= {}\n{}'
                error_message = fmt.format(
                    column_index,
                    format_str,
                    formatobj.error_text)
                assert False, error_message

            processed_formats.append(formatobj)
        return processed_formats

    def _format_cells_as_columns(
            self,
            cellgrid: CellGrid,
            processed_formats: List[FormatScanner]
            ) -> List[List[MonoBlock]]:
        """Format each cell of cellgrid by calling the format_func.

        cellgrid
            Iterable of Iterable of Python values representing table cells.

        processed_formats
            List of instances of FormatScanner.  Each instance
            contains information to control cell formatting.

        Return a list containing columns of MonoBlocks.

        For each cell, create a MonoBlock from the format_func result.
        The horizontal alignment for the cell is determined and set at
        MonoBlock creation time.

        Caller assures len() of processed_formats and every row in
        cellgrid are equal.  Calling _extend_short_rows() takes care of this.
        If the cell is a MonoBlock instance, skip all the formatting
        steps and put a copy of the MonoBlock directly in the output.

        If the cell is None, treat it as a MonoBlock.
        """

        formatted_columns = []    # type: List[List[MonoBlock]]
        cell_columns = _transpose(cellgrid)

        column_index_range = range(len(processed_formats))

        inputs = zip(
            column_index_range,
            processed_formats,
            cell_columns)

        for column_index, formatobj, cell_column in inputs:

            formatted_column = self._formatting_step(
                column_index,
                formatobj,
                cell_column)

            # pre-justify numbers when using parentheses formatting directive
            parentheses_column = self._justify_parentheses(
                formatobj,
                cell_column,
                formatted_column)

            monoblock_column = self._width_step(
                formatobj, cell_column,
                parentheses_column)

            formatted_columns.append(monoblock_column)

        return formatted_columns

    def _formatting_step(
            self,
            column_index: int,
            formatobj: FormatScanner,
            cell_column: Iterable[Cell],
            ) -> List[Union[MonoBlock, str]]:
        """Format cells in the column and handle special case cells."""
        formatted_column = []    # type: List[Union[MonoBlock, str]]
        for row_index, item in enumerate(cell_column):

            # for special cases a MonoBlock is created immediately.
            block1 = self._special_cases(item, formatobj)
            if block1 is not None:
                formatted_column.append(block1)
                continue

            item_format_spec = self._make_format_spec(item, formatobj)

            try:
                text = formatobj.format_func(item, item_format_spec)
            except (AttributeError, LookupError, TypeError, ValueError,
                    ArithmeticError, AssertionError):
                msg = traceback.format_exc()
                exc = MonoTableCellError(
                    row_index,
                    column_index,
                    item_format_spec,
                    msg)  # type: MonoTableCellError
                text = self.format_exc_callback(exc)

            # for parentheses directive enclose negative numbers with (, ).
            if formatobj.parentheses and isinstance(item, numbers.Number):
                if text.startswith('-'):
                    text = text[1:].join('()')

            # for zero directive replace the formatted number if all zeros.
            if formatobj.zero is not None and isinstance(item, numbers.Number):
                is_digit = [c in string.digits for c in text]
                is_zero = [c == string.digits[0] for c in text]
                if is_digit == is_zero:  # are all digits present zero?
                    text = formatobj.zero

            formatted_column.append(text)
        return formatted_column

    @staticmethod
    def _justify_parentheses(
            formatobj: FormatScanner,
            cell_column: Iterable[Cell],
            formatted_column: List[Union[MonoBlock, str]]
            ) -> List[Union[MonoBlock, str]]:
        """If parentheses directive re-justify since added all|some|no ')'."""

        if not formatobj.parentheses:
            return formatted_column    # nothing to do

        # select text strings that were formatted from cells that were numbers.
        formatted_numbers = []
        for item, text in zip(cell_column, formatted_column):
            if isinstance(item, numbers.Number) and isinstance(text, str):
                formatted_numbers.append(text)

        # for the formatted numbers, determine if any but not all
        # are enclosed by parentheses.
        has_parentheses = [text.endswith(')') for text in formatted_numbers]
        if not any(has_parentheses) or all(has_parentheses):
            return formatted_column    # not a mix of (xxx) and yyy.

        # since there are some with parentheses and some without, the
        # formatted numbers without parentheses are padded with one space
        # to maintain vertical alignment of the digits/decimal point.
        # (provided the column is ultimately right justified).
        parentheses_column = []    # type: List[Union[MonoBlock, str]]

        # Note that formatted_column contains a mix of str and MonoBlock.
        # The MonoBlocks get there by bypassing the formatting step.
        # To satisfy mypy, make sure there is no path that calls
        # endswith() on a MonoBlock.
        # This is done by explicitly testing that the variable text
        # is a str before calling text.endswith().
        for item, text in zip(cell_column, formatted_column):
            if (isinstance(item, numbers.Number)
                    and isinstance(text, str)
                    and not text.endswith(')')):
                parentheses_column.append(text + ' ')
            else:
                # This branch handles:
                # 1. formatted text for items that aren't numbers
                # 2. entries from formatted_column that are MonoBlocks
                #    inserted by _special_cases().
                # 3. formatted text for items that are numbers for the cases
                #    where all or none in the column has parentheses.
                parentheses_column.append(text)

        return parentheses_column

    def _width_step(
            self,
            formatobj: FormatScanner,
            cell_column: Iterable[Cell],
            formatted_column: List[Union[MonoBlock, str]]
            ) -> List[MonoBlock]:
        """Create MonoBlocks, determine alignment, implement width control."""
        if formatobj.width is not None and formatobj.wrap:
            text_wrapper = textwrap.TextWrapper(
                width=formatobj.width,
                break_long_words=True)    # type: Optional[textwrap.TextWrapper]    # noqa : E501

        else:
            text_wrapper = None

        monoblock_column = []
        for item, text in zip(cell_column, formatted_column):

            # Special case MonoBlocks are not subject to the
            # wrap format directive.
            if isinstance(text, MonoBlock):
                monoblock_column.append(text)
                continue

            if text_wrapper is not None:
                text = text_wrapper.fill(text)

            if formatobj.align == NOT_SPECIFIED:
                align = self._halign_suggestion(item)
            else:
                align = formatobj.align
            block = MonoBlock(text, align)
            monoblock_column.append(block)

        # All MonoBlocks are subject to column width control specified
        # by the width= and fixed directives.
        for block in monoblock_column:
            self._adjust_width(formatobj, block)
        return monoblock_column

    def _special_cases(
            self,
            item: Cell,
            formatobj: FormatScanner
            ) -> Optional[MonoBlock]:
        """Handle special cases that make a MonoBlock without format_func."""

        if isinstance(item, _HR):
            # The _HR instance is replaced with an _InternalGuideline.
            # The formatting steps are skipped.
            # _InternalGuideline is a subclass of MonoBlock so that
            # it can participate in justification steps later on.
            # This is done to avoid writing extra code to pass
            # _InternalGuideline cells around the justify logic.
            # A row starting with _InternalGuideline is replaced
            # when the table is composed from the individual
            # rows.
            return _InternalGuideline()

        elif item is None:
            # Replace None with a MonoBlock initialized from
            # formatting directive none=ccc (or use the class variable
            # format_none_as) and bypass the formatting steps.
            # Type None auto-aligns to the left since it is not a number.
            if formatobj.align == NOT_SPECIFIED:
                align = LEFT
            else:
                align = formatobj.align

            if formatobj.none is None:
                formatted_text = self.format_none_as
            else:
                formatted_text = formatobj.none

            return MonoBlock(formatted_text, align)

        elif isinstance(item, MonoBlock):
            # MonoBlocks enjoy the privilege of bypassing the
            # formatting and format option steps.  The skipped steps
            # produce a MonoBlock anyway.
            #
            # A short row in the cellgrid has been extended with one
            # or more MonoBlock instances.  Since these bypass the
            # formatting and format option steps there is no chance
            # of failing these steps.
            #
            # The copy is made because MonoBlocks are modified
            # individually by the justification steps.
            return copy.copy(item)
        else:
            return None

    def _make_format_spec(self, item: Cell, formatobj: FormatScanner) -> str:
        """Return a custom format_spec if special cases."""

        format_spec = formatobj.format_spec

        # Set the precision of float items to default_float_format_spec
        # when all of the following:
        #    - using BIF format()
        #    - empty format_spec string
        #    - non-empty class var default_float_format_spec
        if (isinstance(item, float) and
                format_spec == '' and
                formatobj.format_func == format and  # BIF format()
                self.default_float_format_spec):
            format_spec = self.default_float_format_spec

        return format_spec

    def _adjust_width(
            self,
            formatobj: FormatScanner,
            block: MonoBlock
            ) -> None:
        """Control width of block.  Modifies callers block."""

        if formatobj.width is not None:
            # truncate too long lines
            block.chop_to_fieldsize(formatobj.width, self.more_marker)
            if formatobj.fixed:
                # pad to width=N too short lines
                block.hjustify(formatobj.width)

    @staticmethod
    def _make_list_of_seps(
            processed_formats: List[FormatScanner]) -> List[str]:
        """
        Make list of column right side separator strings.

        The separator string is applied on the right side of the column.
        The last column's separator string will be the empty string,
        """

        rseps = []    # type: List[str]
        for formatobj in processed_formats:
            # if lsep= option for this column, unconditionally set the
            # previous coloumn's rsep to lsep,
            # Silently ignore lsep on the first column.
            if rseps and formatobj.lsep is not None:
                rseps[-1] = formatobj.lsep

            rseps.append(formatobj.sep)

        if rseps:
            rseps[-1] = ''  # rsep after last column is always empty string.
        return rseps

    @staticmethod
    def _calculate_column_widths(
            heading_monoblocks: List[MonoBlock],
            cell_monoblock_columns: List[List[MonoBlock]]) -> List[int]:
        """Determine width of each column in the table."""

        # width is length of widest heading or formatted cell
        heading_column_widths = [t.width for t in heading_monoblocks]
        cellgrid_column_widths = []
        for col in cell_monoblock_columns:
            cellgrid_column_widths.append(max([t.width for t in col]))

        table_widths = [max(hwidth, cwidth) for hwidth, cwidth in
                        zip(heading_column_widths, cellgrid_column_widths)]
        return table_widths

    def _justify_headings(
            self,
            processed_headings: List[MonoBlock],
            widths: List[int]
            ) -> None:
        """Justify headings horizontally and vertically."""

        # The caller typically sets the halign attribute at MonoBlock
        # creation time.
        for tb, width in zip(processed_headings, widths):
            tb.hjustify(width)

        # vertically justify headings
        if processed_headings:
            max_heading_height = max([t.height for t in processed_headings])
            for tb in processed_headings:
                tb.vjustify(self.heading_valign,
                            max_heading_height, more_marker='n/a')

    def _justify_cell_columns(
            self,
            cell_monoblock_columns: List[List[MonoBlock]],
            widths: List[int]
            ) -> None:
        """Justify cell columns horizontally and vertically."""

        # The caller typically sets the halign attribute at MonoBlock
        # creation time.
        for column, width in zip(cell_monoblock_columns, widths):
            for tb in column:
                tb.hjustify(width)

        # vertically justify cells
        monotable.alignment.validate_vertical_align(self.cell_valign)
        cell_rows = _transpose(cell_monoblock_columns)
        for row in cell_rows:
            row_height = max([t.height for t in row])
            if not self.max_cell_height:  # configured height limit?
                height = row_height       # no-
            else:
                # yes- don't exceed the height limit
                height = min(self.max_cell_height, row_height)

            for tb in row:
                tb.vjustify(self.cell_valign, height, self.more_marker)

    def _make_guidelines(
            self,
            table_width: int,
            widths: List[int],
            seps: List[str]
            ) -> List[str]:
        # Return tuple (top guideline, heading guideline, bottom guideline).
        # Create them based on the first 3 chars in self.guideline_chars.
        # The corresponding guideline is the empty string if the char is
        # a space or if self.guideline_chars is less than 3 chars long.
        #
        # Separated guidelines have the column sep characters between
        # columns.  This looks good when the seps are all spaces.

        # Assure len()==3.
        three_chars = (self.guideline_chars + '   ')[:3]

        if self.separated_guidelines:
            # Create guidelines with seps between columns.
            guidelines = []    # type: List[str]
            for guideline_char in three_chars:
                if guideline_char == ' ':
                    guidelines.append('')
                else:
                    guideline_parts = [(guideline_char * width) + sep
                                       for width, sep in zip(widths, seps)]
                    guidelines.append(''.join(guideline_parts))
            return guidelines
        else:
            # Create guidelines with no spaces.
            guidelines = [c * table_width for c in three_chars]
            stripped = [guideline.strip() for guideline in guidelines]
            return stripped

    def _make_title_lines(self, title: str, width: int) -> List[str]:
        """Convert title to text lines and justify if narrower than table."""

        align, text = monotable.alignment.split_up(title,
                                                   self.align_spec_chars)
        if self.wrap_spec_char and text.startswith(self.wrap_spec_char):
            text = text[1:]
            if width:
                wrapper = textwrap.TextWrapper(
                    width=width,
                    break_long_words=False)
                text = wrapper.fill(text)
        mb = MonoBlock(text, align)
        if mb.width <= width:
            mb.hjustify(width)
        return mb.lines

    @staticmethod
    def _has_headings(justified_headings: List[MonoBlock]) -> bool:
        """False when all heading MonoBlocks contain only spaces."""

        return any((not t.is_all_spaces() for t in justified_headings))

    @staticmethod
    def _monoblock_row_to_strings(
            row_of_monoblocks: Sequence[MonoBlock],
            seps: Optional[List[str]] = None
            ) -> List[str]:
        """Convert a row of MonoBlock to a list of lines.

        Returns a list of text lines.
        If seps is None no text is inserted between columns.
        If seps is a list, insert from list after each column.
        """
        lines = []
        text_columns = [t.lines for t in row_of_monoblocks]
        text_rows = _transpose(text_columns)
        if seps is None:
            seps = [''] * len(row_of_monoblocks)  # 1 sep per column
        for textrow in text_rows:
            line = ''.join(''.join(pair) for pair in zip(textrow, seps))
            lines.append(line)
        return lines

    def bordered_table(
            self,
            headings: Iterable[str] = (),
            formats: Iterable[str] = (),
            cellgrid: CellGrid = ((),),
            title: str = '',
            ) -> str:
        """Format printable text table with individual cell borders.

        Args:
            headings
                Iterable of strings for each column heading.

            formats
                Iterable of format strings of the form
                ``[align_spec][directives][format_spec]``.
                `Format directive string syntax`_

            cellgrid
                representing table cells.

            title
                ``[align_spec][wrap_spec]string``.
                Text to be aligned and printed above the text table.
                `Title string syntax`_

        Returns:
            The text table as a single string.

        Raises:
            MonoTableCellError

        Here is an example of bordered text table:

        .. code-block:: none

            +----------------------+------------------+  <-- top guideline
            | format string        | format string    |  <-- heading row
            | "%Y-%m-%d--%I:%M:%S" | "week-%U-day-%j" |
            +======================+==================+  <-- heading guideline
            | 2016-01-10--07:35:18 | week-02-day-010  |  <-- cell row
            +----------------------+------------------+  <-- bottom guideline
        """

        # Assure there are exactly 5 border chars.  Extend the string
        # with '+'s if it is too short.  Truncate if it is too long. 1 char
        # each for border: top, bottom, sides, corner, heading guideline.
        border_chars = (self.border_chars + '+++++')[:5]

        # convert, format, and justify headings/cells into MonoBlock objects
        (justified_headings, justified_cells,
            widths, _) = self._format_and_justify(
                    headings,
                    formats,
                    cellgrid)
        lines = []  # lines of printable text

        table_has_headings = self._has_headings(justified_headings)

        # renames to be used below
        bottom_border_char = border_chars[1]
        bordered_heading_guideline_char = border_chars[4]

        # add borders to the heading MonoBlocks.
        if table_has_headings:
            self._add_borders_to_monoblock_row(justified_headings,
                                               border_chars)
            # add list of printable lines obtained from the headings
            lines.extend(self._monoblock_row_to_strings(justified_headings))

            # substitute the border heading guideline char for the bottom chars
            # in the last line of the headings
            # example: +--------+-----+ -> +========+=====+ when
            # self.border_chars='_-|+='
            lines[-1] = lines[-1].replace(bottom_border_char,
                                          bordered_heading_guideline_char)

        for row in justified_cells:
            self._add_borders_to_monoblock_row(row, border_chars)

        # if headings remove top border line of all cells
        # if no headings remove top border line from all but first row of cells
        start = 0 if table_has_headings else 1
        for row in justified_cells[start:]:
            for monoblock in row:
                monoblock.remove_top_line()

        # convert cell rows to printable lines
        for row in justified_cells:
            lines.extend(self._monoblock_row_to_strings(row))

        # prepend the title lines above the table
        if title:
            table_width = self._calculate_bordered_table_width(widths)
            title_lines = self._make_title_lines(title, table_width)
            lines = title_lines + lines

        # strip trailing spaces
        lines = [line.rstrip() for line in lines]

        return self.indent + ('\n' + self.indent).join(lines)

    def _add_borders_to_monoblock_row(
            self,
            row_of_monoblocks: Sequence[MonoBlock],
            border_chars: str
            ) -> None:
        """Add borders to row of monoblocks.  Modifies in-place."""

        for monoblock in row_of_monoblocks:
            monoblock.add_border(
                self.hmargin,
                self.vmargin,
                border_chars[:-1])  # w/o guideline
        # only need one side border between adjacent columns
        for monoblock in row_of_monoblocks[1:]:
            monoblock.remove_left_column()

    def _calculate_bordered_table_width(
            self,
            widths_before_borders: List[int]
            ) -> int:
        """Calculate width of entire table with borders."""

        num_columns = len(widths_before_borders)
        if num_columns == 0:
            return 0
        else:
            num_hmargin_chars = 2 * self.hmargin * num_columns
            num_side_chars = num_columns + 1
            return (sum(widths_before_borders) +
                    num_hmargin_chars + num_side_chars)

    def row_strings(
            self,
            headings: Iterable[str] = (),
            formats: Iterable[str] = (),
            cellgrid: CellGrid = ((),),
            strip: bool = False,
            ) -> List[List[str]]:
        """Format and justify table.  Return rows of the strings.

        Args:
            headings
                Iterable of strings for each column heading.

            formats
                Iterable of format strings of the form
                ``[align_spec][directives][format_spec]``.
                `Format directive string syntax`_

            cellgrid
                representing table cells.

            strip
                If True remove leading and trailing spaces.

        Returns:
            list of rows of string : First row is headings, following rows
            are formatted cell strings.

        Raises:
            MonoTableCellError

        When strip=False, each heading and all cells in each column are
        justified and are the same length.
        """

        # convert, format, and justify headings/cells into MonoBlock objects
        (justified_headings, justified_cells,
            unused1, unused2) = self._format_and_justify(headings,
                                                         formats,
                                                         cellgrid)
        # Combine the resulting MonoBlocks into a single list.
        # Headings is the first row followed by the cell rows.
        #
        # typing cast explained:
        # Given the parameters
        # justified_headings is type List[MonoBlock] and
        # justified_cells is type List[Tuple[MonoBlock]].
        #
        # justified_headings needs to be Tuple[MonoBlock] so that
        # after enclosing it in a List the List is of type
        # List[Tuple[MonoBlock]].
        # That type is needed so that it can be extended with
        # justified_cells which is also type List[Tuple[MonoBlock]].
        tupled_justified_headings = cast(Tuple[MonoBlock], justified_headings)
        combined = [tupled_justified_headings]
        combined.extend(justified_cells)

        # Convert to strings/strip.
        rows = []    # type: List[List[str]]
        for monoblock_row in combined:
            row = [str(block) for block in monoblock_row]
            if strip:
                row = [item.strip() for item in row]
            rows.append(row)
        return rows

    def cotable(
            self,
            column_tuples: Sequence[ColumnTuple] = (),
            title: str = '',
            ) -> str:
        """Format printable text table from tuples describing columns.

        Args:
            column_tuples
                List of tuple of (heading string, format string,
                iterable of cell objects).

                The heading string syntax is described here
                :py:meth:`~MonoTable.table` under the parameter headings.
                The column tuple has a single heading string.

                The format directive string syntax is described here
                :py:meth:`~MonoTable.table` under the
                parameter formats.
                The column tuple has a single format string.

                Iterable of cell objects represent the cells in the column.

            title
                ``[align_spec][wrap_spec]string``.
                Text to be aligned and printed above the text table.
                `Title string syntax`_

        Returns:
            The text table as a single string.

        Raises:
            MonoTableCellError
        """
        if len(column_tuples) == 0:
            return title
        for tup in column_tuples:
            assert len(tup) == 3, 'Short tuple or missing enclosing list.'
        headings, formats, cell_columns = zip(*column_tuples)
        cellgrid = zip_longest(*cell_columns)
        return self.table(headings, formats, cellgrid, title)

    def cobordered_table(
            self,
            column_tuples: Sequence[ColumnTuple] = (),
            title: str = ''
            ) -> str:
        """Format printable bordered text table from tuples describing columns.

        Args:
            column_tuples
                List of tuple of (heading string, format string,
                iterable of cell objects).

                The heading string syntax is described here
                :py:meth:`~MonoTable.table` under the parameter headings.
                The column tuple has a single heading string.

                The format directive string syntax is described here
                :py:meth:`~MonoTable.table` under the
                parameter formats.
                The column tuple has a single format string.

                Iterable of cell objects represent the cells in the column.

            title
                ``[align_spec][wrap_spec]string``.
                Text to be aligned and printed above the text table.
                `Title string syntax`_

        Returns:
            The text table as a single string.

        Raises:
            MonoTableCellError
       """
        if len(column_tuples) == 0:
            return title
        for tup in column_tuples:
            assert len(tup) == 3, 'Short tuple or missing enclosing list.'
        headings, formats, cell_columns = zip(*column_tuples)
        cellgrid = zip_longest(*cell_columns)
        return self.bordered_table(headings, formats, cellgrid, title)


# Convenience Functions

def table(
        headings: Iterable[str] = (),
        formats: Iterable[str] = (),
        cellgrid: CellGrid = ((),),
        title: str = '',
        ) -> str:
    """Wrapper to :py:meth:`monotable.table.MonoTable.table`."""
    tbl = MonoTable()
    return tbl.table(headings, formats, cellgrid, title)


def bordered_table(
        headings: Iterable[str] = (),
        formats: Iterable[str] = (),
        cellgrid: CellGrid = ((),),
        title: str = '',
        ) -> str:
    """Wrapper to :py:meth:`monotable.table.MonoTable.bordered_table`."""
    tbl = MonoTable()
    return tbl.bordered_table(headings, formats, cellgrid, title)


def cotable(
        column_tuples: Sequence[ColumnTuple] = (),
        title: str = '',
        ) -> str:
    """Wrapper to :py:meth:`monotable.table.MonoTable.cotable`."""
    tbl = MonoTable()
    return tbl.cotable(column_tuples, title)


def cobordered_table(
        column_tuples: Sequence[ColumnTuple] = (),
        title: str = '',
        ) -> str:
    """Wrapper to :py:meth:`monotable.table.MonoTable.cobordered_table`."""
    tbl = MonoTable()
    return tbl.cobordered_table(column_tuples, title)


class _InternalGuideline(MonoBlock):
    """
    Internal indication to insert a horizontal rule instead of a row of cells.

    A row that starts with this instance is omitted from the
    table and a heading guideline is formatted in its place.
    This is a subclass of MonoBlock so that it can pass through
    the justify steps as if it were a typical formatted cell.
    """
    pass
