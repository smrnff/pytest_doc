#
# The default base temporary directory
# Temporary directories are by default created as sub-directories of the system temporary directory.
# The base name will be pytest-NUM where NUM will be incremented with each test run. Moreover,
# entries older than 3 temporary directories will be removed.
#
# You can override the default temporary directory setting like this:
# pytest --basetemp=mydir
# When distributing examples on the local machine, pytest takes care to configure a basetemp directory for the
# sub processes such that all temporary data lands below a single per-test run basetemp directory.
#

# content of test_tmp_path.py

CONTENT = "content"


def test_create_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text(CONTENT)
    assert p.read_text() == CONTENT
    assert len(list(tmp_path.iterdir())) == 1
    assert 0

#
#
#


def test_create_file(tmpdir):
    p = tmpdir.mkdir("sub").join("hello.txt")
    p.write("content")
    assert p.read() == "content"
    assert len(tmpdir.listdir()) == 1
    assert 0