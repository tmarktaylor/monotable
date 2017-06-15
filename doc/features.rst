.. module:: monotable.table
.. include:: autodoc_ref.txt

Full List of Features
=====================
- Module level convenience functions for use when no configuration is
  required.
- Two ways to specify the table:

  - Provide row of headings, row of formats, cellgrid, and optional title.
  - Provide a list of tuples, one for each column:
    (heading, format, list of cells), and optional title.

To configure monotable and override class variables,
please see :ref:`configuring-label`.

Links like |format_func| below indicate related MonoTable class variables
that can be overridden to configure monotable.


- Fine-grained control of formatting and alignment,
  on a per column basis as needed.

  - Set a format string.
  - Automatic formatting and alignment by default.
  - Specify the alignment of the cell column by prefixing the
    format string with ``<``, ``^``, or ``>``. |align_spec_chars|
  - Specify the alignment of the heading the same way.
  - Set the format function. The format function has the same
    signature as built-in function format().  The choices are:

    - Built-in function format().  This is the default.
    - Boolean formatter that prints arbitrary strings like 'yes' and 'no'
      for the True and False Python boolean values.
    - 12 format functions that scale numeric values by 10e3, 10e6, etc.
    - An unlimited number of user defined format functions that are
      configured by overriding |format_func_map|.
    - Adapters to string.format(), string.Template(), and printf-style
      format functions.


- The default format function is configurable. |format_func|
- Supports cells that format to multi-line strings and
  truncates too long strings.

  - This prevents unexpected strings from blowing up the table.
  - This allows column width to be minimized.
  - Heading strings can contain newlines.
  - A formatted cell can contain newlines.
  - A formatted cell may be text wrapped to a maximum
    width set for the column.
  - A formatted cell can be truncated to a width set for
    the column. Omission of text is indicated. |more_marker|
  - The column width can be fixed.  Short cells will be padded and justified.
  - The number of vertical lines in a cell can be limited. |max_cell_height|
    Omission of text is indicated.
  - Heading and cell vertical alignment is configurable. |heading_valign|
    |cell_valign|
  - ASCII borders can be added around the headings and cells by calling
    the method **bordered_table()**.  The margins and border characters
    are configurable. |border_chars| |hmargin| |vmargin|
  - The table title can contain newlines.
  - The table title can be text wrapped to the width of the table by
    prefixing the title string with |wrap_spec_char|.

- Handles missing or extra cells, missing headings, and
  missing format strings.

  - No need to specify a heading or format string for every column.
  - The first heading/format string/cell is applied to the left most column.
  - Cell grid rows may vary in length.

- Cells of type None are handled.  |format_none_as|.
- None cell values auto-align to the left.
- Set the default float format_spec for columns that have no format string.
  |default_float_format_spec|
- Flexible cell format error handling:

  - Cells that fail the formatting step are identified by row
    and column index.  Trace information is preserved.
  - Cell format error handling is configurable. |format_exc_callback|.
    The module includes callback functions to ignore, raise,
    and print the error.  Please see :ref:`callbacks-label`.

- Change the character used for the top, heading, and bottom guidelines.
  |guideline_chars|
- Add a horizontal rule by placing a **monotable.table.HR**
  instance in the cellgrid left most column of a row.  HR must be
  enclosed in an iterable for example ``[monotable.table.HR]``.
- Set the text placed between columns by using the **sep=** format string
  option or override |sep|.
- Method **row_strings()** returns lists of formatted,
  aligned, and justified headings and cells.
- Creates reStructuredText simple table markup.
  Please refer to :ref:`simple-table-label`. |separated_guidelines|
- Option spec delimiters ``(``, ``;``, or ``)`` are configurable.
  |option_spec_delimiters|
