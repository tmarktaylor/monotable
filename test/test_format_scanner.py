"""Assertion based test cases for monotable.scanner.FormatScanner."""
import pytest

import monotable.plugin
import monotable.scanner

TOP = monotable.TOP
CENTER_TOP = monotable.CENTER_TOP
CENTER_BOTTOM = monotable.CENTER_BOTTOM
BOTTOM = monotable.BOTTOM

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

    expected_format_functions = [
        '  mformat - <function mformat',
        '  pformat - <function pformat',
        '  sformat - <function sformat',
        '  tformat - <function tformat']

    lines = format_scanner._allowed_format_functions()
    for expected, actual in zip(expected_format_functions, lines):
        assert actual.startswith(expected)


def test_allowed_format_functions_user_format_functions():
    """Checks for match of just the beginning of each string.."""

    expected_format_functions = [
        '  mformat - <function mformat',
        '  myformat - <function ',
        '  mysecondformat - <function ',
        '  pformat - <function pformat',
        '  sformat - <function sformat',
        '  tformat - <function tformat']

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


def test_allowed_format_functions_user_hides_predefined():
    """Checks for match of just the beginning of each string."""

    expected_format_functions = [
        '  mformat - <function mformat',
        '  myformat - <function ',
        '  pformat - <function pformat',
        '  sformat - <function ',      # py -2, py -3 differ beyond here
        '  tformat - <function tformat'
    ]

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
        'Options are enclosed by "(" and ")".  Options are separated by ";".',
        'For example: "(max=22;sep=   )"',
        'Case is significant. Whitespace is not allowed except',
        'after =.  Allowed options are:',
        '  wrap=N  - wrap/rewrap to width of N columns. N > 0.',
        '  max=N   - truncate to max width of N columns. N > 0.',
        '  sep=ccc - characters after sep= are the column separator.',
        ''
        ])

    # The test checks for match of just the beginning of each string.
    expected_format_functions = [
        '  mformat - <function mformat',
        '  pformat - <function pformat',
        '  sformat - <function sformat',
        '  tformat - <function tformat'
    ]
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

    format_str = '(max=22;wrap=19;sep= | ;pformat){:2.7d}'
    fs = monotable.scanner.FormatScanner(format_str, MONOTABLE_CONFIG)
    assert fs.error_text == ''
    assert fs.max == 22
    assert fs.wrap == 19
    assert fs.sep == ' | '
    assert fs.format_func == monotable.plugin.pformat


# List of good format_str concentrating on the option_spec part
# with various options and spacing.  These are used to to show that
# parsing succeeds.
good_format_str_list = [
    # Valid even when missing option_spec end delimiter
    '(max=22;wrap=19{:2.7d}',

    '(max=3;wrap=19;sep= | ;pformat){:2.7d}',
    '( max =3)',
    '( max= 3)',
    '( max = 3)',
    '( max  = 3 )',
    '(  max  =  3)'
    '( wrap = 4)',
    '(  wrap = 4 )',
    '(sep=)',
    '( sep=)',
    '(  sep= )',
    '( sformat)',
    '(sformat )',
    '( pformat)',
    '(pformat )',
    '( mformat)',
    '(mformat )',
    '(tformat )',
    '( tformat)',
    '(max = 3 ; wrap= 19 ;sep= | ;   pformat){:2.7d}']


@pytest.mark.parametrize("a_good_format_str", good_format_str_list)
def test_init_parse_extra_spacing(a_good_format_str):
    """A valid format_str creates empty error_text."""

    fs = monotable.scanner.FormatScanner(a_good_format_str, MONOTABLE_CONFIG)
    assert fs.error_text == ''


# List of illegal format_str concentrating on the option_spec part
# with various typos in the options.
bad_format_str_list = [
    # comma is a bad delimiter
    '(max=22;wrap=19,sep= | ;pformat){:2.7d}',

    # no allowed options
    '(bogus)format_str',

    # bad option name mable, wrap option has no =value
    '(mable=22;wrap){:2.7d}',

    # wrap option has no '='
    '(wrap){:2.7d}',

    # wrap option has no value
    '(wrap=){:2.7d}',

    # wrap option has bad value 0
    '(wrap=0){:2.7d}',

    # wrap option has bad value (negative)
    '(wrap=-1){:2.7d}',

    # max option has no '='
    '(max){:2.7d}',

    # max option has no value
    '(max=){:2.7d}',

    # max option has bad value 0
    '(max=0){:2.7d}',

    # max option has bad value (negative)
    '(max=-1){:2.7d}',

    # sep option has no '='
    '(sep){:2.7d}',

    # extra '='
    '(max=4=){:2.7d}',

    # more than one max
    '(max=3;max=4){:2.7d}',

    # the option in all '='
    '(max=3;=====){:2.7d}',

    # more than one format function
    '(tformat;sformat){:2.7d}']


@pytest.mark.parametrize("a_bad_format_str", bad_format_str_list)
def test_parse_assorted_bad_options(a_bad_format_str):
    fs = monotable.scanner.FormatScanner(a_bad_format_str, MONOTABLE_CONFIG)
    assert fs.error_text[:14] == 'In option_spec'


def valid_options_shuffled_helper(fs):
    """Check a FormatScanner instance in test_valid_options_shuffled()."""

    assert fs.error_text == ''
    assert fs.align == LEFT
    assert fs.wrap == 5
    assert fs.max == 10
    assert fs.sep == 'ZZZ'


# List of good format_str where the option_spec part has the same
# valid options, just in different orders.
shuffled_option_list = [
    '<( sep =ZZZ;wrap =5;max= 10;pformat)my_format_spec',
    '<( sep =ZZZ;wrap =5;pformat;max= 10)my_format_spec',
    '<(max= 10;pformat;wrap =5; sep =ZZZ)my_format_spec',
    '<( sep =ZZZ;max= 10;wrap =5;pformat)my_format_spec',
    '<(pformat;wrap =5;max= 10; sep =ZZZ)my_format_spec',
    '<( sep =ZZZ;pformat;wrap =5;max= 10)my_format_spec',
    '<(pformat;max= 10; sep =ZZZ;wrap =5)my_format_spec',
    '<(pformat;wrap =5; sep =ZZZ;max= 10)my_format_spec',
    '<(wrap =5;pformat; sep =ZZZ;max= 10)my_format_spec',
    '<(pformat; sep =ZZZ;wrap =5;max= 10)my_format_spec',
    '<( pformat;max= 10;wrap =5; sep =ZZZ)my_format_spec',
    '<(max= 10; sep =ZZZ;wrap =5;pformat)my_format_spec',
    '<( wrap =5; sep =ZZZ;max= 10;pformat)my_format_spec',
    '<( sep =ZZZ;max= 10;pformat;wrap =5)my_format_spec',
    '<( sep =ZZZ;wrap =5;pformat;max= 10)my_format_spec',
    '<(wrap =5;pformat; sep =ZZZ;max= 10)my_format_spec',
    '<(pformat; sep =ZZZ;max= 10;wrap =5)my_format_spec',
    '<( pformat;max= 10; sep =ZZZ;wrap =5)my_format_spec',
    '<( wrap =5;pformat; sep =ZZZ;max= 10)my_format_spec',
    '<(max= 10; sep =ZZZ;pformat;wrap =5)my_format_spec']


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
    assert fs.sep == '     '


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
