# Copyright 2017 Mark Taylor
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

"""ASCII table: per column format specs, plug-in format functions, multi-line.

   Formats 2D array of Python objects to ASCII table format.
   The table looks pretty when printed in a monospaced font.
   See class MonoTable docstring for details.

   Classes:
   MonoTable   Format Python objects to ASCII table for monospaced font.

   Exceptions:
   MonoTableCellError  Created when formatting a cell fails.

   Attributes:
   HR             In column 0 of a row, horizontal rule should be inserted.
"""


import copy
import numbers
import sys
import textwrap
import traceback

import monotable.plugin
import monotable.scanner

from monotable.monoblock import MonoBlock

from monotable.alignment import NOT_SPECIFIED
from monotable.alignment import LEFT
from monotable.alignment import RIGHT

# repository: https://github.com/tmarktaylor/monotable
# Docstrings are Google Style for Sphinx plugin sphinx.ext.napoleon.


def _transpose(grid):
    """Swap rows for columns or columns for rows."""

    return list(zip(*grid))


class _HR:
    """Type to distinguish a horizontal rule from other cell types."""
    pass


HR = _HR()
"""Placed in column 0 of a *row* in a cellgrid to insert a horizontal rule.

A row that starts with a HR is omitted from the
table and a heading guideline is inserted in its place.
"""


