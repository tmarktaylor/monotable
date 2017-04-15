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

"""Text alignment constants and validation routines.

   Functions:
   validate_horizontal_align
   validate_vertical_align
   split_up

   Attributes:
   NOT_SPECIFIED  Horizontal text justification is not specified.
   LEFT           Left text justification.
   CENTER         Center text horizontal justification.
   RIGHT          Right text justification.
   TOP            Align vertically to top.
   CENTER_TOP     Align vertically to center biased upwards.
   CENTER_BOTTOM  Align vertically to center biased downwards.
   BOTTOM         Align vertically to bottom.
"""

# These imports are for PEP484, PYPI package mypy static type checking.
try:
    from typing import Tuple    # noqa : F401
except(ImportError):
    pass

# repository: https://github.com/tmarktaylor/monotable

NOT_SPECIFIED = 0  # must be zero
"""Horizontal text justification is not specified."""

LEFT = 1
"""Left text justification."""

CENTER = 2
"""Center text horizontal justification."""

RIGHT = 3
"""Right text justification."""

_HALIGN_ALLOWED = [NOT_SPECIFIED, LEFT, CENTER, RIGHT]
_HALIGN_HELP = '\n'.join([
    'Expected a horizontal align value, got: "{0}".',
    'Allowed values are: _NOT_SPECIFIED, _LEFT, _CENTER, _RIGHT'])


def validate_horizontal_align(value):
    # type: (int) -> None
    """Check if value is a valid enumeration value."""

    assert value in _HALIGN_ALLOWED, _HALIGN_HELP.format(value)


# specify vertical text justification
TOP = 10
"""Shift the text lines towards the top, add blank lines at the bottom."""

CENTER_TOP = 11
"""Shift the text lines towards the top when odd number extra blank lines."""

CENTER_BOTTOM = 12
"""Shift the text lines towards bottom when odd number extra blank lines."""

BOTTOM = 13
"""Shift the text lines towards the bottom, add blank lines at the top."""

_VALIGN_ALLOWED = [TOP, CENTER_TOP, CENTER_BOTTOM, BOTTOM]
_VALIGN_HELP = '\n'.join([
    'Expected a vertical align value, got: "{0}".',
    'Allowed values are: TOP, CENTER_TOP, CENTER_BOTTOM, BOTTOM'])


def validate_vertical_align(value):
    # type: (int) -> None
    """Check if value is a valid enumeration value."""

    assert value in _VALIGN_ALLOWED, _VALIGN_HELP.format(value)


def split_up(prefixed_string, align_spec_chars):
    # type: (str, str) -> Tuple[int, str]
    """Split up string that starts with an optional one char align_spec.

    prefixed_string
        String that starts with an optional one char align_spec.

    align_spec_chars
        Three characters to indicate string left, center, and
        right justification.

    Returns tuple:
        Enumeration value of the align_spec.
        The rest of the prefixed_string after removing align_spec char.
    """

    # skip doing split up if either param is an empty string
    if align_spec_chars and prefixed_string:
        # 1. The asserts and align_map need only be calculated once per
        #    table() or bordered_table() rather than multiple times.
        #    [once per title, each heading, and each format]
        #    The checks are done here as a trade off favoring simpler
        #    logic over minimal reduction in execution time.
        # 2. Creating align_map below dynamically allows modifying the class
        #    attribute align_spec_chars on an instance.
        assert len(align_spec_chars) == 3, 'left, center, right'
        assert len(set(align_spec_chars)) == 3, 'must be unique'
        align_map = dict(zip(align_spec_chars, (LEFT, CENTER, RIGHT)))
        align = align_map.get(prefixed_string[0], NOT_SPECIFIED)
        if align:
            prefixed_string = prefixed_string[1:]  # drop align_spec char
    else:
        align = NOT_SPECIFIED
    return align, prefixed_string
