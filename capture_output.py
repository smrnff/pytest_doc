#
# You can influence output capturing mechanisms from the command line:
#
# pytest -s                  # disable all capturing
# pytest --capture=sys       # replace sys.stdout/stderr with in-mem files
# pytest --capture=fd        # also point filedescriptors 1 and 2 to temp file
# pytest --capture=tee-sys   # combines 'sys' and '-s', capturing sys.stdout/stderr
#                            # and passing it along to the actual sys.stdout/stderr
#


#
# Accessing captured output from a test function
#
# The capsys, capsysbinary, capfd, and capfdbinary fixtures allow access to stdout/stderr output created during
# test execution.
#

def test_myoutput(capsys):  # or use "capfd" for fd-level
    import sys
    print("hello")
    sys.stderr.write("world\n")
    captured = capsys.readouterr()
    assert captured.out == "hello\n"
    assert captured.err == "world\n"
    print("next")
    captured = capsys.readouterr()
    assert captured.out == "next\n"