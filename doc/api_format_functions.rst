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

.. _format-functions-label:

Format Functions
================

.. toctree::
   :maxdepth: 2

.. module:: monotable
.. module:: monotable.plugin

| Links to format functions below:
| :py:func:`~boolean`
| :py:func:`~thousands` :py:func:`~millions` :py:func:`~billions`
| :py:func:`~milli` :py:func:`~micro` :py:func:`~nano`
| :py:func:`~kilo` :py:func:`~mega` :py:func:`~terra`
| :py:func:`~sformat` :py:func:`~mformat` :py:func:`~pformat`
  :py:func:`~tformat`

Format functions have the same signature as ``<built-in function format>``.

These can be used to override the class variable
:py:attr:`~MonoTable.format_func` in a subclass or on an instance.


.. autofunction:: boolean
.. autofunction:: thousands
.. autofunction:: millions
.. autofunction:: billions
.. autofunction:: trillions
.. autofunction:: milli
.. autofunction:: micro
.. autofunction:: nano
.. autofunction:: pico
.. autofunction:: kilo
.. autofunction:: mega
.. autofunction:: terra

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
