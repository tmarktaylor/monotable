"""Assertion based test cases for monotable.table.MonoBlock."""
import pytest

import monotable.table

NOT_SPECIFIED = monotable.table.NOT_SPECIFIED
LEFT = monotable.alignment.LEFT
CENTER = monotable.alignment.CENTER
RIGHT = monotable.alignment.RIGHT

TOP = monotable.alignment.TOP
CENTER_TOP = monotable.alignment.CENTER_TOP
CENTER_BOTTOM = monotable.alignment.CENTER_BOTTOM
BOTTOM = monotable.alignment.BOTTOM

#
# Tests for MonoBlock.__init__().
#


def check_empty_instance(mb):
    """Helper- Make sure empty MonoBlock instance is properly initialized."""

    assert mb.height == 1
    assert mb.width == 0
    assert mb.lines == ['']


def test_init_no_args():
    mb = monotable.table.MonoBlock()
    assert mb._halign == LEFT
    check_empty_instance(mb)


def test_init_empty_string():
    text = ''
    mb = monotable.table.MonoBlock(text)
    assert mb._halign == LEFT
    check_empty_instance(mb)


def test_init_solo_newline():
    mb = monotable.table.MonoBlock('\n')
    assert mb._halign == LEFT
    check_empty_instance(mb)


def test_init_halign_left():
    mb = monotable.table.MonoBlock(halign=LEFT)
    assert mb._halign == LEFT
    check_empty_instance(mb)


def test_init_halign_center():
    mb = monotable.table.MonoBlock(halign=CENTER)
    assert mb._halign == CENTER
    check_empty_instance(mb)


def test_init_halign_right():
    mb = monotable.table.MonoBlock(halign=RIGHT)
    assert mb._halign == RIGHT
    check_empty_instance(mb)


def test_init_illegal_halign():
    # Note- Does not test for newline between the lines.
    bad_msg_start = 'Expected a horizontal align value, got:'
    bad_msg_end = 'Allowed values are: _NOT_SPECIFIED, _LEFT, _CENTER, _RIGHT'

    with pytest.raises(AssertionError) as excinfo:
        _ = monotable.table.MonoBlock(halign=5)
    assert str(excinfo.value).startswith(bad_msg_start)
    assert '5' in str(excinfo.value)
    assert bad_msg_end in str(excinfo.value)

    with pytest.raises(AssertionError) as excinfo:
        _ = monotable.table.MonoBlock(halign=-1)
    assert str(excinfo.value).startswith(bad_msg_start)
    assert '-1' in str(excinfo.value)
    assert bad_msg_end in str(excinfo.value)


def test_init_blank_char():
    text = ' '
    mb = monotable.table.MonoBlock(text)
    assert mb._halign == LEFT
    assert mb.height == 1
    assert mb.width == len(text)
    assert mb.lines == [text]


def test_init_one_line():
    text = ' just one line . '     # leading and trailing spaces
    mb = monotable.table.MonoBlock(text)
    assert mb._halign == LEFT
    assert mb.height == 1
    assert mb.width == len(text)
    assert mb.lines == [text]


def test_init_double_newline():
    mb = monotable.table.MonoBlock('\n\n')
    assert mb._halign == LEFT
    assert mb.height == 2
    assert mb.width == 0
    assert mb.lines == ['', '']


def test_init_triple_newline():
    mb = monotable.table.MonoBlock('\n\n\n', CENTER)
    assert mb._halign == CENTER
    assert mb.height == 3
    assert mb.width == 0
    assert mb.lines == ['', '', '']


def test_init_multi_line():
    mb = monotable.table.MonoBlock('a\nbc\ndef\ng\nhij', LEFT)
    assert mb._halign == LEFT
    assert mb.height == 5
    assert mb.width == 3
    assert mb.lines == ['a', 'bc', 'def', 'g', 'hij']


def test_init_multi_newline():
    mb = monotable.table.MonoBlock('\n\na\nbc\ndef\ng\nhij\n\n', RIGHT)
    assert mb._halign == RIGHT
    assert mb.height == 8
    assert mb.width == 3
    assert mb.lines == ['', '', 'a', 'bc', 'def', 'g', 'hij', '']

#
# Tests for MonoBlock.__str__().
#


def test_str():
    lines = ['ab   hijk', '', 'm', '      n', '', 'p     ']
    text = '\n'.join(lines)
    mb = monotable.table.MonoBlock(text)
    assert str(mb) == text


