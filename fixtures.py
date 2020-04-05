import pytest
import smtplib
import contextlib
import os


#
# Example of fixture usage
#
@pytest.fixture
def smtp_connection():
    return smtplib.SMTP("smtp.gmail.com", 587, timeout=5)


def test_smth(smtp_connection):
    response, msg = smtp_connection.ehlo()
    assert response == 250

#
# conftest.py: sharing fixture functions
#

#
# Sharing test data
# If you want to make test data from files available to your examples, a good way to do this is by loading these data in
# a fixture for use by your examples. This makes use of the automatic caching mechanisms of pytest.
# Another good approach is by adding the data files in the examples folder. There are also community plugins available to
# help managing this aspect of testing, e.g. pytest-datadir and pytest-datafiles.
#

#
# Extending the previous example, we can add a scope="module" parameter to the @pytest.fixture invocation to cause
# the decorated smtp_connection fixture function to only be invoked once per test module (the default is to invoke
# once per test function).
# Possible values for scope are: function, class, module, package or session.
#


@pytest.fixture(scope="module")
def smtp_connection():
    return smtplib.SMTP("smtp.gmail.com", 587, timeout=5)


#
# Fixture finalization / executing teardown code
#

@pytest.fixture(scope="module")
def smtp_connection():
    smtp_connection = smtplib.SMTP("smtp.gmail.com", 587, timeout=5)
    yield smtp_connection  # provide the fixture value
    print("teardown smtp")
    smtp_connection.close()


@pytest.fixture(scope="module")
def smtp_connection():
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=5) as smtp_connection:
        yield smtp_connection  # provide the fixture value


#
# Using the contextlib.ExitStack context manager finalizers will always be called regardless if the fixture setup code
# raises an exception. This is handy to properly close all resources created by a fixture even if one of them fails
# to be created/acquired:
#

@contextlib.contextmanager
def connect(port):
    ...  # create connection
    yield
    ...  # close connection


@pytest.fixture
def equipments():
    with contextlib.ExitStack() as stack:
        yield [stack.enter_context(connect(port)) for port in ("C1", "C3", "C28")]


#
# Factories as fixtures
# The “factory as fixture” pattern can help in situations where the result of a fixture is needed multiple times in a
# single test. Instead of returning data directly, the fixture instead returns a function which generates the data.
# This function can then be called multiple times in the test.
#

@pytest.fixture
def make_customer_record():
    def _make_customer_record(name):
        return {"name": name, "orders": []}

    return _make_customer_record


#
# Parametrizing fixtures
#

@pytest.fixture(scope="module", params=["smtp.gmail.com", "mail.python.org"])
def smtp_connection(request):
    smtp_connection = smtplib.SMTP(request.param, 587, timeout=5)
    yield smtp_connection
    print("finalizing {}".format(smtp_connection))
    smtp_connection.close()


#
# Using fixtures from classes, modules or projects
#
# Due to the usefixtures marker, the cleandir fixture will be required for the execution of each test method,
# just as if you specified a “cleandir” function argument to each of them.
#

@pytest.mark.usefixtures("cleandir")
class TestDirectoryInit:
    def test_cwd_starts_empty(self):
        assert os.listdir(os.getcwd()) == []
        with open("myfile", "w") as f:
            f.write("hello")

    def test_cwd_again_starts_empty(self):
        assert os.listdir(os.getcwd()) == []


# You can specify multiple fixtures like this
@pytest.mark.usefixtures("cleandir", "anotherfixture")
def test():
    ...


#
# Autouse fixtures
#
# The class-level transact fixture is marked with autouse=true which implies that all test methods in the class
# will use this fixture without a need to state it in the test function signature or with a class-level
# usefixtures decorator.
#

class TestClass:
    @pytest.fixture(autouse=True)
    def transact(self, request, db):
        db.begin(request.function.__name__)
        yield
        db.rollback()

    def test_method1(self, db):
        assert db.intransaction == ["test_method1"]

    def test_method2(self, db):
        assert db.intransaction == ["test_method2"]