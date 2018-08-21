# monotable ASCII table formatter.
#
# Copyright 2018 Mark Taylor
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

VR_COL = ('', '(sep=|  )', ())
"""Vertical rule column for use as a column_tuple with monocol().

Note that there will be 2 spaces before and 2 spaces after '|'.
"""


def mono(headings=(),       # type: Iterable[str]
        formats=(),         # type: Iterable[str]
        cellgrid=((),),     # type: Iterable[Iterable[object]]
        title='',           # type: str
        guidelines='---',   # type: str
        floatspec='.6f',  # type: str
        bordered=False    # type: boolean
        ):
    # type: (...) -> str
    """Generate ASCII table from cellgrid.

    Args:
        headings (Iterable[str]):
            Iterable of strings for each column heading.

        formats (Iterable[str]):
            Iterable of format strings of the form
            ``[align_spec][option_spec][format_spec]``.
            Please see :ref:`Format directive string syntax <Format directive string syntax>`.

        cellgrid (Iterable[Iterable[object]]):
            representing table cells.

        title (str): ``[align_spec][wrap_spec]string``.
            Text to be aligned and printed above the text table.
            Please see :ref:`Title string syntax <Title string syntax>`.

        guidelines (str):
            String of 0 to 3 characters to specify top, heading, and bottom
            guideline appearance.
            Meaning is described by
            :py:attr:`~monotable.table.MonoTable.guideline_chars`

        floatspec (str):
            Default format specification for float type.
            Meaning is described by
            :py:attr:`~monotable.table.MonoTable.default_float_format_spec`

        bordered (boolean):
            True means generate table with ASCII cell border characters.
   """
    tbl = MonoTable()
    tbl.guideline_chars = guidelines
    tbl.default_float_format_spec = floatspec
    if not bordered:
        return tbl.table(headings, formats, cellgrid, title)
    else:
        return tbl.bordered_table(headings, formats, cellgrid, title)


def monocol(column_tuples=(),  # type: Sequence[Tuple[str, str, Sequence[object]]]    # noqa : E501
        title='',           # type: str
        guidelines='---',   # type: str
        floatspec='.6f',  # type: str
        bordered=False    # type: boolean
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
            :ref:`Format directive string syntax <Format directive string syntax>`.
            The column tuple has a single format string.

            Iterable of cell objects represent the cells in the column.


        title (str): ``[align_spec][wrap_spec]string``.
            Text to be aligned and printed above the text table.
            Please see :ref:`Title string syntax <Title string syntax>`.

        guidelines (str):
            String of 0 to 3 characters to specify top, heading, and bottom
            guideline appearance.
            Meaning is described by
            :py:attr:`~monotable.table.MonoTable.guideline_chars`

        floatspec (str):
            Default format specification for float type.
            Meaning is described by
            :py:attr:`~monotable.table.MonoTable.default_float_format_spec`

        bordered (boolean):
            True means generate table with ASCII cell border characters.

    """
    tbl = MonoTable()
    tbl.guideline_chars = guidelines
    tbl.default_float_format_spec = floatspec
    if not bordered:
        return tbl.cotable(column_tuples, title)
    else:
        return tbl.cobordered_table(column_tuples, title)

