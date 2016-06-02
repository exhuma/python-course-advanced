Python Object Model & Customisation
===================================

This section explains how Python sees and works with your own objects. It also
explains how you can add special behaviour to your objects by implementing
"magic" methods.


MRO and Multiple Inheritance
----------------------------

* Python guarantees a monotonic MRO for multiple inheritance.
* It relies on the order in which classes are *defined*: ``Foo(A, B)`` ≠
  ``Foo(B, A)``!
* It uses the `C3 linearisation Algorithm
  <https://en.wikipedia.org/wiki/C3_linearization>`_.
* `Python implementation of C3
  <https://www.python.org/download/releases/2.3/mro/>`_.

.. nextslide::
    :increment:

.. digraph:: inheritance

    A -> B [dir=back];
    A -> C [dir=back];
    B -> D [dir=back];
    C -> D [dir=back];

.. code-block:: python
    :class: rightcode

    class A:
        pass

    class B(A):
        pass

    class C(A):
        pass

    class D(B, C):
        pass

|clear|

.. sidebar:: Try changing parents of ``D``

    Note that the MRO depends on your class definition!

.. code-block:: python

    >>> print(D.mro())


Magic Methods
-------------

Reference: `Basic Customisation`_

* ``__str__``, ``__unicode__`` (Python 2 only), ``__bytes__`` (Python 3 Only)
* ``__repr__``
* ``__eq__``, ``__hash__``, ``__lt__``, ``__gt__`` |ell|
* ``__getattr__``, ``__getattribute__``, ``__setattr__``, ``__getitem__``,
  ``__contains__`` |ell|
* ``__slots__``

.. _Basic Customisation: https://docs.python.org/3/reference/datamodel.html#basic-customization

Magic Methods Example
---------------------

.. code-block:: python
    :emphasize-lines: 5-7, 9-11

    class MagicTestA:
        def __init__(self, foo):
            self.foo = foo

        def __str__(self):
            print('__str__ called')
            return self.foo

        def __repr__(self):
            print('__repr__ called')
            return 'MagicTestA(foo=%r)' % self.foo

        def __unicode__(self):
            print('__unicode__ called')
            return self.foo

        def __bytes__(self):
            print('__bytes__ called')
            return self.foo.encode('utf8')

.. sidebar:: Almost always useful
    :class: overlapping

    * ``__repr__``
    * ``__str__``

.. nextslide::

.. warning::

    For **Python2** you should implement both ``__str__`` and
    ``__unicode__``!


Testing Class Customisation
---------------------------

.. code-block:: python
    :caption: Before Adding __str__ and __repr__

    >>> instance = MagicTest('hello')
    >>> instance
    <__main__.MagicTest object at 0x7f34a465d518>
    >>> repr(a)
    '<__main__.MagicTest object at 0x7f34a465d518>'
    >>> print(instance)
    <__main__.MagicTest object at 0x7f34a465d518>
    >>> str(a)
    '<__main__.MagicTest object at 0x7f34a465d518>'
    >>> hex(id(instance))
    '0x7f34a465d518'
    >>> instance.__class__
    <class '__main__.MagicTest'>

.. nextslide::
    :increment:

.. code-block:: python
    :caption: After adding magic methods

    >>> instance = MagicTest('hello')
    >>> instance
    __repr__ called
    MagicTest(foo='hello')
    >>> print(instance)
    __str__ called
    Hello World!
    >>> hex(id(instance))
    '0x7f34a465d518'
    >>> instance.__class__
    <class '__main__.MagicTest'>

.. note::
    When converting the return value of ``id`` to base 16, you will get the
    same value as shown in the default ``repr`` return value. The simplest way
    of doing this is using the builtin :py:func:`hex`.


Magic Methods Example (ctd)
---------------------------

.. code-block:: python

    class MagicTestB:
        def __init__(self, foo):
            self.foo = foo

        def __eq__(self, other):
            print('__eq__ called')
            return other.foo == self.foo

        def __hash__(self):
            print('__hash__ called')
            return hash(('MagicTestB', self.foo))

        def __lt__(self, other):
            print('__lt__ called')
            return self.foo < other.foo

        def __gt__(self, other):
            print('__gt__ called')
            return self.foo > other.foo

.. nextslide::
    :increment:

.. code-block:: python

    class MagicTestC:

        def __getattr__(self, attribute_name):
            print('__getattr__ called')

        def __getattribute__(self, attribute_name):
            print('__getattribute__ called')

        def __setattr__(self, attribute_name, value):
            print('__setattr__ called')

        def __getitem__(self, key):
            print('__getitem__ called')

        def __contains__(self, key):
            print('__contains__ called')


Hashable Classes
----------------

The two most common reasons to implement ``__hash__`` are if you want instances
of your class to be |ell|

    * |ell| used as keys in dictionaries,
    * |ell| used as items in sets

All classes are hasheable by default, **unless** you define an ``__eq__``
method!

.. nextslide::
    :increment:

If Python needs to hash an instance of your custom class and it does *not*
implement ``__hash__`` you will see the following error:

.. code-block:: python
    :emphasize-lines: 8-10

    >>> class Foo:
    ...   def __eq__(self, other):
    ...     return True
    ...
    >>> x = Foo()
    >>> y = Foo()
    >>> {x, y}
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: unhashable type: 'Foo'

.. nextslide::
    :increment:

.. warning::

    The following rules are *not* enforced by Python. They don't need to be!

    But you can save yourself from some difficult to find bugs by following
    them:

    * If you define ``__hash__`` you **must** also define ``__eq__``.
    * |ell| but you can have ``__eq__`` without ``__hash__``.
    * Values used to compute the ``__hash__`` **must** be immutable!

    For more details, see the `official docs
    <https://docs.python.org/3/reference/datamodel.html#object.__hash__>`_.


Slots
-----

* By default Python allocates a new dictionary in each instance for attribute
  storage.
* This is wasteful if you have a *large* number of instances.
* ``__slots__`` reserves *just enough* space for selected attributes.

.. code-block:: python

    class Foo:
        __slots__ = 'a', 'b'

        def __init__(self, a, b):
            self.a = a
            self.b = b


Descriptors
-----------

Descriptors allow you to modify the behaviour of Python when instance members
are accessed, modified and/or deleted. Practical example (logging)::

    class LoggedValue:

        def __init__(self, value, name):
            self.value = value
            self.name = name

        def __get__(self, obj, type=None):
            LOG.debug('Accessing %s', self.name)
            return self.value

        def __set__(self, obj, value):
            LOG.debug('Setting %s to %r', self.name, value)
            self.value = value

.. nextslide::
    :increment:

Using the descriptor from the previous slide:

.. code-block:: python


    class A:
        foo = LoggedValue(234, 'foo')
        bar = LoggedValue(111, 'bar')


    inst = A()
    print(inst.foo)
    print(inst.bar)
    inst.bar = 100


Metaclasses
-----------

Metaclasses allow you to modify *how* a class is created.

.. code-block:: python

    class LoggingMeta(type):
        def __new__(cls, name, parents, dict_):
            new_cls = super(LoggingMeta, cls).__new__(
                cls, name, parents, dict_)
            for key, value in vars(new_cls).items():
                if key.startswith('_'):
                    continue
                setattr(new_cls, key, LoggedValue(value, key))
            return new_cls


    class A(metaclass=LoggingMeta):
        foo = 234
        bar = 111


.. vim: set spelllang=en_gb :
