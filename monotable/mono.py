# monotable ASCII table formatter.
#
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

"""Convenience function access to ASCII table class.
"""

from typing import Optional, Sequence, Iterable, List

from monotable.table import HR
from monotable.table import MonoTable
from monotable.table import CellGrid, Row, ColumnTuple, FormatFuncMap
from monotable.alignment import TOP


HR_ROW = (HR,)    # type: Row
"""Row containing a horizontal rule to use as a row in cellgrid."""

VR_COL = ('', '(lsep= |;rsep= )', ())    # type: ColumnTuple
"""Vertical rule column for use as a column_tuple with monocol()."""


def mono(
        headings: Iterable[str] = (),
        formats: Iterable[str] = (),
        cellgrid: CellGrid = ((),),
        title: str = '',
        *,
        bordered: bool = False,
        format_func_map: Optional[FormatFuncMap] = None,
        guideline_chars: str = '---',
        indent: str = ''
        ) -> str:
    """Generate ASCII table from cellgrid.

    Args:
        headings
            Iterable of strings for each column heading.

        formats
            Iterable of format strings of the form
            ``[align_spec][directives][format_spec]``.
            Please see :ref:`Format directive string syntax
            <Format directive string syntax>`.

        cellgrid
            representing table cells.

        title
            ``[align_spec][wrap_spec]string``.
            Text to be aligned and printed above the text table.
            Please see :ref:`Title string syntax <Title string syntax>`.

    Keyword Args:
        bordered
            True means generate table with ASCII cell border characters.

        format_func_map
            Dictionary of format functions keyed by name.
            name, when used as a format directive in a format string,
            selects the corresponding function from the dictionary.

            If a key is one of the included format directive function
            names like 'boolean', 'mformat', etc. the included format
            directive function is hidden.

            This value overrides
            :py:attr:`~monotable.table.MonoTable.format_func_map`
            in the MonoTable instance that generates the table.

        guideline_chars
            String of 0 to 3 characters to specify top, heading, and bottom
            guideline appearance.
            This value overrides
            :py:attr:`~monotable.table.MonoTable.guideline_chars`
            in the MonoTable instance that generates the table.

        indent
            String added to the beginning of each line in the text table.

    Returns:
        The text table as a single string.

    Raises:
        MonoTableCellError
   """
    tbl = MonoTable(indent=indent)
    tbl.format_func_map = format_func_map
    tbl.guideline_chars = guideline_chars
    if not bordered:
        return tbl.table(headings, formats, cellgrid, title)
    else:
        return tbl.bordered_table(headings, formats, cellgrid, title)


def monocol(
        column_tuples: Sequence[ColumnTuple] = (),
        title: str = '',
        *,
        bordered: bool = False,
        format_func_map: Optional[FormatFuncMap] = None,
        guideline_chars: str = '---',
        indent: str = ''
        ) -> str:
    """Generate ASCII table from column tuples.

    Args:
        column_tuples
            List of tuple of (heading string, format string,
            iterable of cell objects).

            The heading string syntax is described here
            :py:meth:`~monotable.table.MonoTable.table` under the parameter
            headings.
            The column tuple has a single heading string.

            The format directive string syntax is described here
            :ref:`Format directive string syntax
            <Format directive string syntax>`.
            The column tuple has a single format string.

            Iterable of cell objects represent the cells in the column.

        title
            ``[align_spec][wrap_spec]string``.
            Text to be aligned and printed above the text table.
            Please see :ref:`Title string syntax <Title string syntax>`.

    Keyword Args:
        bordered
            True means generate table with ASCII cell border characters.

        format_func_map
            Dictionary of format functions keyed by name.
            name, when used as a format directive in a format string,
            selects the corresponding function from the dictionary.

            If a key is one of the included format directive function
            names like 'boolean', 'mformat', etc. the included format
            directive function is hidden.

            This value overrides
            :py:attr:`~monotable.table.MonoTable.format_func_map`
            in the MonoTable instance that generates the table.

        guideline_chars
            String of 0 to 3 characters to specify top, heading, and bottom
            guideline appearance.
            This value overrides
            :py:attr:`~monotable.table.MonoTable.guideline_chars`
            in the MonoTable instance that generates the table.

        indent
            String added to the beginning of each line in the text table.

    Returns:
        The text table as a single string.

    Raises:
        MonoTableCellError
    """

    tbl = MonoTable(indent=indent)
    tbl.format_func_map = format_func_map
    tbl.guideline_chars = guideline_chars

    if not bordered:
        return tbl.cotable(column_tuples, title)
    else:
        return tbl.cobordered_table(column_tuples, title)


def join_strings(
        multi_line_strings: List[str],
        *,
        title: str = '',
        rsep: str = '    ',
        valign: int = TOP) -> str:
    """Join side-by-side multi-line strings preserving vertical alignment.

    Args:
        multi_line_strings
            List of strings.

    Keyword Args:
        title
            Text to be aligned and printed above the joined strings.
            Please see :ref:`Title string syntax <Title string syntax>`.

        rsep
            Text placed between each line of the multi-line strings
            on the right hand side.
            It is not applied to the right-most multi-line string.

        valign
            Alignment used for vertical justification of multi-line
            strings when the number of lines in the strings differ.
            Callers should use one of TOP,
            CENTER_TOP, CENTER_BOTTOM, or BOTTOM
            defined in monotable.alignment.
    """
    tbl = MonoTable()
    tbl.cell_valign = valign
    tbl.guideline_chars = ''
    formats = ['(rsep={})'.format(rsep) for _ in multi_line_strings]
    cells = (multi_line_strings,)
    return tbl.table(
        headings=(),
        formats=formats,
        cellgrid=cells,
        title=title
        )