def test_str_empty():
    mb = monotable.table.MonoBlock()
    assert str(mb) == ''


def test_str_empty_last_line():
    mb = monotable.table.MonoBlock('\n\n')
    assert str(mb) == '\n'


def test_trailing_whitespace():
    mb = monotable.table.MonoBlock('abc  ')
    assert str(mb) == 'abc  '

    mb = monotable.table.MonoBlock('abc  \n  \t')
    assert str(mb) == 'abc  \n  \t'


#
# Tests for MonoBlock.is_all_spaces().
#

def test_is_all_spaces():
    mb = monotable.table.MonoBlock('')
    assert mb.is_all_spaces()

    mb = monotable.table.MonoBlock('\n')
    assert mb.is_all_spaces()

    mb = monotable.table.MonoBlock(' ')
    assert mb.is_all_spaces()

    mb = monotable.table.MonoBlock('  \n\n ')
    assert mb.is_all_spaces()

    mb = monotable.table.MonoBlock('a')
    assert not mb.is_all_spaces()

    mb = monotable.table.MonoBlock('     \na\n')
    assert not mb.is_all_spaces()

    mb = monotable.table.MonoBlock('a\n     ')
    assert not mb.is_all_spaces()


#
# Lines for MonoBlock instances for horizontal justification tests
# and list of them.
#
HORIZONTAL_LINE0 = 'hijk'
HORIZONTAL_LINE1 = ' t u'
HORIZONTAL_LINE2 = 'r  '
HORIZONTAL_LINE3 = ' s'
HORIZONTAL_LINES = [HORIZONTAL_LINE0, HORIZONTAL_LINE1,
                    HORIZONTAL_LINE2, HORIZONTAL_LINE3]
HORIZONTAL_TEXT = '\n'.join(HORIZONTAL_LINES)


def make_instance_for_horizontal_tests(justification):
    """Create a MonoBlock instance with text from JUSTIFY_LINES.

    justification
        Left, center, right, or not specified alignment for justification.
    """

    return monotable.table.MonoBlock(HORIZONTAL_TEXT, justification)

#
# Tests for MonoBlock.chop_to_fieldsize().
#


def test_illegal_fieldsize():
    mb = make_instance_for_horizontal_tests(NOT_SPECIFIED)
    msg = 'nonsense to truncate to fieldsize=0 or less'
    with pytest.raises(AssertionError) as excinfo:
        mb.chop_to_fieldsize(-1)
    assert str(excinfo.value).startswith(msg)

    with pytest.raises(AssertionError) as excinfo:
        mb.chop_to_fieldsize(0)
    assert str(excinfo.value).startswith(msg)


def test_fieldsize_is_1_no_marker():
    mb = make_instance_for_horizontal_tests(NOT_SPECIFIED)
    mb.chop_to_fieldsize(1)
    assert mb.lines == ['h', ' ', 'r', ' ']


def test_fieldsize_is_1():
    mb = make_instance_for_horizontal_tests(NOT_SPECIFIED)
    mb.chop_to_fieldsize(1, more_marker='#')
    assert mb.lines == ['#', '#', '#', '#']


def test_fieldsize_is_1_wider_marker():
    mb = make_instance_for_horizontal_tests(NOT_SPECIFIED)
    mb.chop_to_fieldsize(1, more_marker='##')
    assert mb.lines == ['#', '#', '#', '#']


def test_fieldsize_is_3():
    mb = make_instance_for_horizontal_tests(NOT_SPECIFIED)
    mb.chop_to_fieldsize(3, more_marker='#')
    assert mb.lines == ['hi#', ' t#', 'r  ', ' s']


def test_fieldsize_is_width():
    mb = make_instance_for_horizontal_tests(NOT_SPECIFIED)
    mb.chop_to_fieldsize(mb.width, more_marker='#')
    assert mb.lines == HORIZONTAL_LINES


def test_fieldsize_is_over_width():
    mb = make_instance_for_horizontal_tests(NOT_SPECIFIED)
    mb.chop_to_fieldsize(
        mb.width + 2, more_marker='#')
    assert mb.lines == HORIZONTAL_LINES

#
# Tests for MonoBlock.hjustify() of instance set to left justification.
#


def test_left_justify():
    mb = make_instance_for_horizontal_tests(LEFT)
    mb.hjustify()
    assert mb.lines == [HORIZONTAL_LINE0.ljust(4),
                        HORIZONTAL_LINE1.ljust(4),
                        HORIZONTAL_LINE2.ljust(4),
                        HORIZONTAL_LINE3.ljust(4)]


