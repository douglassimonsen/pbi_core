Examples
========

Basic Functionality
-------------------

This basic example tests that your PowerBI report can be parsed and reassembled by ``pbi_core``. 

Functionality used:

- `pbi_core.load_pbix() <pbi_core.html#pbi_core.main.LocalReport.load_pbix>`_
- `pbi_core.save_pbix() <pbi_core.html#pbi_core.main.LocalReport.save_pbix>`_


.. code-block:: python
   :linenos:

   from pbi_core import LocalReport

   report = LocalReport.load_pbix("example.pbix")
   report.save_pbix("example_out.pbix")


Altering Data model
-------------------

This example shows how you can add automatic descriptions to PowerBI columns (possibly from some governance tool??)

Functionality used:

- `Column <ssas_records/column.html>`_
- `column.alter() <ssas_records/column.html>`_

.. code-block:: python
   :linenos:

   from pbi_core import LocalReport

   report = LocalReport.load_pbix("example.pbix")
   for column in report.ssas.columns:
      column.description = "pbi_core has touched this"
      column.alter()  # saves the changes to the SSAS DB

   report.save_pbix("example_out.pbix")


Finding records in SSAS tables
------------------------------

This example shows how to find SSAS records and extract data from report columns

Functionality used:

- `group.find() <ssas_records/_group.html#pbi_core.ssas.model_tables._group.Group.find>`_
- `measure.table() <ssas_records/measure.html#pbi_core.ssas.model_tables.measure.Measure.table>`_
- `table.columns() <ssas_records/table.html#pbi_core.ssas.model_tables.table.Table.columns>`_
- `measure.data() <ssas_records/measure.html#pbi_core.ssas.model_tables.measure.Measure.data>`_


.. code-block:: python
   :linenos:

   from pbi_core import LocalReport

   report = LocalReport.load_pbix("example.pbix")
   values = report.ssas.columns.find({"explicit_name": "a"}).data()
   print(values)
   values2 = report.ssas.tables.find({"name": "Table"}).data()
   print(values2)

   measure = report.ssas.measures.find({"name": "Measure"})
   column = measure.table().columns()[1]  # the first column is a hidden row-count column that can't be used in measures
   values3 = measure.data(column, head=10)
   print(values3)

Pbyx Lineage Chart
------------------

This example displays a lineage chart in HTML:

Functionality used:

- `column.get_lineage() <ssas_records/column.html#pbi_core.ssas.model_tables.column.Column.get_lineage>`_

.. code-block:: python
   :linenos:

   from pbi_core import LocalReport

   report = LocalReport.load_pbix("example.pbix", kill_ssas_on_exit=True)
   col = report.ssas.columns.find({"explicit_name": "MeasureColumn"})
   col.get_lineage("parents").to_mermaid().show()


Improved Multilanguage Support
------------------------------

This example displays the ability to easily convert PBIX reports to alternate languages:

Functionality used:

- `get_static_elements <na>`_
- `set_static_elements <na>`_

.. code-block:: python
   :linenos:

   from pbi_core import LocalReport
   from pbi_core.misc.internationalization import get_static_elements, set_static_elements

   report = LocalReport.load_pbix("example.pbix", kill_ssas_on_exit=True)
   x = get_static_elements(report.static_files.layout)
   x.to_excel("multilang.xlsx")

   set_static_elements("multilang1.xlsx", "example.pbix")

Automatic Data Model Cleaning
-----------------------------

One of the core tensions in PowerBI is the size of the data model. In development, you want to have many measures, columns, and tables to simplify new visual creation. After developing the report, the additional elements create two issues:

1. It's difficult to understand which elements are being used and how they relate to each other
2. The additional columns and tables can slow down visual rendering times, negatively impacting UX

Pbyx has an automatic element culler that allows you to remove unnecessary elements after the report has been designed:

Functionality used:

- `pbi_core.cleanse_ssas_model <pbi_core.html#pbi_core.main.LocalReport.cleanse_ssas_model>`_

.. code-block:: python
   :linenos:

   from pbi_core import LocalReport

   report = LocalReport.load_pbix("example_pbis/api.pbix")
   report.cleanse_ssas_model()
   report.save_pbix("cull_out.pbix")
