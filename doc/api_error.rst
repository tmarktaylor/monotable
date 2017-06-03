Exception and Error Callbacks
=============================

.. toctree::
   :maxdepth: 2

Exception
---------

.. module:: monotable.table
.. autoexception:: MonoTableCellError

.. _callbacks-label:

Format Function Error Callbacks
-------------------------------

Format function error callbacks take an instance of
monotable.table.MonoTableCellError.

These are used to override the class variable
:py:attr:`~MonoTable.format_exc_callback` in a subclass or on an instance.

.. module:: monotable.plugin
.. autofunction:: raise_it
.. autofunction:: print_it
.. autofunction:: ignore_it
