set dir=%CD%
set report_dir=%CD%\reports
set test_dir=%CD%\tests

echo The test directory is %test_dir%

python -m pytest --gherkin-terminal-reporter -s -vv --html=%report_dir%\report.html --capture=tee-sys %test_dir%\step_defs

pause