"""Assertion based test cases for monotable.scanner.FormatScanner."""
import pytest

import monotable.alignment
import monotable.plugin
import monotable.scanner
import monotable.table

TOP = monotable.alignment.TOP
CENTER_TOP = monotable.alignment.CENTER_TOP
CENTER_BOTTOM = monotable.alignment.CENTER_BOTTOM
BOTTOM = monotable.alignment.BOTTOM

LEFT = monotable.alignment.LEFT
CENTER = monotable.alignment.CENTER
RIGHT = monotable.alignment.RIGHT

# Tuple of MonoTable attributes used to initialize FormatScanner.
MONOTABLE_CONFIG = monotable.scanner.MonoTableConfig(
    align_spec_chars='<^>',
    sep='  ',
    format_func=format,
    format_func_map=None,
    option_spec_delimiters='(;)')

DEFAULT_FORMAT_FUNCTIONS = [
    '  boolean - <function boolean',
    '  thousands - <function thousands',
    '  millions - <function millions',
    '  billions - <function billions',
    '  trillions - <function trillions',
    '  milli - <function milli',
    '  micro - <function micro',
    '  nano - <function nano',
    '  pico - <function pico',
    '  kibi - <function kibi',
    '  mebi - <function mebi',
    '  gibi - <function gibi',
    '  tebi - <function tebi',
    '  pformat - <function pformat',
    '  sformat - <function sformat',
    '  mformat - <function mformat',
    '  tformat - <function tformat',
]
"""Format functions that can be selected in an option_spec. (def order)."""

@pytest.fixture()
def format_scanner():
    """Create a monotable.scanner.FormatScanner instance."""

    return monotable.scanner.FormatScanner('', MONOTABLE_CONFIG)

#
# Tests for FormatScanner._scan_gt_value().
#


def test_scan_gt_value_none(format_scanner):
    assert format_scanner._scan_gt_value(None) is None


def test_scan_gt_value_empty_string(format_scanner):
    assert format_scanner._scan_gt_value('') is None


def test_scan_gt_value_zero(format_scanner):
    assert format_scanner._scan_gt_value(' 0 ') is None


def test_scan_gt_value_negative(format_scanner):
    assert format_scanner._scan_gt_value(' -1') is None


def test_scan_gt_value_one(format_scanner):
    assert format_scanner._scan_gt_value('  1  ') == 1

#
# Tests for FormatScanner._allowed_format_functions().
#

def test_allowed_format_functions_no_user_defined(format_scanner):
    """Checks for match of just the beginning of each string."""

    expected_format_functions = sorted(DEFAULT_FORMAT_FUNCTIONS)
    lines = format_scanner._allowed_format_functions()
    for expected, actual in zip(expected_format_functions, lines):
        assert actual.startswith(expected)


def test_allowed_format_functions_user_format_functions():
    """Checks for match of just the beginning of each string.."""

    expected_user_defined_format_functions = [
        '  myformat - <function ',
        '  mysecondformat - <function ',
    ]
    expected_format_functions = sorted(DEFAULT_FORMAT_FUNCTIONS +
                                       expected_user_defined_format_functions)
    def myformat(value, format_spec):
        _, _ = value, format_spec
        pass

    def mysecondformat(value, format_spec):
        _, _ = value, format_spec
        pass

    myconfig = MONOTABLE_CONFIG._replace(format_func_map={
        'myformat': myformat,
        'mysecondformat': mysecondformat})
    fs = monotable.scanner.FormatScanner('', myconfig)
    lines = fs._allowed_format_functions()
    for expected, actual in zip(expected_format_functions, lines):
        assert actual.startswith(expected)

    # call to prevent coverage.py missing stmnt
    myformat(None, None)
    mysecondformat(None, None)


def test_allowed_format_functions_user_hides_default_format_function():
    """Checks for match of just the beginning of each string.

    Verify that a user defined format function doesn't break the
    list of expected format functions returned by _allowed_format_functions().
    """

    # note- The user defined format
    expected_user_defined_format_functions = [
        '  myformat - <function ',
    ]
    x1 = (DEFAULT_FORMAT_FUNCTIONS +
          expected_user_defined_format_functions)
    x1.remove('  sformat - <function sformat')
    x1.append('  sformat - <function ')    # py2/3 differ beyond this point
    expected_format_functions = sorted(x1)

    def myformat(value, format_spec):
        _, _ = value, format_spec
        pass

    def sformat(value, format_spec):
        _, _ = value, format_spec
        pass

    myconfig = MONOTABLE_CONFIG._replace(format_func_map={
        'myformat': myformat,
        'sformat': sformat})

    fs = monotable.scanner.FormatScanner('', myconfig)
    lines = fs._allowed_format_functions()
    for expected, actual in zip(expected_format_functions,
                                lines):
        assert actual.startswith(expected)

    # call to prevent coverage.py missing stmnt
    myformat(None, None)
    sformat(None, None)

