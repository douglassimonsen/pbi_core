Examples
========

This basic example tests that your PowerBI report can be parsed and reassembled by ``pbi_core``:

.. code-block:: python
   :linenos:

   from pbi_core import LocalReport

   report = LocalReport.load_pbix("example.pbix")
   report.save_pbix("example_out.pbix")


This example shows how you can add automatic descriptions to PowerBI columns (possibly from some governance tool??)

.. code-block:: python
   :linenos:

   from pbi_core import LocalReport

   report = LocalReport.load_pbix("example.pbix")
   for column in report.ssas.columns:
      column.description = "pbi_core has touched this"
      column.alter()

   report.save_pbix("example_out.pbix")


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
   values3 = measure.data(column, 10)
   print(values3)


This example displays a lineage chart in HTML:

.. code-block:: python
   :linenos:

   from pbi_core import LocalReport

   report = LocalReport.load_pbix("example.pbix", kill_ssas_on_exit=True)
   col = report.ssas.columns.find({"explicit_name": "MeasureColumn"})
   col.get_lineage("parents").to_mermaid().show()
