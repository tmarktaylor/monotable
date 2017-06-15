.. _configuring-label:

How to Configure MonoTable
==========================

.. toctree::
   :maxdepth: 2

.. module:: monotable

Two Ways to Customize
---------------------

1. Create a subclass of MonoTable and override one or more
   :ref:`class-vars-label`

.. testcode::

    import monotable.table

    class SeparatedMonoTable(monotable.table.MonoTable):
       guideline_chars = '-=-'
       separated_guidelines = True

    headings = ['an int', 'string', 'another int', 'another string']
    tbl = SeparatedMonoTable()

    cells = [[123, 'import', 4567, 'this']]

    print(tbl.table(headings, [], cells, title='Subclass of MonoTable.'))

.. testoutput::

               Subclass of MonoTable.
    ------  ------  -----------  --------------
    an int  string  another int  another string
    ======  ======  ===========  ==============
       123  import         4567  this
    ------  ------  -----------  --------------

2. Assign to one or more :ref:`class-vars-label` on an instance.

   This creates an instance variable that overrides the class variable
   with an instance variable of the same name.

.. testcode::

    import monotable.table

    headings = ['an int', 'string', 'another int', 'another string']
    tbl = monotable.table.MonoTable()
    tbl.guideline_chars = '-=-'
    tbl.separated_guidelines = True

    cells = [[123, 'import', 4567, 'this']]

    print(tbl.table(headings, [], cells, title='Override on an instance.'))


.. testoutput::

              Override on an instance.
    ------  ------  -----------  --------------
    an int  string  another int  another string
    ======  ======  ===========  ==============
       123  import         4567  this
    ------  ------  -----------  --------------

.. note::
   Double check the spelling of the class variable.
   A misspelled variable name will be silently ignored.



These techniques work because:
    - None of the instance variables assigned by __init__()
      depend on the value of any other class or instance variable.
    - MonoTable member functions, except __init__(), do not modify any
      class or instance variables.