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
.. _Unit_Prefix:
   https://en.m.wikipedia.org/wiki/Unit_Prefix
.. _Binary_Prefix:
   https://en.m.wikipedia.org/wiki/Binary_Prefix

.. _format-functions-label:

Format Functions
================

.. toctree::
   :maxdepth: 2

.. module:: monotable.plugin

| Links to format functions below:
| :py:func:`~boolean`
| :py:func:`~sformat` :py:func:`~mformat` :py:func:`~pformat`
  :py:func:`~tformat`
| :py:func:`~thousands` :py:func:`~millions` :py:func:`~billions`
  :py:func:`~trillions`
| :py:func:`~milli` :py:func:`~micro` :py:func:`~nano` :py:func:`~pico`
| :py:func:`~kibi` :py:func:`~mebi` :py:func:`~gibi` :py:func:`~tebi`

Format functions have the same signature as ``<built-in function format>``.

These can be used to override the class variable
:py:attr:`~monotable.table.MonoTable.format_func` in a subclass
or on an instance.

Boolean Values
--------------

.. autofunction:: boolean

Python Formatting Function Adapters
-----------------------------------

The Python 3 documentation links below show how to write the format spec
for the monotable's adapters to Python formatting functions.

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

Units Format Functions
----------------------

These functions change the units of numeric values.  They multiply or
divide by a floating point number.  The format_spec should be
appropriate for type float.

.. autofunction:: thousands
.. autofunction:: millions
.. autofunction:: billions
.. autofunction:: trillions
.. autofunction:: milli
.. autofunction:: micro
.. autofunction:: nano
.. autofunction:: pico
.. autofunction:: kibi
.. autofunction:: mebi
.. autofunction:: gibi
.. autofunction:: tebi

References
----------

Please refer to Wikipedia articles `Unit_Prefix`_ and `Binary_Prefix`_.
