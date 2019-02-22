Hints
=====

- Text wrapping wraps text to a maximum width, but it can be less.
- Headings are not affected by width, fixed, and wrap format options.
  A wider heading will take precedence.
- Auto-alignment always looks at the type of the cell.
  When reading keys from a cell that is a dictionary
  auto-alignment is determined by the type of the cell
  (in this case dict(), which auto-aligns to the left) and not the
  value of the key.
- In a format string a missing option_spec end delimiter is not an error.
  The intended option_spec text will become part of the format_spec.
- The lsep format directive silently overrides the rsep format directive
  on the preceding column.
- When any scaling format function (thousands(), millions(), ...) is applied
  to a cell of type integer, the resulting value is promoted to float before
  it is formatted.  A format spec compatible with float should be used.
- Check spelling carefully when overriding a class variable.  Misspelling
  will be silently ignored.
- Format directive none=ccc is all lower case.
- The file test/test_examples.py has PEP484 (mypy) type annotation comments
  for experimental static type checking.  It can serve as a guide to solving
  type checking issues.
- In the code option_spec is a synonym for format directive.
