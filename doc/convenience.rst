.. _convenience-label:

API Functions and Constants
===========================

.. toctree::
   :maxdepth: 2

.. module:: monotable

Functions
---------

The convenience functions below are the quickest way to generate an
Ascii table.
They create and configure a temporary instance of the class MonoTable
and call a member function.

.. autofunction:: mono
.. autofunction:: monocol

Constants
---------

.. autodata:: monotable.mono.HR_ROW
   :annotation:

   HR_ROW is available at the module top level as monotable.HR_ROW.

.. autodata:: monotable.mono.VR_COL
   :annotation:

   VR_COL is available at the module top level as monotable.VR_COL.

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
