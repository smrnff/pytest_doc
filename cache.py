#
# Cache: working with cross-testrun state
#
# The plugin provides two command line options to rerun failures from the last pytest invocation:
# --lf, --last-failed - to only re-run the failures.
# --ff, --failed-first - to run the failures first and then the rest of the tests.
# For cleanup (usually not needed), a --cache-clear option allows to remove all cross-session cache contents
# ahead of a test run.
#
