.. _convenience-label:

Module Level API
================

.. toctree::
   :maxdepth: 2

.. module:: monotable

monotable.HR_ROW
    Row containing a horizontal rule to use as a row in cellgrid.

monotable.VR_COL
    Vertical rule column for use as a column_tuple with monocol().

monotable.MonoTable
    Class to create an aligned and formatted text table from a grid of cells.

Functions
---------

The convenience functions below are the quickest way to generate an
Ascii table.
They create and configure a temporary instance of the class MonoTable
and call a member function.

.. autofunction:: mono
.. autofunction:: monocol

.. issue- using autodata:: monotable.HR_ROW and others here included
.. unwanted text

Legacy Functions
----------------
The details of the function parameters are provided in the class MonoTable
docstrings located by following the links below.

.. module:: monotable.table

.. autofunction:: table
.. autofunction:: bordered_table
.. autofunction:: cotable
.. autofunction:: cobordered_table

.. note:: The prefix **co** in cotable and cobordered_table
   stands for column oriented.
