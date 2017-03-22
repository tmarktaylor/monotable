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

Format Functions
================

.. toctree::
   :maxdepth: 2

.. module:: monotable
.. module:: monotable.plugin

Links: :py:func:`~sformat`
:py:func:`~mformat`
:py:func:`~pformat`
:py:func:`~tformat`

Format functions have the same signature as ``<built-in function format>``.

These can be used to override the class variable
:py:attr:`~MonoTable.format_func` in a subclass or on an instance.

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
