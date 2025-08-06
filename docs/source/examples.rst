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