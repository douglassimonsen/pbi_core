Examples
========

Basic Functionality
-------------------

This basic example tests that your PowerBI report can be parsed and reassembled by ``pbi_core``:

.. code-block:: python
   :linenos:

   from pbi_core import LocalReport

   report = LocalReport.load_pbix("example.pbix")
   report.save_pbix("example_out.pbix")


Altering Data model
-------------------

This example shows how you can add automatic descriptions to PowerBI columns (possibly from some governance tool??)

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

This example shows how to extract data from report columns


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

.. code-block:: python
   :linenos:

   from pbi_core import LocalReport

   report = LocalReport.load_pbix("example.pbix", kill_ssas_on_exit=True)
   col = report.ssas.columns.find({"explicit_name": "MeasureColumn"})
   col.get_lineage("parents").to_mermaid().show()


Improved Multilanguage Support
------------------------------

This example displays the ability to easily convert PBIX reports to alternate languages:

.. code-block:: python
   :linenos:

   from pbi_core import LocalReport

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

.. code-block:: python
   :linenos:

   from pbi_core import LocalReport

   report = LocalReport.load_pbix("example_pbis/api.pbix")
   report.cleanse_ssas_model()
   report.save_pbix("cull_out.pbix")