#
# Tests for FormatScanner._allowed_options().
#


def test_allowed_options(format_scanner):
    first_part_expected_options = '\n'.join([
        'Directives are enclosed by "(" and ")", and are separated by ";".',
        'For example: "(width=22;sep=   )"',
        'Case is significant.  Whitespace is not significant except',
        'after the "=" in "sep =".  Allowed options are:',
        '  width=N - column width is at most N columns. N > 0.',
        '  fixed   - column width is exactly width=N columns.',
        '            Use to qualify width=N option.',
        '  wrap    - wrap/re-wrap to width=N.',
        '            Use to qualify width=N option.',
        '  lsep=ccc - characters after lsep= go to left of column.',
        '  rsep=ccc - characters after rsep= go to right of column.',
        '  none=ccc - None formats as the characters after none=.',
        '  zero=ccc - if all digits are zero replace with ccc.',
        '  parentheses if minus sign, enclose in parentheses.',
        ''
    ])

    # The test checks for match of just the beginning of each string.
    expected_format_functions = sorted(DEFAULT_FORMAT_FUNCTIONS)
    num_expected_format_functions = len(expected_format_functions)
    lines = format_scanner._allowed_options()
    lines_up_to_functions = lines[:-num_expected_format_functions]
    last_lines = lines[-num_expected_format_functions:]

    expected_options_lines = first_part_expected_options.splitlines()
    assert expected_options_lines == lines_up_to_functions

    for expected, actual in zip(expected_format_functions,
                                last_lines):
        assert actual.startswith(expected)

#
# Tests for FormatScanner._parse().
#


def test_parse_typical_options_spec_words(format_scanner):
    (option_spec,
        format_spec) = format_scanner._parse('(options)format_spec')
    assert option_spec == '(options)'
    assert format_spec == 'format_spec'


def test_parse_empty_spec(format_scanner):
    option_spec, format_spec = format_scanner._parse('')
    assert option_spec == ''
    assert format_spec == ''


def test_parse_open_paren(format_scanner):
    option_spec, format_spec = format_scanner._parse('(')
    assert option_spec == ''
    assert format_spec == '('


def test_parse_close_paren(format_scanner):
    option_spec, format_spec = format_scanner._parse(')')
    assert option_spec == ''
    assert format_spec == ')'


def test_parse_empty_option_spec(format_scanner):
    option_spec, format_spec = format_scanner._parse('()')
    assert option_spec == '()'
    assert format_spec == ''


def test_parse_empty_option_spec_one_char_format_spec(format_scanner):
    option_spec, format_spec = format_scanner._parse('()f')
    assert option_spec == '()'
    assert format_spec == 'f'


def test_parse_1_char_option_spec(format_scanner):
    option_spec, format_spec = format_scanner._parse('(p)')
    assert option_spec == '(p)'
    assert format_spec == ''


def test_parse_multi_start_end_char_pairs(format_scanner):
    option_spec, format_spec = format_scanner._parse('(p)f(f)')
    assert option_spec == '(p)'
    assert format_spec == 'f(f)'


def test_parse_nested_start_end_char_pairs(format_scanner):
    option_spec, format_spec = format_scanner._parse('(())f')
    assert option_spec == '(()'
    assert format_spec == ')f'

#
# Tests for FormatScanner.__init__().
#


def test_init_parse_all_good_options():
    """Prove a complex valid format_str produces expected attributes."""

    format_str = '(width=22;wrap;sep= | ;none=...;pformat){:2.7d}'
    fs = monotable.scanner.FormatScanner(format_str, MONOTABLE_CONFIG)
    assert fs.error_text == ''
    assert fs.width == 22
    assert fs.wrap is True
    assert fs.sep == ' | '
    assert fs.format_func == monotable.plugin.pformat

    assert fs.format_spec == '{:2.7d}'
    assert fs.align == monotable.alignment.NOT_SPECIFIED
    assert fs.fixed is False
    assert fs.zero is None
    assert fs.none == '...'
    assert fs.parentheses is False


