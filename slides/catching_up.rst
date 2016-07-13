.. include:: ../../common/rst_defs.rst

Python Basic Recap
==================

Reminder of what we saw in "Python Basic" (up to and including 2016).

Covered Topics
--------------

* Python REPL, saving and running Python programs.
* Data Types (int, str, unicode, bytes, dicts, tuples, namedtuples, |ell|)
* Defining functions and classes.
* Packaging Python applications.
* DB connectivity with DBAPI2.
* Standard Library Overview.

Builtins and Library functions
------------------------------

* Imports
* reading/writing files
* Regular Expressions

Python Syntax Features
----------------------

* with-statement
* the "in" operator
* loops
* variable unpacking
* String Formatting


Not Covered in the old Course
=============================

A few things were not covered in "Python Basic" up to and including 2016. The
next few slides will cover these.


Variadic functions
------------------

* Functions can take both *positional* (``call(1, 2)``) and/or *keyword*
  (``call(a=10, b=20)``) arguments.
* It is possible to write variadic functions by adding ``*args`` and/or
  ``**kwargs`` in the function definition.

.. code-block:: python

    def print_args(a, b, *args, **kwargs):
        print("Type of args is:", type(args))
        print("Type of kwargs is:", type(kwargs))

        for arg in args:
            print(arg)

        for key, value in kwargs.items():
            print("kwargs[%r] = %r" % (key, value))

.. note::

    ``args`` and ``kwargs`` are just conventional variable names. You could use
    different names if you wish.


.. slide:: Exercise

    Write a function ``msum`` that takes any number of arguments, *and* any
    number of keyword arguments. It should return the sum of the arguments
    (positional and keyword). Use the *values* of the keyword arguments to
    calculate the sum::

        assert(msum(10) == 10)
        assert(msum(a=10) == 10)
        assert(msum() == 0)
        assert(msum(10, 30, a=11, b=12) == 63)


Argument Unpacking
------------------

Consider the following::

    def hello(a, b, c=0):
        pass

It is possible to call it in the following ways::

    data = [1, 2, 3]
    hello(*data)  # Equivalent to: hello(1, 2, 3)

    data2 = {'b': 10, 'c': 20}
    hello(1, **data2)  # Equivalent to: hello(1, c=20, b=10)


.. note::

    The second example shows that the arguments can be mixed.


Exercise: Delegator Function
----------------------------

Write a function ``mylog`` which takes one fixed argument: username. It should
also take any number of positional and keyword arguments.

Use this function to print the username, and then delegate the rest of the
arguments to :py:func:`logging.warning`.

The following call should work::

    mylog('malbert', 'This is the log message', exc_info=True)


Relative Imports
----------------

See also `PEP 328 <https://www.python.org/dev/peps/pep-0328/>`_

*Example*

.. code-block:: text
    :class: smaller

    myapp
    ├── __init__.py
    ├── sub1
    │   ├── __init__.py
    │   └── sub2
    │       ├── __init__.py
    │       ├── somemodule.py
    │       └── sys.py
    └── types.py

.. code-block:: python
    :caption: somemodule.py

    from .sys import hello_world
    from ...types import goodbye_world


.. rst-class:: smaller-slide

Running Modules with Relative Imports
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # python myapp/sub1/sub2/somemodule.py

    Traceback (most recent call last):
    File "/usr/lib/python2.7/runpy.py", line 174, in _run_module_as_main
        "__main__", fname, loader, pkg_name)
    File "/usr/lib/python2.7/runpy.py", line 72, in _run_code
        exec code in run_globals
    File "/tmp/myapp/sub1/sub2/somemodule.py", line 1, in <module>
        from .sys import hello_world
    ValueError: Attempted relative import in non-package

The following will work:

.. code-block:: text

    $ python -m myapp.sub1.sub2.somemodule

For details, see `PEP 366 <https://www.python.org/dev/peps/pep-0366/>`_
