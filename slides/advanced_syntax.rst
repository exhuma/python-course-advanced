Syntax Features & Useful Builtins
=================================


List-Comprehensions
-------------------

List comprehensions are concise 1-line statements to create new collections.

.. code-block:: python

    iterable = [1, 2, 3, 4, 5]
    new_list = [x for x in iterable]

* Creates a *new* list from elements of the *iterable*.
* If *iterable* is a generator, this will consume the generator.
* Can be used to modify and filter out values from the iterable.
* Don't over-use. Sometimes a ``for`` loop is easier to read.

.. nextslide::
    :increment:

Applying a function to each item:

.. code-block:: python

    def modifier(x):
        return x * 2

    new_list = [modifier(x) for x in old_list]

Using :py:func:`map`:

.. code-block:: python

    new_list = map(modifier, old_list)

.. nextslide::
    :increment:

Filtering items from a list:

.. code-block:: python

    def is_valid(x):
        return x > 2

    new_list = [x for x in old_list if is_valid(x)]

Using :py:func:`filter`:

.. code-block:: python

    new_list = filter(is_valid, old_list)

.. nextslide::
    :increment:

Filtering & Mapping combined

.. code-block:: python

    def modifier(x):
        return x * 2

    def is_valid(x):
        return x > 2

    new_list = [modifier(x) for x in old_list if is_valid(x)]

Using :py:func:`map` & :py:func:`filter`:

.. code-block:: python

    new_list = map(modifier, filter(is_valid, old_list))


Other Comprehensions
~~~~~~~~~~~~~~~~~~~~

Comprehensions can also be used to create dictionaries, sets and generators
on-the-fly:

.. code-block:: python

    data = [
        ('x', 1),
        ('x', 1),
        ('y', 2),
    ]

    # Dictionary Comprehension
    dictionary = {key: value for key, value in data}

    # Set Comprehension
    unique_keys = {row[0] for row in data}

    # Generator Expression
    my_generator = (row for row in data)


zipping
-------

:py:func:`zip` and :py:func:`itertools.zip_longest` are *very* powerful utility
function. They take iterables and return a new iterable where each item is a
tuple consisting of the next item of each iterable.

* :py:func:`zip` stops once the first iterable is exhausted.
* :py:func:`itertools.zip_longest` fills in missing values with *fillvalue*

.. rst-class:: smaller-slide

zip Examples
~~~~~~~~~~~~

.. code-block:: python
    :class: smaller

    >>> from itertools import zip_longest
    >>> list_a = [1, 2, 3]
    >>> list_b = [5, 6, 7, 8]

    >>> zip(list_a, list_b)
    <zip object at 0x*******>

    >>> list(zip(list_a, list_b))
    [(1, 5), (2, 6), (3, 7)]

    >>> list(zip_longest(list_a, list_b))
    [(1, 5), (2, 6), (3, 7), (None, 8)]

    >>> list(zip_longest(list_a, list_b, fillvalue=0))
    [(1, 5), (2, 6), (3, 7), (0, 8)]

This also works with more than two iterables:

.. code-block:: python
    :class: smaller

    >>> list_a = [1, 2, 3]
    >>> list_b = [5, 6, 7]
    >>> list_c = ['a', 'b', 'c']
    >>> a, b, c = zip(list_a, list_b, list_c)

    >>> a, b, c
    ((1, 5, 'a'), (2, 6, 'b'), (3, 7, 'c'))


.. nextslide::
    :increment:

Using zip to "unzip"
~~~~~~~~~~~~~~~~~~~~

An implicit property of the zip algorith is that it can also be used to "unzip"
items. Consider the following two lists::

    [1, 2, 3]
    [5, 6, 7]

By zipping them we get these three tuples::

    (1, 5)
    (2, 6)
    (3, 7)

.. nextslide::
    :increment:

:py:func:`zip` can be used with multiple iterables. So we can use those three
tuples as input again::

    zip((1, 5), (2, 6), (3, 7))

This will yield the following two **tuples**::

    (1, 2, 3)
    (5, 6, 7)

This end result is almost identical to the original input! So we can write the
following:

``zip(*zip(a, b)) ≈ a, b``


"Practical" Example
~~~~~~~~~~~~~~~~~~~

Write a function ``parse`` which converts a key/value string into a dictionary.
Try to use ``zip``!

.. sidebar:: tip

    * Remember list "slicing" including "stepping"

.. code-block:: python

    >>> data = 'a 10 b 20 c 30'
    >>> parse(data)
    {'a': '10', 'b': '20', 'c': '30'}

|clear|

**Solution...**

.. code-block:: python
    :class: build

    >>> def parse(line):
    ...     items = line.split()
    ...     keys = items[::2]
    ...     values = items[1::2]
    ...     return dict(zip(keys, values))
