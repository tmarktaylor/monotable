Hints
=====

- Text wrapping wraps text to a maximum width, but it can be less.
- Headings are not affected by width, fixed, and wrap format options.
  A wider heading will take precedence.
- Check spelling carefully when overriding a class variable.  Misspelling
  will be silently ignored.
- Auto-alignment always looks at the type of the cell.
  When reading keys from a cell that is a dictionary
  auto-alignment is determined by the type of the cell and not the
  value of the key.
- In a format string a missing option_spec end delimiter is not an error.
  The intended option_spec text will become part of the format_spec.
- The sep format option applies to *after* the column where it is specified.
- The file test/test_examples.py has PEP484 (mypy) type annotation comments
  for experimental static type checking.  It can serve as a guide to solving
  type checking issues.
