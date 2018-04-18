Advanced Functions
==================


.. rst-class:: smaller-slide

Variadic Functions and Default Arguments
----------------------------------------

* Default arguments.
* ``*args`` and ``**kwargs`` allow for variadic functions.

.. code-block:: python

    from pprint import pprint

    def default_arg(name='<unknown>'):
        print('Hello %s' % name)

    def variadic_args(*args, **kwargs):
        pprint(locals())


.. tip::

    ``args`` and ``kwargs`` are only conventional names. Sometimes (but rarely)
    it may be useful to use other names.


Enforced Keyword Arguments
--------------------------

It is possible to *require* some arguments to be passed as keyword arguments:


.. code-block:: python

    import sys

    def say_hello(name, *, stream=sys.stdout):
        print(f'Hello {name}', file=stream)

    say_hello('John')
    say_hello('Jane', stream=sys.stderr)
    say_hello('Jane', sys.stderr)  # This will cause an error


.. rst-class:: smaller-slide


Type Hints
----------


Simple Type Hints
~~~~~~~~~~~~~~~~~

For details see :pep:`484`

Example:

.. code-block:: python

    def format_hello(name: str) -> str:
        return f'Hello {name}'


Benefits
~~~~~~~~

* Detection of errors before runtime (`mypy <http://mypy-lang.org>`_)
* Better documentation (`Sphinx <http://sphinx-doc.org>`_)
* Better tooling support (`PyCharm <https://www.jetbrains.com/pycharm>`_)


Challenges
~~~~~~~~~~

* Python is dynamically typed. Types can be created at run-time!

  * Annotating dynamic code is difficult
  * Checking runtime types is close to impossible

* Disagreement in the community
* Python 2 support



.. rst-class:: smaller-slide
The typing module
~~~~~~~~~~~~~~~~~

The :py:mod:`typing` module contains generic types to use with type hints. Example:


.. code-block:: python

    from typing import List, Set, TypeVar

    T = TypeVar('T')


    def process_elements(elements: List[str]) -> Set[int]:

        output = set()
        for element in elements:
            output.add(int(element))
        return output


    def fetch_element(elements: List[T]) -> T:
        return elements[0]


    if __name__ == '__main__':
        mylist = [1, 2, 3]
        element = fetch_element(mylist)
        print(element.upper())


Checking Type Hints
~~~~~~~~~~~~~~~~~~~

Checking types is *optional* in Python. It is **not enforced** by the Python
runtime. Instead, separate tools may use these hints for useful information.

PyCharm already supports type hints for quite some time and uses them for more
helpful auto-completions.

Additionally, the tool `mypy <http://mypy-lang.org>`_ can be used to check a
project for type correctness:

.. code-block:: shell

    $ mypy checked.py
    checked.py:21: error: "int" has no attribute "upper"

    $ mypy -p package  # Recursively checks files in <package>.
    $ mypy -m module  # Checks <module> and everything imported in it.


Type Checking Legacy Code
~~~~~~~~~~~~~~~~~~~~~~~~~

mypy has support for "stub" files (``.pyi``). These files a *very* similar to a
C header file. They only contain function signatures without body.

* mypy first looks for stub files.
* If found they are used for type hints instead of the ``.py`` file.
* Can be used to add type-checks to third-party modules without type hints.
* `typeshed <https://github.com/python/typeshed>`_ contains some stub files for
  popular projects and is bundled with ``mypy`` (this is still very much work
  in progress).


mypy difficulties
~~~~~~~~~~~~~~~~~

* mypy has its own search path to find Python source files (non-trivial with
  virtual environments).
* Dependencies to Python source which has no type-annotations
* Following imports not found on the mypy search path



Functions as Objects
--------------------

Because functions are objects, they can be assigned to variables. For example
as values in a dictionary::

    def case_1():
        print("Hello 1")

    def case_2():
        print("Hello 2")

    cases = {
        1: case_1,
        2: case_2,
    }

    user_selection = int(input('Type a number: '))

    function = cases.get(user_selection, lambda: print("unknown case"))
    function()

.. note::

    Python has no ``case`` or ``switch`` statement. Using functions as values
    in dictionaries, lets you have a very similar code structure. As a
    side-effect, this will give you functions for each switched case, which
    makes unit-testing easier.