# List of good format_str concentrating on the option_spec part
# with various options and spacing.  These are used to to show that
# parsing succeeds.
good_format_str_list = [
    '()',
    # Valid even when missing option_spec end delimiter
    '(width=22;wrap{:2.7d}',
    '(width=3;wrap;sep= | ;pformat){:2.7d}',
    '( width =3)',
    '( width= 3)',
    '( width = 3)',
    '( width  = 3 )',
    '(  width  =  3)'
    '( width = 4;wrap)',
    '(  width = 4; wrap )',
    '(width=22;fixed{:2.7d}',
    '(width=3;fixed;sep= | ;pformat){:2.7d}',
    '( width =3)',
    '( width= 3)',
    '( width = 3)',
    '( width  = 3 )',
    '(  width  =  3)'
    '( width = 4;fixed)',
    '(  width = 4; fixed )',
    '(fixed)',    # note- fixed w/o width= is silently ignored
    '(wrap)',     # note- wrap w/o width= is silently ignored
    '( fixed),'
    '(fixed '
    '(none=...)'
    'none=)',
    'none=  )',
    'none =  )',
    '(zero=--)'
    '( zero=--)'
    '( zero =--)'
    '(zero=...)'
    'zero=)',
    'zero=  )',
    '(parentheses)'
    '( parentheses)'
    '(parentheses )'
    '(sep=)',
    '( sep=)',
    '(  sep= )',
    '(lsep=)',
    '(lsep =)',
    '( lsep=)',
    '(  lsep= )',
    '(rsep=)',
    '(rsep =)',
    '( rsep=)',
    '(  rsep= )',
    '( sformat)',
    '(sformat )',
    '( pformat)',
    '(pformat )',
    '( mformat)',
    '(mformat )',
    '(tformat )',
    '( tformat)',
    '(width = 3 ; wrap ;sep= | ;   pformat){:2.7d}'

    # fixed without width=N is silently ignored
    '(fixed)',
    # wrap without width=N is silently ignored
    '(wrap)',

    '(wrap;fixed)',
    ]


@pytest.mark.parametrize("a_good_format_str", good_format_str_list)
def test_init_parse_extra_spacing(a_good_format_str):
    """A valid format_str creates empty error_text."""

    fs = monotable.scanner.FormatScanner(a_good_format_str, MONOTABLE_CONFIG)
    assert fs.error_text == ''


# List of illegal format_str concentrating on the option_spec part
# of the formatting directive with various typos.
bad_format_str_list = [
    # comma is a bad delimiter
    '(width=22;wrap,sep= | ;pformat){:2.7d}',

    # no allowed options
    '(bogus)format_str',

    # bad option name mable
    '(mable=22;wrap){:2.7d}',

    # width option has no '='
    '(width){:2.7d}',

    # width option has no value
    '(width=){:2.7d}',

    # width option has bad value 0
    '(width=0){:2.7d}',

    # width option has bad value (negative)
    '(width=-1){:2.7d}',

    # sep option has no '='
    '(sep){:2.7d}',

    # lsep option has no '='
    '(lsep){:2.7d}',

    # rsep option has no '='
    '(rsep){:2.7d}',

    # none option has no '='
    '(none){:2.7d}',

    # zero option has no '='
    '(zero){:2.7d}',

    # specify unexpected = for non format function options (directives).
    '(fixed=ccc)',
    '(wrap=ccc)',
    '(parentheses=ccc)',

    # extra '='
    '(width=4=){:2.7d}',

    # more than one width
    '(width=3;width=4){:2.7d}',

    # format function with = value
    '(mformat=2){:2.7d}',

    # the option is all '='
    '(width=3;=====){:2.7d}',

    # more than one format function
    '(tformat;sformat){:2.7d}',

    # illegal fixed arg
    '(width=10;fixed = 2)',
    '(fixed=1)',

    # illegal wrap arg
    '(wrap=A;width=10)',
    '(wrap=1)',

    # illegal parentheses arg
    '(parentheses=)',
    '(parentheses=A)',
    '(parentheses=1)',
]


@pytest.mark.parametrize("a_bad_format_str", bad_format_str_list)
def test_parse_assorted_bad_options(a_bad_format_str):
    fs = monotable.scanner.FormatScanner(a_bad_format_str, MONOTABLE_CONFIG)
    assert fs.error_text[:14] == 'In option_spec'


