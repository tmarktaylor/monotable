Functions
=========

.. toctree::
   :maxdepth: 2

.. module:: monotable.table

The convenience functions below are the quickest way to generate an
Ascii table.
They are module level functions in the module **monotable.table**.
They create a temporary instance of the class MonoTable
and call the same named MonoTable member function.

The details of the function parameters are provided in the class MonoTable
docstrings located by following the links below.

These functions are useful when the default configuration of
class MonoTable meets the caller's needs.

If MonoTable configuration is required,
please see section :ref:`configuring-label`.

.. do not need links since descriptions are short
.. Links:
.. :py:func:`~table`
.. :py:func:`~bordered_table`
.. :py:func:`~cotable`
.. :py:func:`~cobordered_table`

.. autofunction:: table
.. autofunction:: bordered_table
.. autofunction:: cotable
.. autofunction:: cobordered_table

.. note:: The prefix **co** in cotable and cobordered_table
   stands for column oriented.