class MonoTable:
    """Create an aligned and formatted text table from a grid of cells.

    Pass a sequence of heading strings and a
    sequence of format strings to the constructor.  Call
    :py:meth:`~MonoTable.table` passing a sequence of sequence of
    cells and a title string.
    The return value is a string ready for printing.

    Call :py:meth:`~MonoTable.bordered_table` with the same arguments
    to format a table with character borders.

    Call :py:meth:`~MonoTable.row_strings` passing a sequence of sequence of
    cells to return a tuple of lists of formatted headings and
    list of list of cells.

    Heading strings, title strings, and formatted cells may contain
    newlines.

    Cells that inherit from numbers.Number are *Auto-Aligned* to the right
    and all other cell types are auto aligned to the left.

    align_spec
        One of the characters '<', '^', '>'.  The characters
        indicate left, center, and right justification.
        To configure, override the class variable
        :py:attr:`~MonoTable.align_spec_chars`.

    Heading String
        [align_spec]string

    Format String
        [align_spec][option_spec][format_spec]

    Title String
        [align_spec][wrap_spec]string

    * The format string syntax is described by the
      :py:meth:`~MonoTable.__init__` argument **formats** below.

    * Heading alignment is determined by this decision order:

        1. align_spec if present in the heading string.
        2. align_spec if present in the format string.
        3. Auto-Alignment for the cell in the first row.

    * Cell alignment is determined by this decision order:

        1. align_spec if present in the format string.
        2. Auto-Alignment for the cell in the first row.

    * The title is auto-aligned to center.

    :note:
        The align_spec prefix may be omitted, but is required if the
        rest of the string starts with one of the align_spec_chars.
        Or the user can put in any empty option_spec for example '()'.

    :note:
        align_spec scanning/parsing can be disabled by setting the
        class variable :py:attr:`~MonoTable.align_spec_chars` to
        the empty string.

    There is one format string for each column of cells.
    Please see description of :py:meth:`~MonoTable.__init__`
    argument **formats**.

    Formatting, by default, is done by ``<built-in function format>``.

        * The user can specify a different default format function for the
          table by overriding the class variable
          :py:attr:`~MonoTable.format_func`.  Be sure to use staticmethod().
        * In option_spec the user can specify a format function for
          a column which takes precedence over the table default format
          function.

          =============  ========================  =========================
          option name    format function           description
          =============  ========================  =========================
          mformat        monotable.plugin.mformat  mapping with str.format()
          pformat        monotable.plugin.pformat  printf-style
          sformat        monotable.plugin.sformat  str.format()
          tformat        monotable.plugin.tformat  string.Template()
          function-name  \                         user defined function
          =============  ========================  =========================


        * Any user defined function in the dict assigned to the class variable
          :py:attr:`~MonoTable.format_func_map`
          may be selected by putting its key as an option in option_spec.

    Here is the data flow through the formatting engine:

    .. code-block:: none

        cell -> format_func -> [width=N] ->
                format_spec    [fixed]
                               [wrap]

        * width=N is selected by option_spec and may be omitted.
        * N = width of field (characters).
        * fixed and wrap are selected by option_spec to
          modify width's behaviour.
        * fixed truncates or pads to exactly width=N columns.
        * wrap textwraps.

    * If cell is None an empty string is formatted.
      Configure by overriding class variable
      :py:attr:`~MonoTable.format_none_as`.
    * If a cell is float and format_spec is an empty string, the cells
      is formatted using class variable :py:attr:`~default_float_format_spec`.
    * Internally, if a cell is a MonoBlock the formatting engine is skipped.

    option_spec can contain the option `sep=` which sets the separator
    string placed after the column.

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
    a column format string option_spec specifies a format function.

    When overriding in a subclass definition use the result of
    Python built in function staticmethod() like this:

    >>> import monotable
    >>> def your_user_defined_format_function():
    ...    pass
    >>> class SubclassMonoTable(monotable.MonoTable):
    ...     format_func = staticmethod(your_user_defined_format_function)
    >>>
    >>> # Or this...
    >>>
    >>> class SubclassMonoTable(monotable.MonoTable):
    ...     format_func = staticmethod(monotable.plugin.sformat)
    >>>
    >>> # When overriding on an instance do not use staticmethod.
    >>>
    >>> tbl = monotable.MonoTable()
    >>> tbl.format_func = monotable.plugin.sformat

    .. _Docs Here:
       https://docs.python.org/3/howto/descriptor.html#functions-and-methods

    Reading Python functions and methods `Docs Here`_ helps explain when
    to use @staticmethod.
    """

    format_exc_callback = staticmethod(monotable.plugin.raise_it)
    """ Function called when format_func raises an exception.

    The function takes the argument MonoTableCellError and
    (if returning) returns the string to be returned by format_func.

    When overriding in a subclass definition use the result of
    Python built in function staticmethod() like this:

    >>> import monotable
    >>> def your_exc_callback_function(exc):
    ...    pass
    >>> class SubclassMonoTable(monotable.MonoTable):
    ...     format_exc_callback = staticmethod(your_exc_callback_function)
    >>>
    >>> # Or this...
    >>>
    >>> class SubclassMonoTable(monotable.MonoTable):
    ...     format_exc_callback = staticmethod(monotable.plugin.ignore_it)
    >>>
    >>> # When overriding on an instance do not use staticmethod.
    >>>
    >>> tbl = monotable.MonoTable()
    >>> tbl.format_exc_callback = monotable.plugin.ignore_it

    .. _Docs Here:
       https://docs.python.org/3/howto/descriptor.html#functions-and-methods

    Reading Python functions and methods `Docs Here`_ helps explain when
    to use @staticmethod.
    """

    default_float_format_spec = '.6f'
    """Default format specification for float type.

    Applies only to item of type float passed to the default
    format function: <built-in function format>.  If the
    format_spec is the empty string this value is used instead.
    This sets the precision to align the decimal points in a column
    of floats.
    Disable this feature by setting to the empty string.
    """

    sep = '  '
    """String that separates columns in non-bordered tables.

    sep after a column can be overridden by the format string
    option_spec option called sep.
    """

    separated_guidelines = False
    """When True guidelines will have the sep characters between columns.

    This looks good when the seps are all spaces.
    When False the guideline character is repeated for the width
    of the table.  seps refers to characters placed between heading and
    cell columns in the table.
    """

    format_func_map = None
    """Adds format functions selectable by a column format string option_spec.

    Dictionary of format functions keyed by name.
    name, when used as a format option in format string option_spec, selects
    the corresponding function from the dictionary.  If a key
    is one of 'mformat', 'pformat', 'sformat', or 'tformat' and is used
    in a format string option_spec the function from format_func_map
    will be selected.
    """

    format_none_as = ''
    """Value placed in table for cell of type None."""

    more_marker = '...'
    """Inserted to indicate text has been omitted."""

    align_spec_chars = '<^>'
    """Three characters to indicate justification.

    Applies to align_spec scanning in heading, title, and format strings.
    The first indicates left justification.  The second and third
    indicate center and right justification.
    Setting align_spec_chars to "" disables align_spec scanning.
    """

    wrap_spec_char = '='
    """Single character to indicate the title should be text wrapped.

    Wrapping is done to the width of the table.
    Setting wrap_spec_char to "" disables title text wrap.
    """

    option_spec_delimiters = '(;)'
    """Three characters to enclose and separate format options.

    The first and third chars enclose the options.
    The second char separates individual options. Setting
    option_spec_delimiters to "" disables option_spec scanning
    in format strings.
    """

    guideline_chars = '---'
    """String of 0 to 3 characters to specify guideline apperance.

    The first character is used for the top guideline.
    The second and third characters are used for the heading guideline
    and bottom guideline.  If the character is a space the
    guideline is omitted.  The empty string supresses all guidelines.
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

    max_cell_height = None
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

    def __init__(self,
                 headings=(),
                 formats=(),
                 indent=''):
        """
        Args:
            headings (Optional[Iterable[str]]):
                Iterable of strings for each column heading.

            formats (Optional[Iterable[str]]):
                Iterable of format strings of the form
                ``[align_spec][option_spec][format_spec]``.

                align_spec
                    One of the characters '<', '^', '>' to
                    override auto-alignment.

                option_spec
                    One or more of `options`_ enclosed by '(' and ')'
                    separated by ';'.

                        * Each option is allowed once in an option_spec.
                        * Spacing before and after '=' is ignored except after
                          ``sep =`` where spacing becomes part of sep.
                        * The options are shown following the arg list.

                format_spec
                    String passed to the format function.


            indent (Optional[str]):
                String added to the beginning of each line in the text table.

        The ``option_spec`` options are:

        .. _options:

        width=N
            Truncate each formatted cell line to width N and
            insert the class variable :py:attr:`more_marker` if text was
            omitted.

        fixed
            Format text to exactly width = N columns.

        wrap
            Do textwrap of formatted cell to width = N.

        sep=ccc
            Characters after 'sep=' are the column separator on the
            right hand side of the column.

        mformat
            Use :py:func:`monotable.plugin.mformat` to format the cell.

        pformat
            Use :py:func:`monotable.plugin.pformat` to format the cell.

        sformat
            Use :py:func:`monotable.plugin.sformat` to format the cell.

        tformat
            Use :py:func:`monotable.plugin.tformat` to format the cell.

        function-name
            Use the function selected by key function-name
            in the dictionary supplied by class variable
            :py:attr:`~MonoTable.format_func_map`.
        """

        # User can override class and instance variables by assignment to
        # an instance.
        # To maintainers:
        # - No instance variables are dependent on any other
        #   instance variables.
        # - No instance variables are assigned outside of the constructor.
        #
        self.headings = headings
        self.formats = formats
        self.indent = indent

    def table(self, cellgrid=((),), title=''):

        """Format printable text table.  It is pretty in monospaced font.

        Args:
            cellgrid (Optional[Iterable[Iterable[Any]]]): of Python objects
                representing table cells.

            title (Optional[str]): ``[align_spec][wrap_spec]string``.
                Text to be aligned and printed above the text table.

                align_spec
                    One of the characters '<', '^', '>' to
                    override auto-alignment.

                wrap_spec
                    Character '=' to indicate the title
                    should be text wrapped to the width of the table.

        Returns:
            str : The text table as a single string.

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
                     sep          sep

        This example has 6 sep strings of 2 spaces each.  The seps are placed
        between columns in the heading line and between the columns in
        each of the 2 cell rows.
        """

        # convert, format, and justify headings/cells into MonoBlock objects
        justified_headings, justified_cells, widths, seps = (
            self._format_and_justify(self.headings,
                                     self.formats,
                                     cellgrid))

        table_width = sum(widths) + sum([len(s) for s in seps])

        top_guideline, heading_guideline, bottom_guideline = (
            self._make_guidelines(table_width, widths, seps))

        lines = []

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

    def _format_and_justify(self, headings, formats, cellgrid):
        """Format, align, and justify the text table.

        headings
            Iterable of strings for each table column heading.
            See description for the constructor argument 'headings'.

        formats
            Iterable of format strings used to format each column of cells.
            See description for the constructor argument 'formats'.

        cellgrid
            Iterable of Iterable of Python objects representing table cells.

        Returns tuple:
            Row of heading MonoBlocks ready to be justified.

            List of list of MonoBlocks representing formatted cells.
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
        processed_headings = self._process_headings(xheadings,
                                                    xformats,
                                                    xcellgrid[0])

        widths = self._calculate_column_widths(processed_headings,
                                               formatted_cell_columns)

        # Do both horizontal and vertical justification.  (In-place).
        self._justify_headings(processed_headings, widths)
        self._justify_cell_columns(formatted_cell_columns, widths)

        return (processed_headings,
                _transpose(formatted_cell_columns),
                widths,
                self._make_list_of_seps(processed_formats)
                )

    @staticmethod
    def _extend_short_rows(headings, formats, cellgrid):
        """Create new headings, formats, and cellgrid so rows are equal length.

        Returns new lists of headings, formats, and a new cellgrid.

        headings and formats must be Iterables.  cellgrid must be
        a Iterable of Iterable.  Sequences are fine as well.
        Extend too short headings or too short cell rows.
        Don't extend anything if too many formats, silently discard instead.

        Headings and formats are extended with the empty string.
        Cellgrid rows are extended with a single instance of MonoBlock.
        MonoBlock instances receive special handling during formatting.
        """

        # Convert cellgrid to list of lists in order to determine the length
        # of each row.  Also test that each row is iterable.
        xcellgrid = []
        for row in cellgrid:
            try:
                xcellgrid.append(list(row))  # copy and convert row to list
            except TypeError as exc:
                msg = 'If one row cellgrid, likely missing outer list.'
                assert False, 'Exception "{}". {}'.format(str(exc), msg)

        num_columns = max([len(headings)] + [len(row) for row in xcellgrid])

        # extend any short rows in xcellgrid
        for row in xcellgrid:
            row.extend([MonoBlock()] * (num_columns - len(row)))
            # It is OK to extend with same instance of MonoBlock because
            # of special handling later by _format_cells_as_columns().

        # Make copies and convert to list.
        # Extend by more than needed, truncate to len() = num_columns.
        xheadings = list(headings)
        xheadings.extend([''] * num_columns)
        xheadings = xheadings[:num_columns]

        xformats = list(formats)
        xformats.extend([''] * num_columns)
        xformats = xformats[:num_columns]

        return xheadings, xformats, xcellgrid

    def _process_headings(self, headings, formats, cellgrid_row):
        """Determine align for each heading, convert to MonoBlocks."""

        heading_monoblocks = []
        for heading, format_str, cell in zip(headings, formats, cellgrid_row):
            align, text = monotable.alignment.split_up(
                heading, self.align_spec_chars)
            format_align, _ = monotable.alignment.split_up(
                format_str, self.align_spec_chars)

            # alignment for headings is determined by presence of
            # heading align_spec, format align_spec or by type (numeric or
            # all other) of the cell in the column.
            default = self._halign_suggestion(cell)
            head_align = align or format_align or default
            heading_monoblocks.append(MonoBlock(text, head_align))
        return heading_monoblocks

    @staticmethod
    def _halign_suggestion(item):
        """
        Return horizontal alignment enum value determined from the item type.
        """
        if isinstance(item, numbers.Number):
            return RIGHT
        else:
            return LEFT

    def _process_formats(self, formats):
        """Scan format for align_spec, format_spec, and format options.

        Return list of FormatScanner instances that describe
        information scanned from the format string.
        """

        processed_formats = []

        # Copy class vars to pass to FormatScanner().
        instance_config = monotable.scanner.MonoTableConfig(
            align_spec_chars=self.align_spec_chars,
            sep=self.sep,
            format_func=self.format_func,
            format_func_map=self.format_func_map,
            option_spec_delimiters=self.option_spec_delimiters)

        for column_index, format_str in enumerate(formats):
            formatobj = monotable.scanner.FormatScanner(format_str,
                                                        instance_config)
            if formatobj.error_text:
                fmt = 'cell column {:d}, format= {}\n{}'
                error_message = fmt.format(
                    column_index,
                    format_str,
                    formatobj.error_text)
                assert False, error_message

            processed_formats.append(formatobj)
        return processed_formats

    def _format_cells_as_columns(self, cellgrid, processed_formats):
        """Format each cell of cellgrid by calling the format_func.

        cellgrid
            Iterable of Iterable of Python objects representing table cells.

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

        If the cell in None, treat it as a MonoBlock.
        """

        formatted_columns = []
        cell_columns = _transpose(cellgrid)

        column_index_range = range(len(processed_formats))

        inputs = list(zip(column_index_range,
                          processed_formats,
                          cell_columns))

        for column_index, formatobj, cell_column in inputs:
            formatted_column = []

            align = formatobj.align

            # renames to shorten long lines
            format_func = formatobj.format_func
            format_spec = formatobj.format_spec

            # create TextWrapper instance for the column if needed.
            if formatobj.wrap:
                text_wrapper = textwrap.TextWrapper(
                    width=formatobj.width,
                    break_long_words=True)
            else:
                text_wrapper = None

            for row_index, item in enumerate(cell_column):
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
                    formatted_column.append(_InternalGuideline())
                    continue

                if item is None:
                    # Replace None with an empty MonoBlock and
                    # bypass the formatting steps.
                    # If column width is fixed, justify the MonoBlock to
                    # pad out to the width=N value.  This will also truncate
                    # any too long lines duplicating downstream logic.
                    t1 = MonoBlock(self.format_none_as, halign=align)
                    if formatobj.fixed:
                        t1.hjustify(formatobj.width)
                    formatted_column.append(t1)
                    continue

                if isinstance(item, MonoBlock):
                    t2 = copy.copy(item)
                    if formatobj.fixed:
                        t2.hjustify(formatobj.width)
                    formatted_column.append(t2)
                    continue
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
                    #
                    # If column width is fixed, justify the MonoBlock to
                    # pad out to the width=N value.  This will also truncate
                    # any too long lines duplicating downstream logic.


                if align == NOT_SPECIFIED:
                    align = self._halign_suggestion(item)

                # Special case to set the precision of floating point value
                # so the decimal point will align in a column of floats.
                # If formatting a float with BIF format() that has an
                # empty string format_spec use the class variable value
                # as the format_spec.
                if (isinstance(item, float) and
                        format_spec == '' and
                        format_func == format and       # BIF format()
                        self.default_float_format_spec):
                    format_spec = self.default_float_format_spec

                try:
                    text = format_func(item, format_spec)
                # Catch probable errors but more narrowed than just
                # catching Exception.
                except (AttributeError, LookupError, TypeError, ValueError,
                        ArithmeticError, AssertionError):
                    msg = ''.join(
                        traceback.format_exception(*sys.exc_info()))
                    exc = MonoTableCellError(row_index,
                                             column_index,
                                             formatobj.format_spec,
                                             msg)
                    text = self.format_exc_callback(exc)

                if text_wrapper:
                    text = text_wrapper.fill(text)

                block = MonoBlock(text, align)

                if formatobj.width is not None:
                    # truncate too long lines
                    block.chop_to_fieldsize(formatobj.width, self.more_marker)
                    if formatobj.fixed:
                        # pad to width=N too short lines
                        block.hjustify(formatobj.width)

                formatted_column.append(block)
            formatted_columns.append(formatted_column)
        return formatted_columns

    @staticmethod
    def _make_list_of_seps(processed_formats):
        """Make list of column separator strings ending with empty string."""

        seps = []
        for formatobj in processed_formats:
            seps.append(formatobj.sep)
        if seps:
            seps[-1] = ''  # sep after last column is always empty string
        return seps

    @staticmethod
    def _calculate_column_widths(heading_monoblocks, cell_monoblock_columns):
        """Determine width of each column in the table."""

        # width is length of widest heading or formatted cell
        heading_column_widths = [t.width for t in heading_monoblocks]
        cellgrid_column_widths = []
        for col in cell_monoblock_columns:
            cellgrid_column_widths.append(max([t.width for t in col]))

        table_widths = [max(hwidth, cwidth) for hwidth, cwidth in
                        zip(heading_column_widths, cellgrid_column_widths)]
        return table_widths

    def _justify_headings(self, processed_headings, widths):
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

    def _justify_cell_columns(self, cell_monoblock_columns, widths):
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

    def _make_guidelines(self, table_width, widths, seps):
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
            guidelines = []
            for guideline_char in three_chars:
                if guideline_char == ' ':
                    guidelines.append('')
                else:
                    guideline_parts = [(guideline_char * width) + sep
                                       for width, sep in zip(widths, seps)]
                    guidelines.append(''.join(guideline_parts))
            return tuple(guidelines)
        else:
            # Create guidelines with no spaces.
            guidelines = [c * table_width for c in three_chars]
            stripped = [guideline.strip() for guideline in guidelines]
            return stripped

    def _make_title_lines(self, title, width):
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
    def _has_headings(justified_headings):
        """False when all heading MonoBlocks contain only spaces."""

        return any((not t.is_all_spaces() for t in justified_headings))

    @staticmethod
    def _monoblock_row_to_strings(row_of_monoblocks, seps=None):
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

    def bordered_table(self, cellgrid=((),), title=''):
        """Format printable text table with individual cell borders.

        Args:
            cellgrid (Optional[Iterable[Iterable[Any]]]): of Python objects
                representing table cells.

            title (Optional[str]): ``[align_spec][wrap_spec]string``.
                Text to be aligned and printed above the text table.

                align_spec
                    One of the characters '<', '^', '>' to
                    override auto-alignment.

                wrap_spec
                    Character '=' to indicate the title
                    should be text wrapped to the width of the table.

        Returns:
            str : The text table as a single string.

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
         widths, _) = self._format_and_justify(self.headings,
                                               self.formats,
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

    def _add_borders_to_monoblock_row(self, row_of_monoblocks, border_chars):
        """Add borders to row of monoblocks.  Modifies in-place."""

        for monoblock in row_of_monoblocks:
            monoblock.add_border(self.hmargin,
                                 self.vmargin,
                                 border_chars[:-1])  # w/o guideline
        # only need one side border between adjacent columns
        for monoblock in row_of_monoblocks[1:]:
            monoblock.remove_left_column()

    def _calculate_bordered_table_width(self, widths_before_borders):
        """Calculate width of entire table with borders."""

        num_columns = len(widths_before_borders)
        if num_columns == 0:
            return 0
        else:
            num_hmargin_chars = 2 * self.hmargin * num_columns
            num_side_chars = num_columns + 1
            return (sum(widths_before_borders) +
                    num_hmargin_chars + num_side_chars)

    def row_strings(self, cellgrid=((),), strip=False):
        """Format and justify table.  Return rows of the strings.

        Args:
            cellgrid (Optional[Iterable[Iterable[Any]]]): of Python objects
                representing table cells.

            strip (bool): If True remove leading and trailing spaces.

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
            _, _) = self._format_and_justify(self.headings,
                                             self.formats,
                                             cellgrid)
        # Combine the resulting MonoBlocks into a single list.
        # Headings is the first row followed by the cell rows.
        combined = [justified_headings]
        combined.extend(justified_cells)

        # Convert to strings/strip.
        rows = []
        for row in combined:
            row = [str(item) for item in row]
            if strip:
                row = [item.strip() for item in row]
            rows.append(row)
        return rows


