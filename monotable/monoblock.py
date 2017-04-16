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

"""Class MonoBlock manages and aligns a two dimensional block of text.

   Classes:
   MonoBlock   manages a two dimensional block of text.
"""

import monotable.alignment
from monotable.alignment import LEFT
from monotable.alignment import CENTER
from monotable.alignment import RIGHT
from monotable.alignment import NOT_SPECIFIED
from monotable.alignment import TOP
from monotable.alignment import BOTTOM
from monotable.alignment import CENTER_TOP
from monotable.alignment import CENTER_BOTTOM


try:
    from typing import List, Any, Optional    # noqa : F401
except(ImportError):
    pass


class MonoBlock:
    """
    Manages a two dimensional block of text.

    Methods:

        is_all_spaces()
            Tests if object contains only whitespace.

        chop_to_fieldsize()
            Truncates lines longer than fieldsize.

        hjustify()
            Horizontally justify each line into width sized field.

        vjustify()
            Vertically justify lines into height sized region.

    Methods for bordered MonoBlock:

        add_border()
            Add margins and border characters around a MonoBlock.

        remove_top_line()
            Remove the topmost line.

        remove_left_column()
            Remove 1st char of each line.

    Instance variables for user read access:

        height
            Number of text lines.

        width
            Width in chars of widest line.

        lines
            List of lines of text.
    """

    def __init__(self, text='', halign=LEFT):
        # type: (str, int) -> None
        """
        Create MonoBlock from caller's string.

        Uses str.splitlines() to separate a multi-line string into the
        individual lines.

        text
            String of text. Embedded newlines are ok.

        halign
            One of monotable.alignment module values: LEFT, CENTER,
            RIGHT, or NOT_SPECIFIED for use by hjustify().
            NOT_SPECIFIED is handled the same way as CENTER.
        """

        monotable.alignment.validate_horizontal_align(halign)
        self.lines = text.splitlines()
        if not self.lines:
            self.lines = ['']
        self._halign = halign
        # keep track if has been horizontally justified for add_border()
        self._is_hjustified = False
        self._update_height_and_width()

    def is_all_spaces(self):
        # type: () -> bool
        """Return True if MonoBlock is all spaces, False otherwise."""

        # Concatenate lines, strip spaces, test for not empty string.
        return not ''.join(self.lines).strip()

    def chop_to_fieldsize(self, fieldsize, more_marker=''):
        # type: (int, str) -> None
        """
        Truncate any lines longer than fieldsize and insert the more_marker.

        fieldsize
            Maximum width of each text line.  Must be greater than 0.

        more_marker
            String inserted to indicate text was omitted.
        """

        assert fieldsize > 0, 'nonsense to truncate to fieldsize=0 or less'
        truncated_lines = []
        if len(more_marker) > fieldsize:
            more_marker = more_marker[:fieldsize]
        for line in self.lines:
            if len(line) > fieldsize:
                # example:
                # <-------- fieldsize -------->
                # original line text that ru...  # more marker = '...' at end
                truncated_lines.append(
                    line[:fieldsize - len(more_marker)] + more_marker)
            else:
                truncated_lines.append(line)
        self.lines = truncated_lines
        self._update_height_and_width()

    def hjustify(self, width=None):
        # type: (Optional[int]) -> None
        """
        Horizontally justify each text line and pad to uniform length.

        width
            Justify each line into string of length width.
            If width is None use the instance width.
            Ignores width if width is less than the instance width.
        """

        justified_lines = []
        if width is None:
            width = self.width
        else:
            width = max(width, self.width)  # ignore width if smaller
        for line in self.lines:
            if self._halign == LEFT:
                text = line.ljust(width)
            elif self._halign == CENTER:
                text = line.center(width)
            elif self._halign == RIGHT:
                text = line.rjust(width)
            elif self._halign == NOT_SPECIFIED:
                text = line.center(width)
            else:    # pragma: no cover
                # It should be an error to get to the assert statement
                # if all the possible values of _halign have been handled.
                monotable.alignment.validate_horizontal_align(self._halign)
                assert False, 'missing branch for valid enumeration value.'

            justified_lines.append(text)
        self.lines = justified_lines
        self._update_height_and_width()
        self._is_hjustified = True        # keep track for add_border()

    def vjustify(self, valign, height, more_marker=''):
        # type: (int, int, str) -> None
        """Vertically justify lines per valign into field of height lines.

        If the MonoBlock has more lines than height, the first height
        lines are retained and valign is ignored.  If lines are omitted
        the more more_marker is placed at the end of last line.

        valign
            Alignment used for vertical justification of a multi-line
            MonoBlock.  Callers should use one of TOP,
            CENTER_TOP, CENTER_BOTTOM, or BOTTOM.

        height
            Height of field into which MonoBlock is justified.
            Must be greater than 0.

        more_marker
            String inserted to indicate text was omitted.

        """

        assert height > 0, 'nonsense if less than 1 line in result'
        monotable.alignment.validate_vertical_align(valign)
        if self.width < len(more_marker):
            more_marker = more_marker[:self.width]

        if self.height == height:
            return

        if self.height > height:  # truncate?
            # yes- truncate to height
            # right justify more_marker into the last remaining line
            # so that the line does not exceed width characters
            self.lines = self.lines[:height]
            if len(self.lines[-1]) >= self.width - len(more_marker):
                self.lines[-1] = self.lines[-1][:self.width - len(more_marker)]
            self.lines[-1] += more_marker
        else:
            # no need to truncate, so justify lines vertically in the cell
            # add whitespace pad lines above and below to fill out to height
            # lines.
            num_pad_lines = height - self.height
            quotient, remainder = divmod(num_pad_lines, 2)
            pad_text = ' ' * self.width
            pad_lines = [pad_text] * num_pad_lines
            little_pad = [pad_text] * quotient
            bigger_pad = [pad_text] * (quotient + remainder)  # bigger when odd
            if valign == TOP:
                # add empty lines at the bottom of the cell
                self.lines.extend(pad_lines)
            elif valign == BOTTOM:
                # insert empty pad lines at the top of the cell
                self.lines = pad_lines + self.lines
            elif valign == CENTER_TOP:
                self.lines.extend(bigger_pad)
                self.lines = little_pad + self.lines
            elif valign == CENTER_BOTTOM:
                self.lines.extend(little_pad)
                self.lines = bigger_pad + self.lines
            else:    # pragma: no cover
                # It should be an error to get here.  The next statement
                # should raise AssertionError.
                assert False, 'missing branch for valid enumeration value.'
        self._update_height_and_width()

    def add_border(self,
                   hmargin=1,
                   vmargin=0,
                   border_chars='--|+'):
        # type: (int, int, str) -> None
        """
        Expand MonoBlock to include ascii char borders and blank margins.

        The MonoBlock is justified to make all lines the same length before
        the border is added.

        hmargin
            Number of horizontal margin spaces between side
            border and the original text.

        vmargin
            Number of empty lines above and below the original text.

        border_chars
            Four characters used for the border:
            Top border character between the upper corners.
            Bottom border character between the lower corners.
            Either side border character below the top corner.
            Corner character.
        """

        #
        # Assure there are exactly 4 border chars.  Extend the string
        # with '+'s if it is too short.  Truncate if it is too long.
        # 1 char each for border: top, bottom, sides, corner.
        border_chars = (border_chars + '++++')[:4]
        top_char, bottom_char, side_char, corner_char = border_chars

        # Assure MonoBlock lines are all the same length.
        if not self._is_hjustified:
            self.hjustify(self.width)

        # add blank lines at top and bottom per vmargin (vertical)
        blank_line = ' ' * self.width
        blank_lines = [blank_line] * vmargin
        self.lines = blank_lines + self.lines + blank_lines

        # add horizontal margin spaces
        hspaces = ' ' * hmargin
        self.lines = [line.join((hspaces, hspaces)) for line in self.lines]

        # add one side border char to each side
        self.lines = [line.join((side_char, side_char)) for line in self.lines]

        self._update_height_and_width()

        # add top and bottom borders
        segment_width = self.width - 2         # leave room for 2 corners
        top_segment = top_char * segment_width
        # noinspection PyUnresolvedReferences
        top_border = top_segment.join((corner_char, corner_char))

        bottom_segment = bottom_char * segment_width
        # noinspection PyUnresolvedReferences
        bottom_border = bottom_segment.join((corner_char, corner_char))

        self.lines = [top_border] + self.lines + [bottom_border]
        self._update_height_and_width()

    def remove_top_line(self):
        # type: () -> None
        """Remove top line of MonoBlock. Used for stacking bordered blocks.

        If the MonoBlock only has 1 line it is shortened to the empty string.
        """

        if self.height > 1:
            self.lines = self.lines[1:]
        else:
            self.lines = ['']
        self._update_height_and_width()

    def remove_left_column(self):
        # type: () -> None
        """
        Remove left column of MonoBlock. Used to join adjacent bordered blocks.
        """

        if self.width > 0:
            self.lines = [line[1:] for line in self.lines]
            self._update_height_and_width()

    def _update_height_and_width(self):
        # type: () -> None
        self.height = len(self.lines)
        line_widths = [len(line) for line in self.lines]
        for width in line_widths:
            assert width >= 0, 'len_func must return value >= 0.'
        self.width = max(line_widths)

    def __str__(self):
        # type: () -> str
        return '\n'.join(self.lines)
