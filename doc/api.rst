Module Api
==========

.. toctree::
   :maxdepth: 2

.. module:: monotable
.. include:: autodoc_ref.txt

MonoTable
---------

.. autoclass:: MonoTable
.. automethod:: MonoTable.__init__
.. automethod:: MonoTable.table
.. automethod:: MonoTable.bordered_table
.. automethod:: MonoTable.row_strings

.. _class-vars-label:

MonoTable Class Variables
-------------------------

| Link to class variable below:
| |format_func| |format_exc_callback|
| |default_float_format_spec| |format_none_as|
| |sep| |separated_guidelines| |guideline_chars|
| |format_func_map|
| |more_marker| |align_spec_chars| |wrap_spec_char|
| |option_spec_delimiters|
| |heading_valign| |cell_valign| |max_cell_height|
| |border_chars| |hmargin| |vmargin|

.. autoattribute:: MonoTable.format_func
.. autoattribute:: MonoTable.format_exc_callback

.. autoattribute:: MonoTable.default_float_format_spec
.. autoattribute:: MonoTable.format_none_as

.. autoattribute:: MonoTable.sep
.. autoattribute:: MonoTable.separated_guidelines
.. autoattribute:: MonoTable.guideline_chars

.. autoattribute:: MonoTable.format_func_map

.. autoattribute:: MonoTable.more_marker
.. autoattribute:: MonoTable.align_spec_chars
.. autoattribute:: MonoTable.wrap_spec_char
.. autoattribute:: MonoTable.option_spec_delimiters

.. autoattribute:: MonoTable.heading_valign
.. autoattribute:: MonoTable.cell_valign
.. autoattribute:: MonoTable.max_cell_height

.. autoattribute:: MonoTable.border_chars
.. autoattribute:: MonoTable.hmargin
.. autoattribute:: MonoTable.vmargin

Exception
---------

.. autoexception:: MonoTableCellError

Horizontal Rule
---------------

.. autodata:: monotable.HR
   :annotation:

Vertical Alignment Constants
----------------------------

For convenience these names are copied to the monotable namespace by
__init__.py.  They are unique int enumeration values.
They are accesible as::

   monotable.TOP
   montable.CENTER_TOP
   montable.CENTER_BOTTOM
   montable.BOTTOM


.. Using monotable.alignment.TOP, etc. here since Sphinx autodata renders
   the description of them incorrectly.  Don't know why.

.. autodata:: monotable.alignment.TOP
.. autodata:: monotable.alignment.CENTER_TOP
.. autodata:: monotable.alignment.CENTER_BOTTOM
.. autodata:: monotable.alignment.BOTTOM


Functions
---------

.. module:: monotable.plugin

Format Functions
****************

.. _Format Spec:
   https://docs.python.org
   /3/library/string.html#format-specification-mini-language
.. _Format String Syntax:
   https://docs.python.org/3/library/string.html#format-string-syntax
.. _Template Strings:
   https://docs.python.org/3/library/string.html#template-strings
.. _printf-style:
   https://docs.python.org
   /3/library/stdtypes.html#printf-style-string-formatting

Format functions have the same signature as ``<built-in function format>``.

These can be used to override the class variable
:py:attr:`~MonoTable.format_func` in a subclass or on an instance.
Be sure to use staticmethod().

The Python 3 documentation links below show how to write the format spec
for built-in function format and each of monotable's
format functions.

========  =======================
function  Python 3 Documentation
========  =======================
format    `Format Spec`_
sformat   `Format String Syntax`_
mformat   same as sformat
tformat   `Template Strings`_
pformat   `printf-style`_
========  =======================

.. autofunction:: sformat
.. autofunction:: mformat
.. autofunction:: pformat
.. autofunction:: tformat

Format Function Error Callbacks
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Format function error callbacks take an instance of
monotable.MonoTableCellError.

.. autofunction:: raise_it
.. autofunction:: print_it
.. autofunction:: ignore_it
