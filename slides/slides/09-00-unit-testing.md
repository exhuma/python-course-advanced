# Unit Testing

^

## Core Python

* Part of the standard library
* Test Discovery & Execution
* Mocking, Faking & Monkey-Patching

Note:

Unit testing is part of the standard library (in the ``unittest`` module). The
standard library also offers:

* Automated test discovery (As of Python 3.2+)
* Conditional test skipping (f.ex.: only run tests on a specific hostname).
* mocking (via ``unittest.mock`` in Python3.3+)

Because it's Python, you can easily monkey-patch and fake/stub out existing
functions as well instead of mocking.

^

## Mocks, Stubs and Fakes

<dl>
    <dt>stub</dt>
    <dd>Something that provides predefined responses.</dd>
    <dt>fake</dt>
    <dd>A custom implementation of a part of code you don't really want to execute.</dd>
    <dt>mock</dt>
    <dd>Like a fake, but additionally tracks calls and can check execution expectations.</dd>
</dl>

Note:

See: https://martinfowler.com/articles/mocksArentStubs.html

^

## Simple Unit Test

```py
import unittest

class ExampleTest(unittest.TestCase):

    def test_example_failure(self):
        self.assertEqual(1, 2)

    def test_example_pass(self):
        self.assertEqual(1, 1)
```
<!-- .element: data-caption="Filename: test_example.py" -->

Run the test using:

```
python -m unittest
```

^

## Priming Tests / Fixtures

* Override ``TestCase.setUp`` to prepare your environment.
* Override ``TestCase.tearDown`` to clean up your environment.

^

```py
class ExampleTest(unittest.TestCase):

    def setUp(self):
        self.connection = open_connection()

    def tearTown(self):
        self.connection.close()

    def test_example(self):
        result = self.connection.get_ports()
        self.assertEqual(len(result), 123)
```

Note:

Other ways to setup your tests:

* ``setUpClass``  *(must be a class-method)*
* ``tearDownClass``  *(must be a class-method)*
* ``setUpModule``
* ``tearDownModule``

Make sure both ``setUp`` and ``tearDown`` work properly. Otherwise all of
your tests will return an ``Error`` instead of a ``Failure``.
<!-- .element: class="admonition warning" -->

When an error occurs in ``setUp``, ``tearDown`` will not be called and may lead
to resource leaks. To avoid this, consider using `unittest.TestCase.addCleanup`
to clean-up resources.
<!-- .element: class="admonition tip" -->

^

## Test Suites

From the docs:

<div class="text">
In most cases, calling unittest.main() will do the right thing and collect
all the module’s test cases for you, and then execute them.

However, should you want to customize the building of your test suite, you
can do it yourself:
</div>

```py
def suite():
    suite = unittest.TestSuite()
    suite.addTest(WidgetTestCase('test_default_size'))
    suite.addTest(WidgetTestCase('test_resize'))
    return suite
```

Note:

## Assertion Methods

The module contains a lot of assertion methods. They are separated into
multiple sections:

* [basic assertion methods](https://docs.python.org/3.4/library/unittest.html#assert-methods)
* [for warnings, exceptions and logging](https://docs.python.org/3.4/library/unittest.html#unittest.TestCase.assertRaises)
* [for inequalities and fuzzy matching](https://docs.python.org/3.4/library/unittest.html#unittest.TestCase.assertAlmostEqual)
* [for sequences](https://docs.python.org/3.4/library/unittest.html#unittest.TestCase.assertMultiLineEqual)

^

## py.test

* an alternative unit-testing framework
* very popular
* third party plugins
* simplified test-definition

^

# Mocking

^

Important classes/methods:

* `unittest.mock.MagicMock`
* `unittest.mock.patch`
* `unittest.mock.create_autospec`

Official [Quick Guide](https://docs.python.org/3/library/unittest.mock.html#quick-guide)

^

## Example Mocking

```py
import snmp

def get_hostname(ip):
    return snmp.get(ip, '1.3.6.1.2.1.1.5.0').strip()
```
<!-- .element: data-caption="core.py" -->

Note:

Testing the function has several challenges:

* Executing it will be slow (network access)
* The return value may be **out of your control**

    * Someone may change the hostname on the remote device.
    * Security (SNMP credentials, firewall) considerations.

^

"monkey-patching" using the ``patch`` context-manager

```py
from unittest.mock import patch
import core

...

def test_hostname(self):
    with patch('core.snmp') as mock_snmp:
        mock_snmp.get.return_value = 'myhostname   '
        result = core.get_hostname('1.2.3.4')
    expected = 'myhostname'
    self.assertEqual(result, expected)
```
<!-- .element: data-cation="test_core.py" -->

^

Simulating exceptions using a ``Mock`` instance

```py
def test_failure(self):
    with patch('core.snmp') as mock_snmp:
        mock_snmp.get.side_effect = OSError
        result = core.get_hostname('1.2.3.4')
    expected = 'unknown'
    self.assertEqual(result, expected)
```

Note:

The argument to `unittest.mock.patch` represents the "import name" *relative to
the test-case module*!
<!-- .element: class="admonition warning" -->

For example, consider the following module:

```py
from telnetlib import Telnet
connection = Telnet(...)
```
<!-- .element: data-caption="core.py" -->

In this case the name used for patching is ``core.Telnet``. **NOT**
``telnetlib.Telnet``!

^

Faking/Stubbing
---------------

* Replace code with a simple implementation
* Replacement is functional code
* Not representative of production code
* Useful for execution speed & determinism

Note:

"faking" and "stubbing" is the process of replacing an existing function with a
non-production ready replacement. That replacement returns predictable results
in the context of a test.

The difference between a "fake" and a "stub" is the degree by how *far* they are
implemented.

You can monkey-patch with standard Python, but that will not provide
call-tracing. Using `unittest.mock` will give you call tracing for free.

To replace a mocked function with a custom function, you assign that function
to the mock ``side_effect``.

^

```py
def my_stub(ip, oid):
    results = {
        '1.2.3': 123,
        '1.2.4': 0,
        '1.2.5': 'hello'
    }
    return results[oid]

def test_stubbing(self):
    with patch('core.snmp') as mck_obj:
        mck_obj.get.side_effect = my_stub

        ...
```

^

## Faking Any Class

``MagicMock`` and ``create_autospec`` allow you to create a "magic" instance
which accepts any calls. This can be quite handy for DI/IOC.

```py
def test_interfaces(self):
    from mymodel import get_interfaces
    fake_device = object()
    fake_device.ip = '192.168.0.100'
    mocked_snmp = MagicMock()
    mocked_snmp.walk.return_value = [1, 2, 3]
    result = get_interfaces(mocked_snmp, fake_device)
    mocked_snmp.walk.assert_called_with(
        '192.168.0.100', '1.3.6.1.2.1.2.2'
    )
    # ... and verify the contents of "result"
```

^

## Verifying Calls on a Mock Object

Test for a single call:

```py
mock_instance.assert_called_with(1, 2, 3)
```

Test for multiple calls:

```py
mock_instance.assert_has_calls(
    [call(1, 2, 3), call(2, 3, 4)],
    any_order=False
)
```