def make_shuffled_option_list():
    """Run off line to produce a shuffled_option_list to paste in below.

    Note: The correctness of the output depends on the correctness
    of the list options below.

    Note: The options list below does not cover all options.

    These are cmd.exe commands on Windows that will invoke this function.
    The virtual env is in a folder at the same level as monotable top level.
    You will need pytest in the virtual env.  I am using py 3.7.0.
    I just cut and paste the 8 commands into cmd.

    cd <YOUR_PATH_TO_MONOTABLE>
    set PYTHONPATH=%PYTHONPATH%;<YOUR_PATH_TO_MONOTABLE>/test
    ../venv/scripts/activate
    py
    import test_format_scanner
    test_format_scanner.make_shuffled_option_list()
    exit()
    deactivate
    """
    import random
    options = [' sep =ZZZ',
               'wrap',
               'width= 10',
               'pformat',
               'fixed',
               'zero=...',
               'parentheses'
               ]
    shuffled = []
    for _ in range(10):
        random.shuffle(options)
        directive_string = "    '" + '<(' + ';'.join(options) + ')F' + "',"
        shuffled.append(directive_string)
    print('\n'.join(shuffled))


def valid_options_shuffled_helper(fs):
    """Check a FormatScanner instance in test_valid_options_shuffled()."""
    assert fs.format_spec == 'F'
    assert fs.error_text == ''
    assert fs.align == LEFT
    assert fs.width == 10
    assert fs.fixed is True
    assert fs.wrap is True
    assert fs.sep == 'ZZZ'
    assert fs.zero == '...'
    assert fs.none is None
    assert fs.parentheses is True


# List of good format_str where the option_spec part has the same
# valid options, just in different orders.
# Maintainers Use make_shuffled_option_list() above to generate the list.
shuffled_option_list = [
    '<(width= 10;pformat;zero=...;fixed;parentheses; sep =ZZZ;wrap)F',
    '<(fixed;width= 10;wrap;zero=...;pformat;parentheses; sep =ZZZ)F',
    '<(pformat;wrap; sep =ZZZ;parentheses;fixed;width= 10;zero=...)F',
    '<(pformat;zero=...;parentheses;fixed;wrap; sep =ZZZ;width= 10)F',
    '<(parentheses;fixed; sep =ZZZ;pformat;zero=...;width= 10;wrap)F',
    '<(width= 10;parentheses;fixed; sep =ZZZ;pformat;wrap;zero=...)F',
    '<(fixed;parentheses;wrap; sep =ZZZ;pformat;width= 10;zero=...)F',
    '<( sep =ZZZ;width= 10;zero=...;wrap;pformat;parentheses;fixed)F',
    '<(parentheses;width= 10;fixed;pformat;zero=...; sep =ZZZ;wrap)F',
    '<(pformat;parentheses;wrap;width= 10;zero=...; sep =ZZZ;fixed)F',
]


@pytest.mark.parametrize("a_shuffled_option_format_str",
                         shuffled_option_list)
def test_valid_options_shuffled(a_shuffled_option_format_str):
    """Test different orderings of all the possible format options.

    There are 4 possibilities for the format function option:
    pformat, sformat, tformat, and a user defined format function.
    The parameter a_shuffled_option_format_str includes pformat.
    """

    # Test with pformat.
    fs = monotable.scanner.FormatScanner(a_shuffled_option_format_str,
                                         MONOTABLE_CONFIG)
    valid_options_shuffled_helper(fs)
    assert fs.format_func == monotable.plugin.pformat

    # Test with sformat by replacing pformat in the format_str.
    format_str = a_shuffled_option_format_str.replace('pformat', 'sformat')
    fs = monotable.scanner.FormatScanner(format_str, MONOTABLE_CONFIG)
    valid_options_shuffled_helper(fs)
    assert fs.format_func == monotable.plugin.sformat

    # Test with tformat by replacing pformat in the format_str.
    format_str = a_shuffled_option_format_str.replace('pformat', 'tformat')
    fs = monotable.scanner.FormatScanner(format_str, MONOTABLE_CONFIG)
    valid_options_shuffled_helper(fs)
    assert fs.format_func == monotable.plugin.tformat

    # Test with a user defined format function by configuring the
    # FormatScanner with a user defined format function and
    # by replacing pformat in the format_str.

    # User defined format function.
    def user_format_func(value, format_spec):
        _, _ = value, format_spec
        pass

    # Associate name 'user_format_func' with the function object
    # and update format_func_map passed via named tuple config.
    format_func_map = {'user_format_func': user_format_func}
    new_config = MONOTABLE_CONFIG._replace(format_func_map=format_func_map)

    format_str = a_shuffled_option_format_str.replace('pformat',
                                                      'user_format_func')
    fs = monotable.scanner.FormatScanner(format_str, new_config)
    valid_options_shuffled_helper(fs)
    assert fs.format_func == user_format_func

    # call to prevent coverage.py missing stmnt
    user_format_func(None, None)


