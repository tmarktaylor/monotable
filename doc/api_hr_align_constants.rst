Rules, Vertical Align Constants
===============================

.. toctree::
   :maxdepth: 2

.. module:: monotable.table

HR_ROW and VR_COL are accesible at the top level module level
as monotable.HR_ROW and monotable.VR_COL.

Horizontal Rule
---------------
.. autodata:: monotable.mono.HR_ROW

.. autodata:: HR
   :annotation:

Vertical Rule Column
--------------------
.. autodata:: monotable.mono.VR_COL

.. _vertical-alignment-constants-label:

Vertical Alignment Constants
----------------------------

Use these to specify a value for MonoTable class variable
:py:attr:`~MonoTable.heading_valign` or
:py:attr:`~MonoTable.cell_valign`

.. autodata:: monotable.alignment.TOP
.. autodata:: monotable.alignment.CENTER_TOP
.. autodata:: monotable.alignment.CENTER_BOTTOM
.. autodata:: monotable.alignment.BOTTOM
