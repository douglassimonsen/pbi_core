.. Pbyx documentation master file, created by
   sphinx-quickstart on Tue Sep 17 19:38:43 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. |check| raw:: html

    <input checked="" disabled="" type="checkbox">

.. |uncheck| raw:: html

    <input disabled="" type="checkbox">

Pbyx documentation
==================

Goals of this package:

- |uncheck| Data/Visual Lineage Tool
   - |check| Low-level SSAS interface for updating PBIX Data Models
   - |check| Low-level interface for updating Static PBIX elements
   - |check| Intra-SSAS lineage
   - |check| Intra-layout lineage
   - |check| Layout-SSAS lineage
- |check| AST parser for DAX Queries
- |check| AST parser for M Queries
- |uncheck| Automatic Data Refresh
   - |uncheck| with Desktop PBIX SSAS
   - |uncheck| with self-created SSAS
- |check| Automated Data Extraction
   - |check| At the Column Level
   - |check| At the Table Level
   - |check| At the Measure Level
   - |check| At the Visual Level
- |uncheck| Automated Performance Testing
   - |uncheck| At the Column Level
   - |uncheck| At the Table Level
   - |uncheck| At the Measure Level
   - |uncheck| At the Visual Level
- |uncheck| Linting Tools
   - |uncheck| Layout stylistic Linting
   - |uncheck| DAX Formatter
   - |uncheck| DAX Linting
   - |uncheck| M Query Linting
- |uncheck| Remote PowerBI Manipulation
   - |uncheck| Incorporating REST API lib
   - |uncheck| Include non-REST endpoints
   - |uncheck| Report Deployment
   - |uncheck| Report Download
   - |uncheck| Viewship, etc. statistics
- |uncheck| Built-In Data Export Options
   - |uncheck| To Postgres
   - |uncheck| To SQLite
   - |uncheck| To CSVs

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   examples
   layout_api
   ssas_api

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`