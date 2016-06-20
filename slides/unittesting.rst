Unit Testing
============


Core Python
-----------

Unit testing is part of the standard library (in the ``unittest`` module). The
standard library also offers:

* Automated test discovery (The docs say Python 3.2+, but also works in 2.7)
* Conditional test skipping (f.ex.: only run tests on a specific hostname).
* mocking (via ``unittest.mock`` in Python3.3+)

Because it's Python, you can easily monkey-patch and fake/stub out existing
functions as well instead of mocking. Especially if you don't need the tracking
that is provided via mocks.

.. note::

    **Mocking in Python 2**

    The ``unittest.mock`` has been backported to Python 2 with the module
    ``mock`` which is available on pypi.


    **Auto-Discovery in Python 2**

    According to the official docs, auto-discovery has been added in Python
    3.2. However, it also works on 2.7 but the invocation is different. On
    Python 3.2+ it is sufficient to write::

        python -m unittest

    On Python 2.7 you have to write::

        python -m unittest discover


Mocks, Stubs and Fakes
----------------------

**stub**
    Something that provides predefined responses.

**fake**
    A custom implementation of a part of code you don't really want to execute.

**mock**
    Like a fake, but additionally tracks calls and can check execution
    expectations.


A simple Unit Test
------------------

.. code-block:: python
    :caption: Filename: test_example.py

    import unittest


    class ExampleTest(unittest.TestCase):

        def test_example_failure(self):
            self.assertEqual(1, 2)

        def test_example_pass(self):
            self. assertEqual(1, 1)


Run the test using::

    python -m unittest


Priming Tests / Fixtures
------------------------

* Override ``TestCase.setUp`` to prepare your environment.
* Override ``TestCase.tearDown`` to clean up your environment.

Example:

.. code-block:: python
    :class: smaller

    class ExampleTest(unittest.TestCase):

        def setUp(self):
            self.connection = open_connection()

        def tearTown(self):
            self.connection.close()

        def test_example(self):
            result = self.connection.get_ports()
            self.assertEqual(len(result), 123)


.. nextslide::
    :increment:

Other ways to setup your tests:

* ``setupClass``
* ``tearDownClass``
* ``setupModule``
* ``tearDownModule``

.. warning::

    Make sure both ``setUp`` and ``tearDown`` work properly. Otherwise all of
    your tests will return an ``Error`` instead of a ``Failure``.


Test Suites
-----------

From the docs:

    In most cases, calling unittest.main() will do the right thing and collect
    all the module’s test cases for you, and then execute them.

    However, should you want to customize the building of your test suite, you
    can do it yourself:

.. code-block:: python

    def suite():
        suite = unittest.TestSuite()
        suite.addTest(WidgetTestCase('test_default_size'))
        suite.addTest(WidgetTestCase('test_resize'))
        return suite


Assertion Methods
-----------------

The module contains a lot of assertion methods. They are separated into
multiple sections:

* `basic assertion methods <https://docs.python.org/3.4/library/unittest.html#assert-methods>`_
* `for warnings, exceptions and logging <https://docs.python.org/3.4/library/unittest.html#unittest.TestCase.assertRaises>`_
* `for inequalities and fuzzy matching <https://docs.python.org/3.4/library/unittest.html#unittest.TestCase.assertAlmostEqual>`_
* `for sequences <https://docs.python.org/3.4/library/unittest.html#unittest.TestCase.assertMultiLineEqual>`_


py.test
-------

* an alternative unit-testing framework
* highly popular
* third party plugins
* interesting due to the ``pytest-xdist`` plugin.

    * Main purpose: distributed test running
    * killer-feature: **automatically rerun failed tests**


py.test loop failures example
-----------------------------

.. code-block:: python
    :caption: mymoduletest.py
    :class: smaller

    import unittest
    from mymodule import func_1, func_2, func_3


    class TestPyTest(unittest.testCase):

        def test_func_1(self):
            result = func_1(1, 2)
            expected = 3
            self.assertEqual(result, expected)

        def test_func_2(self):
            result = func_2(1, 2)
            expected = 2
            self.assertEqual(result, expected)

        def test_func_3(self):
            result = func_3(1, 2)
            expected = -1
            self.assertEqual(result, expected)

.. nextslide::
    :increment:

.. code-block:: python
    :caption: mymodule.py

    def func_1(a, b):
        return a + b

    def func_2(a, b):
        return a * b

    def func_3(a, b):
        return a - b

**py.test execution**

::

    py.text -f mymoduletest.py


Mocking with ``unittest.mock``
------------------------------

Important classes/methods:

* :py:class:`unittest.mock.MagicMock`
* :py:func:`unittest.mock.patch`
* :py:func:`unittest.mock.create_autospec`

Official `Quick Guide <https://docs.python.org/3/library/unittest.mock.html#quick-guide>`_


Example Mocking
---------------

.. code-block:: python
    :caption: core.py

    import snmp


    def get_hostname(ip):
        return snmp.get(ip, '1.3.6.1.2.1.1.5.0')


Testing the above function has several challenges:

* Executing it will be slow (network access)
* The return value may be **out of your control**

    * Someone else may change the hosntame.
    * Security (SNMP credentials, firewall) considerations.


.. nextslide::
    :increment:


.. code-block:: python
    :caption: test_core.py

    from unittest.mock import patch
    import core

    ...

    def test_hostname(self):
        with patch('core.snmp') as mock_snmp:
            mock_snmp.get.return_value = 'myhostname'
            result = core.get_hostname('1.2.3.4')
        expected = 'myhostname'
        self.assertEqual(result, expected)

The above code demonstrates "monkey-patching" using the ``patch``
context-manager..

.. nextslide::
    :increment:

.. code-block:: python

    def test_failure(self):
        with patch('core.snmp') as mock_snmp:
            mock_snmp.get.side_effect = OSError
            result = core.get_hostname('1.2.3.4')
        expected = 'unknown'
        self.assertEqual(result, expected)

The above code demonstrates simulating exceptions using a ``Mock`` instance.


Faking/Stubbing
---------------

.. code-block:: python

    def my_stub(ip, oid):
        results = {
            '1.2.3': 123,
            '1.2.4': 0,
            '1.2.5': 'hello'
        }
        return results[oid]

    def test_stubbing(self):
        with patch('a.b.c') as mck_obj:
            mck_obj.amethod.side_effect = my_stub

            ...

Verifying Calls on a Mock Object
--------------------------------

Test for a single call::

    mock_instance.assert_called_with(1, 2, 3)

Test for multiple calls::

    mock_instance.assert_has_calls([
        call(1, 2, 3),
        call(2, 3, 4),
    ], any_order=False)


General Tips for Unit Testing
-----------------------------

* Set ``TestCase.maxDiff`` to ``None`` to disable summarizing diffs.
* Use a ``self.fail('TODO')`` as final instruction in a unit test to make use
  of the "loop on failing" feature of "py.test" while working on the test.
  Remove it when done
* Use a simplg ``raise`` statement inside your code to trigger failures to best
  utilize the "loop on failing" feature. Remove it when done.

.. nextslide::
    :increment:

* Try to use only one "assert" statement per test case.

    * Convert your real results to "testable" results by wrapping them in a
      simple structure like a dict or list.

* Use ``self.assertCountEqual`` to test contents of unsorted lists.
* Save test-data in external files to keep your unit tests as small and
  readable as possible.