def test_left_justify_into_larger():
    mb = make_instance_for_horizontal_tests(LEFT)
    mb.hjustify(5)
    assert mb.lines == [HORIZONTAL_LINE0.ljust(5),
                        HORIZONTAL_LINE1.ljust(5),
                        HORIZONTAL_LINE2.ljust(5),
                        HORIZONTAL_LINE3.ljust(5)]


def test_left_justify_into_smaller_ignored():
    mb = make_instance_for_horizontal_tests(LEFT)
    mb.hjustify(2)
    assert mb.lines == [HORIZONTAL_LINE0.ljust(4),
                        HORIZONTAL_LINE1.ljust(4),
                        HORIZONTAL_LINE2.ljust(4),
                        HORIZONTAL_LINE3.ljust(4)]

#
# Tests for MonoBlock.hjustify() of instance set to center justification.
#


def test_center_justify():
    mb = make_instance_for_horizontal_tests(CENTER)
    mb.hjustify()
    assert mb.lines == [HORIZONTAL_LINE0.center(4),
                        HORIZONTAL_LINE1.center(4),
                        HORIZONTAL_LINE2.center(4),
                        HORIZONTAL_LINE3.center(4)]


def test_center_justify_into_larger():
    mb = make_instance_for_horizontal_tests(CENTER)
    mb.hjustify(5)
    assert mb.lines == [HORIZONTAL_LINE0.center(5),
                        HORIZONTAL_LINE1.center(5),
                        HORIZONTAL_LINE2.center(5),
                        HORIZONTAL_LINE3.center(5)]


def test_center_justify_into_smaller_ignored():
    mb = make_instance_for_horizontal_tests(CENTER)
    mb.hjustify(2)
    assert mb.lines == [HORIZONTAL_LINE0.center(4),
                        HORIZONTAL_LINE1.center(4),
                        HORIZONTAL_LINE2.center(4),
                        HORIZONTAL_LINE3.center(4)]

#
# Tests for MonoBlock.hjustify() of instance set to right justification.
#


def test_right_justify():
    mb = make_instance_for_horizontal_tests(RIGHT)
    mb.hjustify()
    assert mb.lines == [HORIZONTAL_LINE0.rjust(4),
                        HORIZONTAL_LINE1.rjust(4),
                        HORIZONTAL_LINE2.rjust(4),
                        HORIZONTAL_LINE3.rjust(4)]


def test_right_justify_into_larger():
    mb = make_instance_for_horizontal_tests(RIGHT)
    mb.hjustify(5)
    assert mb.lines == [HORIZONTAL_LINE0.rjust(5),
                        HORIZONTAL_LINE1.rjust(5),
                        HORIZONTAL_LINE2.rjust(5),
                        HORIZONTAL_LINE3.rjust(5)]


def test_right_justify_into_smaller_ignored():
    mb = make_instance_for_horizontal_tests(RIGHT)
    mb.hjustify(2)
    assert mb.lines == [HORIZONTAL_LINE0.rjust(4),
                        HORIZONTAL_LINE1.rjust(4),
                        HORIZONTAL_LINE2.rjust(4),
                        HORIZONTAL_LINE3.rjust(4)]

#
# Tests for MonoBlock.vjustify().
#
# The following tests that call MonoBlock.vjustify are run on
# MonoBlocks initialized arbitrarily for left, center, and right justification.
# The tests should work for any horizontal justification.
#


def test_illegal_height():
    mb = make_instance_for_horizontal_tests(RIGHT)
    msg = 'nonsense if less than 1 line in result'
    with pytest.raises(AssertionError) as excinfo:
        mb.vjustify(TOP, 0)
    assert str(excinfo.value).startswith(msg)

    with pytest.raises(AssertionError) as excinfo:
        mb.vjustify(TOP, -1)
    assert str(excinfo.value).startswith(msg)


def test_top_justify():
    mb = make_instance_for_horizontal_tests(LEFT)
    mb.vjustify(TOP, 6)
    assert mb.height == 6
    assert mb.width == 4
    assert mb.lines == [HORIZONTAL_LINE0, HORIZONTAL_LINE1,
                        HORIZONTAL_LINE2, HORIZONTAL_LINE3,
                        '    ', '    ']


