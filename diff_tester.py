import json
import pathlib
import zipfile

from pbi_core import LocalReport

start = LocalReport.load_pbix("example_pbis/differences/original.pbix", kill_ssas_on_exit=False)
start = LocalReport.load_pbix("example_pbis/differences/updated_measure_and_layout.pbix", kill_ssas_on_exit=False)