def test_empty_sep():
    """Test scanning valid sep= with no text."""

    fs = monotable.scanner.FormatScanner('(sep=)F', MONOTABLE_CONFIG)
    assert fs.error_text == ''
    assert fs.sep == ''


def test_sep_is_spaces():
    """Test scanning sep=<spaces>."""

    fs = monotable.scanner.FormatScanner('(sep=     )F', MONOTABLE_CONFIG)
    assert fs.error_text == ''
    assert fs.format_spec == 'F'
    assert fs.align == monotable.alignment.NOT_SPECIFIED
    assert fs.width is None
    assert fs.fixed is False
    assert fs.wrap is False
    assert fs.sep == '     '
    assert fs.none is None
    assert fs.zero is None
    assert fs.parentheses is False


def test_zero():
    fs = monotable.scanner.FormatScanner('(zero=+++)F', MONOTABLE_CONFIG)
    assert fs.error_text == ''
    assert fs.format_spec == 'F'
    assert fs.align == monotable.alignment.NOT_SPECIFIED
    assert fs.width is None
    assert fs.fixed is False
    assert fs.wrap is False
    assert fs.sep == MONOTABLE_CONFIG.sep
    assert fs.none is None
    assert fs.zero == '+++'
    assert fs.parentheses is False


def test_empty_zero():
    """Test scanning valid sep= with no text."""

    fs = monotable.scanner.FormatScanner('(zero=)F', MONOTABLE_CONFIG)
    assert fs.error_text == ''
    assert fs.format_spec == 'F'
    assert fs.align == monotable.alignment.NOT_SPECIFIED
    assert fs.width is None
    assert fs.fixed is False
    assert fs.wrap is False
    assert fs.sep == MONOTABLE_CONFIG.sep
    assert fs.none is None
    assert fs.zero == ''
    assert fs.parentheses is False


def test_zero_is_spaces():
    """Test scanning valid sep= with no text."""

    fs = monotable.scanner.FormatScanner('(zero=    )F', MONOTABLE_CONFIG)
    assert fs.error_text == ''
    assert fs.format_spec == 'F'
    assert fs.align == monotable.alignment.NOT_SPECIFIED
    assert fs.width is None
    assert fs.fixed is False
    assert fs.wrap is False
    assert fs.sep == MONOTABLE_CONFIG.sep
    assert fs.none is None
    assert fs.zero == '    '
    assert fs.parentheses is False


def test_parentheses():
    fs = monotable.scanner.FormatScanner('(parentheses)F', MONOTABLE_CONFIG)
    assert fs.error_text == ''
    assert fs.format_spec == 'F'
    assert fs.align == monotable.alignment.NOT_SPECIFIED
    assert fs.width is None
    assert fs.fixed is False
    assert fs.wrap is False
    assert fs.sep == MONOTABLE_CONFIG.sep
    assert fs.none is None
    assert fs.zero is None
    assert fs.parentheses is True


def test_align_left():
    """Test align_spec '<' is scanned as monotable.table._LEFT."""

    fs = monotable.scanner.FormatScanner('<F', MONOTABLE_CONFIG)
    assert fs.align == LEFT
    assert fs.format_spec == 'F'


def test_align_center():
    """Test align_spec '^' is scanned as monotable.table._CENTER."""

    fs = monotable.scanner.FormatScanner('^F', MONOTABLE_CONFIG)
    assert fs.align == CENTER
    assert fs.format_spec == 'F'


def test_align_right():
    """Test align_spec '>' is scanned as monotable.table._RIGHT."""

    fs = monotable.scanner.FormatScanner('>F', MONOTABLE_CONFIG)
    assert fs.align == RIGHT
    assert fs.format_spec == 'F'