def test_illegal_vertical_justify():
    # Note- Only tests the first part of the exception string.
    mb = make_instance_for_horizontal_tests(LEFT)
    msg = 'Expected a vertical align value, got:'
    with pytest.raises(AssertionError) as excinfo:
        mb.vjustify(-1, 6)
    assert str(excinfo.value).startswith(msg)

    with pytest.raises(AssertionError) as excinfo:
        mb.vjustify(0, 6)
    assert str(excinfo.value).startswith(msg)

    with pytest.raises(AssertionError) as excinfo:
        mb.vjustify(19, 6)
    assert str(excinfo.value).startswith(msg)

    with pytest.raises(AssertionError) as excinfo:
        mb.vjustify(25, 6)
    assert str(excinfo.value).startswith(msg)


def test_center_top_justify():
    mb = make_instance_for_horizontal_tests(RIGHT)
    mb.vjustify(CENTER_TOP, 7)
    assert mb.height == 7
    assert mb.width == 4
    assert mb.lines == ['    ',
                        HORIZONTAL_LINE0, HORIZONTAL_LINE1,
                        HORIZONTAL_LINE2, HORIZONTAL_LINE3,
                        '    ', '    ']


def test_center_bottom_justify():
    mb = make_instance_for_horizontal_tests(RIGHT)
    mb.vjustify(CENTER_BOTTOM, 7)
    assert mb.height == 7
    assert mb.width == 4
    assert mb.lines == ['    ', '    ',
                        HORIZONTAL_LINE0, HORIZONTAL_LINE1, HORIZONTAL_LINE2,
                        HORIZONTAL_LINE3,
                        '    ']


def test_bottom_justify():
    mb = make_instance_for_horizontal_tests(RIGHT)
    mb.vjustify(BOTTOM, 5)
    assert mb.height == 5
    assert mb.width == 4
    assert mb.lines == ['    ',
                        HORIZONTAL_LINE0, HORIZONTAL_LINE1,
                        HORIZONTAL_LINE2, HORIZONTAL_LINE3]


#
# Tests for MonoBlock.vjustify().
#

#
# Lines for MonoBlock instances for vertical justification tests
# and list of them.
#
VERTICAL_LINE0 = 'hijk'
VERTICAL_LINE1 = 't'
VERTICAL_LINE2 = 'r  '
VERTICAL_LINE3 = ' s'
VERTICAL_TEXT = '\n'.join([VERTICAL_LINE0, VERTICAL_LINE1,
                           VERTICAL_LINE2, VERTICAL_LINE3])


def make_instance_for_vertical_tests(justification):
    """Create a MonoBlock instance with text from VERTICAL_LINES.

    justification
        Left, center, right, or not specified alignment for justification.
    """

    return monotable.table.MonoBlock(VERTICAL_TEXT, justification)


def test_vertical_truncate_no_marker():
    mb = make_instance_for_vertical_tests(RIGHT)
    mb.vjustify(TOP, 3)
    assert mb.height == 3
    assert mb.width == 4
    assert mb.lines == [VERTICAL_LINE0, VERTICAL_LINE1, 'r  ']


def test_vertical_truncate_1_char_marker():
    mb = make_instance_for_vertical_tests(RIGHT)
    mb.vjustify(TOP, 3, more_marker='#')
    assert mb.height == 3
    assert mb.width == 4
    assert mb.lines == [VERTICAL_LINE0, VERTICAL_LINE1, 'r  #']


def test_vertical_truncate_2_char_marker():
    mb = make_instance_for_vertical_tests(RIGHT)
    mb.vjustify(TOP, 3, more_marker='##')
    assert mb.height == 3
    assert mb.width == 4
    assert mb.lines == [VERTICAL_LINE0, VERTICAL_LINE1, 'r ##']


def test_vertical_truncate_3_char_marker():
    mb = make_instance_for_vertical_tests(RIGHT)
    mb.vjustify(TOP, 3, more_marker='###')
    assert mb.height == 3
    assert mb.width == 4
    assert mb.lines == [VERTICAL_LINE0, VERTICAL_LINE1, 'r###']


def test_vertical_truncate_4_char_marker():
    mb = make_instance_for_vertical_tests(RIGHT)
    mb.vjustify(TOP, 3, more_marker='####')
    assert mb.height == 3
    assert mb.width == 4
    assert mb.lines == [VERTICAL_LINE0, VERTICAL_LINE1, '####']


def test_vertical_truncate_wider_marker():
    mb = make_instance_for_vertical_tests(RIGHT)
    mb.vjustify(TOP, 3, more_marker='#####')
    assert mb.height == 3
    assert mb.width == 4
    assert mb.lines == [VERTICAL_LINE0, VERTICAL_LINE1, '####']


