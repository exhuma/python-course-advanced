Higher Order Functions
======================

"Higher Order Functions" are functions that operate on functions. They can
either modify existing functions or generate new functions.

Example: Multiplicators
-----------------------

.. code-block:: python

    def multiplicator(n):
        """
        Create a function which multiplies a value by *n*.
        """
        def fun(m):
            return n*m
        return fun

    times2 = multiplicator(2)
    times3 = multiplicator(3)
    times2(2)
    times3(2)


Closures
--------

* The previous example is only possible because Python supports closures.
* A closure is a persistent local scope (It persists even after the function
  exits).
* In the previous example, the inner function ``fun`` keeps a reference to
  ``n`` even *after the call to multiplicator has returned*.
* If the reference to the inner function is lost/removed (f.ex. ``times2``),
  the closure is also lost.


Example: HTML Wrappers
----------------------

.. code-block:: python

    def wrapper(tag):
        """
        Create a new function that wraps a string in the HTML tag *tag*.
        """
        def wrap_text(innertext):
            return '<%s>%s</%s>' % (tag, innertext, tag)
        return wrap_text

    bold = wrapper('strong')
    emphasize = wrapper('em')
    heading1 = wrapper('h1')

    print(bold(emphasize('Hello')))


.. nextslide::

.. hint::

    * The ``multiplicator`` and ``wrapper`` example are very simple!
    * They can also be solved differently without difficulty.
    * The idea to take home is that you can write functions that create
      functions. *Even at runtime!*


Example: Timing Functions
-------------------------

.. code-block:: python
    :class: smaller

    from datetime import datetime

    def timed(f):
        "Add timing information to function f."
        def fun(*args, **kwargs):
            begin = datetime.now()
            result = f(*args, **kwargs)
            runtime = datetime.now() - begin
            print('Runtime of %s: %s' % (f, runtime))
            return result
        return fun

    def hello():
        """
        Prints "Hello World"
        """
        print("Hello World")

    timed_hello = timed(hello)

    hello()
    timed_hello()

But there's a problem
---------------------

.. code-block:: python

    >>> print(timed_hello.__doc__)
    >>> help(timed_hello)

Solution:

.. code-block:: python
    :class: smaller
    :emphasize-lines: 3, 8

    ...

    from functools import wraps

    ...

    def timed(f):
        @wraps(f)
        def fun(*args, **kwargs):
            ...
        return fun


Congratulations
---------------

You've written your first *decorator*.


.. figure:: _static/SuccessKid.jpg


Decorators
----------

* ``@``-syntax introduced in Python 2.4
* Convenient to *add* behaviour to a function or class (caching, logging,
  authentication, |ell|)

With the ``@``-syntax, the previous code can be rewritten as:

.. code-block:: python

    @timed
    def hello():
        print("Hello World!")


Parametrized Decorators
-----------------------

To create a parametrized decorator (a decorator which takes one or more
parameters), you have to write a function (or class) which *returns* a
decorator.

.. code-block:: python
    :emphasize-lines: 2-6

    def prefix_timed(prefix):
        def decorator(f):
            @wraps(f)
            def fun(*args, **kwargs):
                pass  # Implement the decorator
            return fun
        return decorator


Lambda Expressions in Python
----------------------------

* A lambda expression is a function with exactly one statement.
* In other words: Any function that has only one statement can be rewritten as
  lambda expression.
* A lambda expression implicitly/automatically returns the result of that one
  statement.
* A lambda expression has no name.


Lambda Expressions: Example
---------------------------

.. code-block:: python
    :class: smaller

    class Page:
        def __init__(self, title='untitled'):
            self.title = title
    data = [Page('b'), Page('c'), Page('a')]

    def my_sort_key(a):
        return a.title

    print(sorted(data, key=my_sort_key))

Can be rewritten as:

.. code-block:: python
    :class: smaller
    :emphasize-lines: 1-4

    class Page:
        def __init__(self, title='untitled'):
            self.title = title
    data = [Page('b'), Page('c'), Page('a')]

    print(sorted(data, key=lambda a: a.title))


Lambda Expressions: Different Example
-------------------------------------

.. code-block:: python
    :class: smaller

    def my_sort_key(a):
        return a.title

Can be rewritten as:

.. code-block:: python
    :class: smaller

    my_sort_key = lambda a: a.title

.. hint::

    This example does not make sense in production code. It is used to
    demonstrate lambda expressions and functions as first-class objects.
