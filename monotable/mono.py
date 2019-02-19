# monotable ASCII table formatter.
#
# Copyright 2019 Mark Taylor
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

from .table import HR
from .table import MonoTable


HR_ROW = (HR,)
"""Row containing a horizontal rule to use as a row in cellgrid."""

VR_COL = ('', '(lsep= |;rsep= )', ())
"""Vertical rule column for use as a column_tuple with monocol()."""


def mono(
        headings=(),        # type: Iterable[str]
        formats=(),         # type: Iterable[str]
        cellgrid=((),),     # type: Iterable[Iterable[object]]
        title='',           # type: str
        **kargs
        ):
    # type: (...) -> str
    """Generate ASCII table from cellgrid.

    Args:
        headings (Iterable[str]):
            Iterable of strings for each column heading.

        formats (Iterable[str]):
            Iterable of format strings of the form
            ``[align_spec][option_spec][format_spec]``.
            Please see :ref:`Format directive string syntax
            <Format directive string syntax>`.

        cellgrid (Iterable[Iterable[object]]):
            representing table cells.

        title (str): ``[align_spec][wrap_spec]string``.
            Text to be aligned and printed above the text table.
            Please see :ref:`Title string syntax <Title string syntax>`.

    Keyword Args:
        bordered (bool):
            True means generate table with ASCII cell border characters.

        format_func_map (Dict[str, Callable[[object, str], str]])
            Dictionary of format functions keyed by name.
            name, when used as a format directive in a format string,
            selects the corresponding function from the dictionary.
            If a key is one of the included format directive function
            names like 'boolean', 'mformat', etc. the included format
            directive function is hidden.
            This value overrides
            :py:attr:`~monotable.table.MonoTable.format_func_map`
            in the MonoTable instance that generates the table.

        guideline_chars (str):
            String of 0 to 3 characters to specify top, heading, and bottom
            guideline appearance.
            This value overrides
            :py:attr:`~monotable.table.MonoTable.guideline_chars`
            in the MonoTable instance that generates the table.

        indent (str):
            String added to the beginning of each line in the text table.
   """

    indent = kargs.pop('indent', '')
    tbl = MonoTable(indent=indent)
    tbl.guideline_chars = kargs.pop(
        'guideline_chars', '---')
    bordered = kargs.pop('bordered', False)
    tbl.format_func_map = kargs.pop(
        'format_func_map', None)

    if kargs:
        raise TypeError('unexpected keywords: %s' % kargs)

    if not bordered:
        return tbl.table(headings, formats, cellgrid, title)
    else:
        return tbl.bordered_table(headings, formats, cellgrid, title)


def monocol(
        column_tuples=(),   # type: Sequence[Tuple[str, str, Sequence[object]]]    # noqa : E501
        title='',           # type: str
        **kargs
        ):
    # type: (...) -> str
    """Generate ASCII table from column tuples.

    Args:
        column_tuples (List[Tuple[str, str, List[object]]]):
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

        title (str): ``[align_spec][wrap_spec]string``.
            Text to be aligned and printed above the text table.
            Please see :ref:`Title string syntax <Title string syntax>`.

    Keyword Args:
        bordered (bool):
            True means generate table with ASCII cell border characters.

        format_func_map (Dict[str, Callable[[object, str], str]])
            Dictionary of format functions keyed by name.
            name, when used as a format directive in a format string,
            selects the corresponding function from the dictionary.
            If a key is one of the included format directive function
            names like 'boolean', 'mformat', etc. the included format
            directive function is hidden.
            This value overrides
            :py:attr:`~monotable.table.MonoTable.format_func_map`
            in the MonoTable instance that generates the table.

        guideline_chars (str):
            String of 0 to 3 characters to specify top, heading, and bottom
            guideline appearance.
            This value overrides
            :py:attr:`~monotable.table.MonoTable.guideline_chars`
            in the MonoTable instance that generates the table.

        indent (str):
            String added to the beginning of each line in the text table.
    """

    indent = kargs.pop('indent', '')
    tbl = MonoTable(indent=indent)
    tbl.guideline_chars = kargs.pop(
        'guideline_chars', '---')
    bordered = kargs.pop('bordered', False)
    tbl.format_func_map = kargs.pop(
        'format_func_map', None)

    if kargs:
        raise TypeError('unexpected keywords: %s' % kargs)

    if not bordered:
        return tbl.cotable(column_tuples, title)
    else:
        return tbl.cobordered_table(column_tuples, title)
