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

"""Responsible for scanning callers format string.

   Classes:
   MonoTableConfig Copy of selected MonoTable instance and class variables.
   FormatScanner   Format Python objects to ASCII table for monospaced font.
"""

import collections
import fnmatch

import monotable.plugin
import monotable.alignment

# These imports are for PEP484, PYPI package mypy static type checking.
try:
    from typing import List, Tuple, Optional, Any    # noqa : F401
except(ImportError):
    pass

MonoTableConfig = collections.namedtuple('MonoTableConfig',
                                         ['align_spec_chars',
                                          'sep',
                                          'format_func',
                                          'format_func_map',
                                          'option_spec_delimiters'
                                          ]
                                         )
"""Copy of selected MonoTable instance and class variables."""


class FormatScanner:
    """Scans a format string for align, format_spec, and options.

    The format string takes the form [align_spec][option_spec][format_spec].
    See formats description in MonoTable.__init().

    The following format functions are selectable using an option_spec
    in addition to any supplied by format_func_map.

        option name     function
        --------------------------
        'boolean'        boolean
        'thousands'      thousands
        'millions'       millions
        'billions'       billions
        'trillions'      trillions
        'milli'          milli
        'micro'          micro
        'nano'           nano
        'pico'           pico
        'kibi'           kibi
        'mebi'           mebi
        'gibi'           gibi
        'tebi'           tebi
        'mformat'        mformat
        'pformat'        pformat
        'sformat'        sformat
        'tformat'        tformat

    An example usage:

    >>> import monotable
    >>> def my_format_func(value, format_spec):
    ...    pass

    >>> align_spec = '<'
    >>> option_spec = '(width=17;wrap;sep= | ;my_format)'
    >>> format_spec = '.0f'
    >>> format_str = align_spec + option_spec + format_spec
    >>> config = monotable.scanner.MonoTableConfig(
    ...         align_spec_chars='<^>',
    ...         sep='  ',
    ...         format_func=format,            # <built-in function format>
    ...         format_func_map= {'my_format': my_format_func},
    ...         option_spec_delimiters='(;)')

    >>> formatobj = monotable.scanner.FormatScanner(format_str, config)

    # formatobj has these attributes:
    >>> assert formatobj.error_text == ''      # indicates no scanning errors

    # enumeration value for '<'
    >>> assert formatobj.align == monotable.alignment.LEFT

    # overrides config.format_func
    >>> assert formatobj.format_func == my_format_func
    >>> assert formatobj.format_spec == '.0f'
    >>> assert formatobj.width == 17
    >>> assert formatobj.fixed is False
    >>> assert formatobj.wrap is True
    >>> assert formatobj.sep == ' | '          # overrides config.sep

    Instance variables for user read access:

        error_text
            Describes what was wrong with option_format_spec.
            Empty sting indicates a good option_format_spec.

        align
            Value scanned from [align_spec].  It is one of _LEFT,
            _CENTER, _RIGHT, or _NOT_SPECIFIED.

        format_func
            Function with signature of <built-in function format>.
            Reference to a format function associated with a
            scanned option-name or a default value.

        format_spec
            format_spec part of format_str.

        width
            Specifies the maximum number of horizontal columns of the
            formatted text.

        fixed
            When True, indicates the formatted text is exactly width columns.

        wrap
            When True, indicates the formatted text is text wrapped.

        sep
            Specifies separator string to be placed after the formatted
            text.

    """

    def __init__(self, format_str, config):
        # type: (str, MonoTableConfig) -> None
        """
        Scan the string per delimiters, return results as instance vars.

        format_str
            String: [align_spec][option_spec][format_spec]
            See formats description in MonoTable.__init__().

        config
            Instance of MonoTableConfig that contains copies of a subset
            of MonoTable instance and class variables.  See MonoTable
            doc string for detailed descriptions.
                align_spec_chars
                sep
                format_func
                format_func_map
                option_spec_delimiters
        """

        # A design choice was made to keep all the format string
        # and format option handling in a separate class.  This was done
        # to reduce the size of MonoTable class.  The downside is that
        # the functions in this class need several MonoTable class and
        # instance variables.  A copy of these variables are passed
        # here by parameter 'config' of type MonoTableConfig.
        # The design choice not taken was to move the
        # FormatScanner member functions into MonoTable.

        # renames to shorten long lines
        align_spec_chars = config.align_spec_chars
        option_spec_delimiters = config.option_spec_delimiters

        # Verify that the start delimiter of option_spec_delimiters cannot
        # be mis-interpreted as one of the align_spec_chars.
        # Do test here after instance is created to allow overriding the
        # class variables on an instance.  For example:
        #   mt = MonoTable()
        #   mt.align_spec_chars = 'lcr'
        if align_spec_chars and option_spec_delimiters:
            t = option_spec_delimiters[0]
            assert t not in align_spec_chars, 'ambiguous'

        if option_spec_delimiters:
            d = option_spec_delimiters
            assert len(d) == 3, 'one for start, between, end'

            # start char and end char can be the same.
            # between char must be unique.
            assert d[0] != d[1], 'between char different than start char'
            assert d[1] != d[2], 'between char different than end char'

        # Combine hard coded format function options with user supplied
        # format functions.  Note that a user name will hide a hard coded
        # name.                 option name  function
        self._format_functions = {'boolean': monotable.plugin.boolean,
                                  'thousands': monotable.plugin.thousands,
                                  'millions': monotable.plugin.millions,
                                  'billions': monotable.plugin.billions,
                                  'trillions': monotable.plugin.trillions,
                                  'milli': monotable.plugin.milli,
                                  'micro': monotable.plugin.micro,
                                  'nano': monotable.plugin.nano,
                                  'pico': monotable.plugin.pico,
                                  'kibi': monotable.plugin.kibi,
                                  'mebi': monotable.plugin.mebi,
                                  'gibi': monotable.plugin.gibi,
                                  'tebi': monotable.plugin.tebi,
                                  'mformat': monotable.plugin.mformat,
                                  'pformat': monotable.plugin.pformat,
                                  'sformat': monotable.plugin.sformat,
                                  'tformat': monotable.plugin.tformat
                                  }
        if config.format_func_map is not None:
            self._format_functions.update(config.format_func_map)

        self.error_text = ''
        self.width = None    # type: Optional[int]
        self.fixed = False
        self.wrap = False
        self.sep = config.sep
        self.format_func = config.format_func
        self.align, option_format_spec = monotable.alignment.split_up(
            format_str, align_spec_chars)
        if not option_spec_delimiters:
            # no delimiters disables option_spec scanning
            self.format_spec = option_format_spec    # type: str
            return

        self._start, self._between, self._end = option_spec_delimiters
        option_spec, self.format_spec = (
            self._parse(option_format_spec))    # type: Tuple[str, str]
        self._scan(option_spec)

    def _parse(self, option_format_spec):
        # type: (str) -> Tuple[str, str]
        """Split option_format_spec into option_spec and format_spec.

        option_format_spec
            [option_spec][format_spec]
            option_spec == (*)  where * is 0 or more characters
            See option_spec description in MonoTable.__init__().

        Returns a tuple consisting of:
            The option_spec including the enclosing delimiters or empty string.
            The rest of the string after closing delimiter or entire string.
        """

        startswith_match = self._start + '*' + self._end + '*'
        if fnmatch.fnmatchcase(option_format_spec, startswith_match):
            # look for self._end starting char after self._start
            option_spec_end = option_format_spec.find(self._end, 1)
            option_spec = option_format_spec[:option_spec_end + 1]
            format_spec = option_format_spec[option_spec_end + 1:]
            return option_spec, format_spec
        return '', option_format_spec

    def _scan(self, option_spec):
        # type: (str) -> None
        """Scan option_spec string for options and values.

        Updates instance variables align, error_text, format_func,
        format_spec, width, fixed, wrap, and sep per scan results.

        option_spec
            (*)  where * is one or more option names separated by ;.
            See option_spec description in MonoTable.__init__().
        """

        if not option_spec:
            return

        # assumes option_spec starts and ends with correct delimiters
        option_spec_copy_for_error_text = option_spec[:]
        option_spec = option_spec[1:-1]  # drop start and end delimiters
        if not option_spec:  # anything left to scan?
            return

        option_list = option_spec.split(self._between)    # type: List[str]

        # scan for each option, process, and remove from option_list
        self._scan_width(option_list)
        self._scan_fixed(option_list)
        self._scan_wrap(option_list)
        self._scan_sep(option_list)
        self._scan_format_func(option_list)

        # silently ignore fixed or wrap options if no width=N option
        if self.width is None:
            self.wrap = False
            self.fixed = False

        if len(option_list) > 0:
            # All the allowed option expressions have been removed from
            # option_list.  So option_list contains only invalid values or
            # duplicates.  Duplicates can be the same option or more than
            # one format function name.  Show them in the error message.
            error_messages = ['In option_spec "{}"'.format(
                option_spec_copy_for_error_text)]
            for opt in option_list:
                message = ('    unrecognized option "{}",'
                           ' bad/duplicate name or bad "=value".').format(opt)
                error_messages.append(message)
            error_messages.extend(self._allowed_options())
            self.error_text = '\n'.join(error_messages)

    def _scan_width(self, option_list):
        # type: (List[str]) -> None
        """Scan option_list for width option and arg, remove if found."""
        for option in option_list:
            name, arg = self._option_and_arg(option)
            if name == 'width':
                value = self._scan_gt_value(arg)
                if value is not None:
                    self.width = value
                    option_list.remove(option)
                    break

    def _scan_fixed(self, option_list):
        # type: (List[str]) -> None
        """Scan option_list for fixed option, remove if found."""
        for option in option_list:
            name, arg = self._option_and_arg(option)
            if name == 'fixed':
                if arg is None:
                    self.fixed = True
                    option_list.remove(option)
                    break

    def _scan_wrap(self, option_list):
        # type: (List[str]) -> None
        """Scan option_list for wrap option, remove if found."""
        for option in option_list:
            name, arg = self._option_and_arg(option)
            if name == 'wrap':
                if arg is None:
                    self.wrap = True
                    option_list.remove(option)
                    break

    def _scan_sep(self, option_list):
        # type: (List[str]) -> None
        """Scan option_list for sep option and arg, remove if found."""
        for option in option_list:
            name, arg = self._option_and_arg(option)
            if name == 'sep':
                # Keep rest after '='.  OK if empty string after '='.
                if arg is not None:
                    self.sep = arg
                    option_list.remove(option)
                    break

    def _scan_format_func(self, option_list):
        # type: (List[str]) -> None
        """Scan option_list for a format function, remove if found."""
        for option in option_list:
            name, arg = self._option_and_arg(option)
            if name is not None and name in self._format_functions:
                if arg is None:
                    self.format_func = self._format_functions[name]
                    option_list.remove(option)
                break

    @staticmethod
    def _option_and_arg(option):
        # type: (str) -> Tuple[Optional[str], Optional[str]]
        """Split up a format option to an option name and arg."""
        split_option = option.split('=')
        if len(split_option) == 1:
            return split_option[0].strip(), None
        elif len(split_option) == 2:
            return split_option[0].strip(), split_option[1]
        else:
            return None, None

    @staticmethod
    def _scan_gt_value(text):
        # type: (Optional[str]) -> Optional[int]
        """
        Scan text for integer value N. Returns N if an int > 0, else None.

        text can be None. If so return None.
        """
        if text is None:
            return None
        try:
            int_value = int(text)
        except ValueError:
            return None
        if int_value < 1:
            return None
        else:
            return int_value

    def _allowed_format_functions(self):
        # type: () -> List[str]
        lines = []
        fmt = '  {} - {}.'
        for name in sorted(self._format_functions):
            lines.append(fmt.format(name, self._format_functions[name]))
        return lines

    def _allowed_options(self):    # type: () -> List[str]
        lines = ['Options are enclosed by "{}" and "{}".  '
                 'Options are separated by "{}".'.format(self._start,
                                                         self._end,
                                                         self._between),
                 'For example: "{}width=22{}sep=   {}"'.format(
                     self._start, self._between, self._end),
                 'Case is significant.  Whitespace is not significant except',
                 'after the "=" in "sep =".  Allowed options are:',
                 '  width=N - column width is at most N columns. N > 0.',
                 '  fixed   - column width is exactly width=N columns.',
                 '            Use to qualify width=N option.',
                 '  wrap    - wrap/re-wrap to width=N.',
                 '            Use to qualify width=N option.',
                 '  sep=ccc - characters after sep= are the column separator.',
                 ]
        lines.extend(self._allowed_format_functions())
        return lines
