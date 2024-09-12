# Copyright 2020, 2024 Mark Taylor
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
"""Table cell formatting exception class."""

from typing import Optional


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
        # type: (int, int, str, Optional[str]) -> None

        self.row = row
        self.column = column
        self.format_spec = format_spec
        self.trace_text = trace_text
        self.name = 'MonoTableCellError'

    def __str__(self):
        # type: () -> str
        """Show cell's position, format_spec, and trace info."""

        fmt = '{}: cell[{:d}][{:d}], format_spec= {}'
        exception_msg = fmt.format(
            self.name,
            self.row,
            self.column,
            self.format_spec)
        return exception_msg