def test_vertical_truncate_short_line():
    mb = make_instance_for_vertical_tests(RIGHT)
    mb.vjustify(TOP, 2, more_marker='###')
    assert mb.height == 2
    assert mb.width == 4
    assert mb.lines == [VERTICAL_LINE0, 't###']

#
# Tests for MonoBlock.add_border().
#


def test_add_border_negative_hmargin_ignored():
    mb = monotable.table.MonoBlock()
    mb.add_border(hmargin=-1)
    assert str(mb) == '++\n||\n++'


def test_add_border_negative_vmargin_ignored():
    mb = monotable.table.MonoBlock()
    mb.add_border(hmargin=0, vmargin=-1)
    assert str(mb) == '++\n||\n++'


def test_add_border_empty_monoblock():
    mb = monotable.table.MonoBlock()
    mb.add_border(hmargin=0)
    assert str(mb) == '++\n||\n++'


def test_add_border_1_char_monoblock():
    mb = monotable.table.MonoBlock('b')
    mb.add_border(hmargin=0, border_chars='1234')
    assert str(mb) == '414\n3b3\n424'


def test_add_border_no_justify():
    mb = monotable.table.MonoBlock('ABCDE\nF\nG')
    mb.add_border()
    assert str(mb) == '\n'.join(['+-------+',
                                 '| ABCDE |',
                                 '| F     |',
                                 '| G     |',
                                 '+-------+'])


def test_add_border_extra_border_chars():
    mb = monotable.table.MonoBlock('ABCDE\nF\nG')
    mb.add_border(border_chars='--|+=XXXXXX')
    assert str(mb) == '\n'.join(['+-------+',
                                 '| ABCDE |',
                                 '| F     |',
                                 '| G     |',
                                 '+-------+'])


def test_add_border_fewer_border_chars():
    mb = monotable.table.MonoBlock('ABCDE\nF\nG')
    mb.add_border(border_chars='_')
    assert str(mb) == '\n'.join(['+_______+',
                                 '+ ABCDE +',
                                 '+ F     +',
                                 '+ G     +',
                                 '+++++++++'])


def test_add_border_justified():
    mb = monotable.table.MonoBlock('ABCDE\nF\nG', RIGHT)
    mb.add_border()
    assert str(mb) == '\n'.join(['+-------+',
                                 '| ABCDE |',
                                 '|     F |',
                                 '|     G |',
                                 '+-------+'])


def test_add_border_bigger_margins():
    mb = monotable.table.MonoBlock('ABCDE\nF\nG', CENTER)
    mb.add_border(hmargin=2, vmargin=3)
    assert str(mb) == '\n'.join(['+---------+',
                                 '|         |',
                                 '|         |',
                                 '|         |',
                                 '|  ABCDE  |',
                                 '|    F    |',
                                 '|    G    |',
                                 '|         |',
                                 '|         |',
                                 '|         |',
                                 '+---------+'])

#
# Tests for MonoBlock.remove_top_line().
#


def test_remove_top_line_empty_monoblock():
    mb = monotable.table.MonoBlock()
    mb.remove_top_line()
    assert mb.height == 1
    assert mb.width == 0
    assert str(mb) == ''


def test_remove_top_line_one_line_monoblock():
    mb = monotable.table.MonoBlock('abc')
    mb.remove_top_line()
    assert mb.height == 1
    assert mb.width == 0
    assert str(mb) == ''


def test_remove_top_line_multiline_monoblock():
    mb = monotable.table.MonoBlock('ABCDE\nF\nG', RIGHT)
    mb.remove_top_line()
    assert str(mb) == 'F\nG'

#
# Tests for MonoBlock.remove_left_column().
#


def test_remove_left_column_zero_width_monoblock():
    mb = monotable.table.MonoBlock()
    mb.remove_left_column()
    assert mb.height == 1
    assert mb.width == 0
    assert str(mb) == ''


def test_remove_left_column_one_line_monoblock():
    mb = monotable.table.MonoBlock('abc')
    mb.remove_left_column()
    assert mb.height == 1
    assert mb.width == 2
    assert str(mb) == 'bc'


def test_remove_left_column_multiline_monoblock():
    mb = monotable.table.MonoBlock('ABCDE\nF\nG', RIGHT)
    mb.remove_left_column()
    assert str(mb) == 'BCDE\n\n'
