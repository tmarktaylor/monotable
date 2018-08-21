Functions
=========

.. toctree::
   :maxdepth: 2

.. module:: monotable.table

The convenience functions below are the quickest way to generate an
Ascii table.
They create and configure a temporary instance of the class MonoTable
and call a member function.

mono() and monocol() are accessible at the top level module level
as monotable.mono() and monotable.monocol().

To create a custom MonoTable class,
please see section :ref:`configuring-label`.

.. autofunction:: monotable.mono.mono
.. autofunction:: monotable.mono.monocol

Legacy Functions
================
The details of the function parameters are provided in the class MonoTable
docstrings located by following the links below.

.. autofunction:: table
.. autofunction:: bordered_table
.. autofunction:: cotable
.. autofunction:: cobordered_table

.. note:: The prefix **co** in cotable and cobordered_table
   stands for column oriented.