class MonoTableCellError(Exception):
    """Raised when format_func fails.  Identifies the offending cell.

        Attributes:
            row (int):
                Cell grid row index of value causing format_func exception.

            column (int):
                Cell grid column index of value causing format_func exception.

            format_spec (str):
                Format_spec passed to format_func when exception occurred.

            trace_text (str):
                Exception trace information for root cause of the exception.

            name (str):
                Name of the exception shown in the string representation.
    """

    def __init__(self, row, column, format_spec='', trace_text=None):

        self.row = row
        self.column = column
        self.format_spec = format_spec
        self.trace_text = trace_text
        self.name = 'MonoTableCellError'

    def __str__(self):
        """Show cell's position, format_spec, and trace info."""

        fmt = '{}: cell[{:d}][{:d}], format_spec= {}'
        exception_msg = fmt.format(self.name,
                                   self.row,
                                   self.column,
                                   self.format_spec)

        if sys.version_info < (3,):
            # Python 2.x
            tfmt = '\n' + self.name + ' raised after catching:\n{:s}'
            return exception_msg + tfmt.format(self.trace_text)
        else:
            return exception_msg


class _InternalGuideline(MonoBlock):
    """
    Internal indication to insert a horizontal rule instead of a row of cells.

    A row that starts with this instance is omitted from the
    table and a heading guideline is formatted in its place.
    This is a subclass of MonoBlock so that it can pass through
    the justify steps as if it were a typical formatted cell.
    """
    pass
