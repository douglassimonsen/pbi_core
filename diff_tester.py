from pbi_core import LocalReport, git

start = LocalReport.load_pbix("example_pbis/git_differences/original.pbix", kill_ssas_on_exit=False)
end = LocalReport.load_pbix("example_pbis/git_differences/updated_measure_and_layout.pbix", kill_ssas_on_exit=False)

git.diff(start, end)