#
# A skip means that you expect your test to pass only if some conditions are met, otherwise pytest should skip running
# the test altogether. Common examples are skipping windows-only examples on non-windows platforms, or skipping examples
# that depend on an external resource which is not available at the moment (for example a database).
#
# A xfail means that you expect a test to fail for some reason. A common example is a test for a feature
# not yet implemented, or a bug not yet fixed. When a test passes despite being expected to fail
# (marked with pytest.mark.xfail), it’s an xpass and will be reported in the test summary.
#
import pytest
import sys


@pytest.mark.skip(reason="no way of currently testing this")
def test_the_unknown():
    ...


#
# It is also possible to skip the whole module using pytest.skip(reason, allow_module_level=True) at the module level:
#
if not sys.platform.startswith("win"):
    pytest.skip("skipping windows-only examples", allow_module_level=True)


#
# If you wish to skip something conditionally then you can use skipif instead. Here is an example of marking a test
# function to be skipped when run on an interpreter earlier than Python3.6:
#

@pytest.mark.skipif(sys.version_info < (3, 6), reason="requires python3.6 or higher")
def test_function():
    ...


#
# Skip all test functions of a class or module
#
@pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows")
class TestPosixCalls:
    def test_function(self):
        "will not be setup or run under 'win32' platform"


#
# Here’s a quick guide on how to skip examples in a module in different situations:
#
# Skip all examples in a module unconditionally:
pytestmark = pytest.mark.skip("all examples still WIP")
# Skip all examples in a module based on some condition:
pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="examples for linux only")
# Skip all examples in a module if some import is missing:
pexpect = pytest.importorskip("pexpect")


#
# XFail: mark test functions as expected to fail
#
@pytest.mark.xfail
def test_function():
    ...


#
# condition parameter
# If a test is only expected to fail under a certain condition, you can pass that condition as the first parameter:
#
@pytest.mark.xfail(sys.platform == "win32", reason="bug in a 3rd party library")
def test_function():
    ...


#
# run parameter
# If a test should be marked as xfail and reported as such but should not be even executed,
# use the run parameter as False:
#
@pytest.mark.xfail(run=False)
def test_function():
    ...


#
# Skip/xfail with parametrize
#
# It is possible to apply markers like skip and xfail to individual test instances when using parametrize:
@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (1, 2),
        pytest.param(1, 0, marks=pytest.mark.xfail),
        pytest.param(1, 3, marks=pytest.mark.xfail(reason="some bug")),
        (2, 3),
        (3, 4),
        (4, 5),
        pytest.param(
            10, 11, marks=pytest.mark.skipif(sys.version_info >= (3, 0), reason="py2k")
        ),
    ],
)
def test_increment(n, expected):
    assert n + 1 == expected
