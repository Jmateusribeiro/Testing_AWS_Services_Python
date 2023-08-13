set dir=%CD%
set report_dir=%CD%\reports
set test_dir=%CD%\tests

echo The test directory is %test_dir%

python -m pytest -s -vv --gherkin-terminal-reporter %test_dir%\step_defs --html=%report_dir%\report.html -n 4 --capture sys

pause