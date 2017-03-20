.. _features-label:

Full List of Features
=====================

- Fine-grained control of formatting and alignment,
  on a per column basis as needed.

  - Set a format string.
  - Specify the alignment of the cell column by prefixing the
    format string with ``<``, ``^``, or ``>``.
  - Specify the alignment of the heading the same way.
  - Set the format function. The format function has the same
    signature as <built-in function format>.  The choices are:

    - <built-in function format> is the default.
    - Adapter to string.format().
    - Adapter to pass a mapping to string.format().
    - Adapter to ``%`` printf style string formatting.
    - Adapter to string.Template().
    - User defined format function.  This requires configuration.


- The default format function is configurable.
- Supports cells that format to multi-line strings and
  truncates too long strings.

  - This prevents unexpected strings from blowing up the table.
  - This allows column width to be minimized.
  - Heading strings can contain newlines.
  - A formatted cell can contain newlines.
  - A formatted cell may be text wrapped to a maximum
    width set for the column.
  - A formatted cell can be truncated to a width set for
    the column. Omission of text is indicated.
  - The number of vertical lines in a cell can be limited.
    Omission of text is indicated.  This requires overriding the
    max_cell_height class variable.
  - ASCII borders can be added around the headings and cells by calling
    the method **bordered_table()**.  The margins and border characters
    are configurable.
  - The table title can contain newlines.
  - The table title can be text wrapped to the width of the table.

- Handles missing or extra cells, missing headings, and
  missing format strings.

  - No need to specify a heading or format string for every column.
  - The first heading/format string/cell is applied to the left most column.
  - Cell grid rows may vary in length.

- Cells of type None are handled.  Appearance is configurable.
- Flexible cell format error handling:

  - Cells that fail the formatting step are identified by row
    and column index.  Trace information is preserved.
  - Cell format error handling is configurable by overriding
    the callback function.  The module includes callback
    functions to ignore, raise, and print the error.

- Add a horizontal rule by placing a **monotable.HR**
  instance in the cellgrid left most column of a row.  HR must be
  enclosed in an iterable for example ``[monotable.HR]``.
- Set the text placed between columns by using the sep= format string option
  or by overriding the sep class variable.
- Set the default float format_spec for columns that have no format string.
- Automatic formatting and alignment by default.
- Method **row_strings()** returns lists of formatted,
  aligned, and justified headings and cells.

To configure monotable and override class variables,
please see :ref:`configuring-label` next.