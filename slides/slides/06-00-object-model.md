## Python Object Model & Customisation

Note:

This section explains how Python sees and works with your own objects. It also
explains how you can add special behaviour to your objects by implementing
"magic" methods.

---

## MRO and Multiple Inheritance

* Monotonic MRO for multiple inheritance.
* Parent class ordering matters.
* C3 linearisation Algorithm.

Note:

The method resolution order (MRO) is always the same in Python. This makes
multiple inheritance predictable and stable.

For this, it relies on the order in which classes are *defined:* ``class Foo(A, B)`` ≠ ``class Foo(B, A)``!

Internally it uses the [C3 linearisation
Algorithm](https://en.wikipedia.org/wiki/C3_linearization) ([Python
implementation](https://www.python.org/download/releases/2.3/mro/)).

^

## Example

<div class="mermaid">
    <pre>
        %%{init: {'theme': 'dark', 'themeVariables': { 'darkMode': true }}}%%
        flowchart TD
        A --> B;
        A --> C;
        B --> D;
        C --> D;
    </pre>
</div>

```py
class A:
    pass

class B(A):
    pass

class C(A):
    pass

class D(B, C):
    pass
```
<!-- .element: data-caption="Python Implementation" -->

Note:

The MRO can be displayed using:

```py
>>> print(D.mro())
```

---

## Magic Methods

Reference: [Basic Customisation](https://docs.python.org/3/reference/datamodel.html#basic-customization)

Note:

* ``__str__``, ``__unicode__`` (Python 2 only), ``__bytes__`` (Python 3 Only)
* ``__repr__``
* ``__eq__``, ``__hash__``, ``__lt__``, ``__gt__`` |ell|
* ``__getattr__``, ``__getattribute__``, ``__setattr__``, ``__getitem__``,
  ``__contains__`` |ell|
* ``__slots__``

* ``__getattr__`` gets only called if ``__getattribute__`` does not find anythng.
* ``__getattribute__`` gets called unconditionally but is more error-prone
    (risk of endless loop if not careful).

---

## Magic Methods Example

```py
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
```
<!-- .element: data-line-numbers="5-7, 9-11" -->

Note:

As other languages provide "to-string" conversions, Python offers more than one:

* ``__str__``: Converts to a string. The intended audience is end-users.
* ``__repr__``: Converts to a string. The intended audience are developers.

An alternative perspecive is that `__str__` contains less information than
`__repr__`. So it is easier to embed in display-strings. This may still be
useful for developers.

For **Python2** you should implement both ``__str__`` and
``__unicode__``!
<!-- .element: class="admonition warning" -->

^

## Testing Class Customisation

```py
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
```
<!-- .element: data-caption="Before Adding __str__ and __repr__" -->

^

```py
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
```
<!-- .element: data-caption="After adding magic methods" -->


Note:

When converting the return value of ``id`` to base 16, you will get the
same value as shown in the default ``repr`` return value. The simplest way
of doing this is using the builtin :py:func:`hex`.

^

## Magic Methods Example (ctd)

```py
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
```

^

```py
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
```

^

## Hashable Classes

* Classes must be hashable for some use-cases
* Custom classes are *not* hashable by default when `__eq__` is defined

Note:

The two most common reasons to implement ``__hash__`` are:

* ... you want to use instances of your class as keys in dictionaries,
* ... you want to use instances of your class in sets.

All classes are hasheable by default, **unless** you define an ``__eq__``
method! The default implementation will have a different hash value for each
instance, even if the member values are identical.

^

```py
>>> class Foo:
...
...     def __init__(self, name):
...         self.name = name
...
>>> x = Foo('John')
>>> y = Foo('John')
>>> users = {x, y}
>>> len(users)
2
```

… probably not what we want?

^

```py
>>> class Foo:
...
...     def __init__(self, name):
...         self.name = name
...
...     def __eq__(self, other):
...         return self.name == other.name
...
...     def __hash__(self):
...         return hash(self.name)
...
>>> x = Foo('John')
>>> y = Foo('John')
>>> users = {x, y}
>>> len(users)
1
```

Note:

If Python needs to hash an instance of your custom class and it does *not*
implement ``__hash__`` you will see the following error:

```py
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
```

<div class="admonition warning">
The following rules are <em>not</em> enforced by Python. They don't need to be!

But you can save yourself from some difficult to find bugs by following
them:

* If you define ``__hash__`` you **must** also define ``__eq__``.
* |ell| but you can have ``__eq__`` without ``__hash__``.
* Values used to compute the ``__hash__`` **must** be immutable!

For more details, see the [official docs](https://docs.python.org/3/reference/datamodel.html#object.__hash__).
</div>

^

## Slots

* Considerably lower memory footprint
* Limits flexibility of instances

Note:

* By default Python allocates a new dictionary in each instance for attribute
  storage.
* This is wasteful if you have a *large* number of instances.
* ``__slots__`` reserves *just enough* space for selected attributes.


```py
class Foo:
    __slots__ = 'a', 'b'

    def __init__(self, a, b):
        self.a = a
        self.b = b
```

---

## Descriptors

Descriptors allow you to modify the behaviour of Python when instance members
are accessed, modified and/or deleted.

^

Practical example (logging):

```py
import logging

LOG = logging.getLogger(__name__)

class LoggedValue:

    def __init__(self, value, name):
        self.value = value
        self.name = name

    def __get__(self, obj, type=None):
        LOG.debug('Accessing %s', self.name)
        return self.value

    def __set__(self, obj, value):
        LOG.debug('Setting %s on %r to %r', self.name, obj, value)
        self.value = value
```

^

Using the descriptor from the previous slide:

```py
class A:
    foo = LoggedValue(234, 'foo')
    bar = LoggedValue(111, 'bar')

    def __init__(self, foo, bar):
        self.foo = foo
        self.bar = bar

inst = A(10, 20)
print(inst.foo)
print(inst.bar)
inst.bar = 100
```

Note:

Descriptors have to be set on a *class*, not an *instance*

---

## Metaclasses

Metaclasses allow you to modify *how* a class is created.

```py
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
```
