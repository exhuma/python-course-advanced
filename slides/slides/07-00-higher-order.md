# Higher Order Functions

"Higher Order Functions" are functions that operate on functions. They can
either modify existing functions or generate new functions.

---

## Example: Multiplicators

```py
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
```

^

## Closures

* Persistent local scope
* Remains after function has returned
* Variables are "frozen" inside the closue

Note:

The previous example is only possible because Python supports closures.

A closure is a persistent local scope (It persists even after the function
exits/returns).

In the previous example, the inner function ``fun`` keeps a reference to ``n``
even *after the call to multiplicator has returned*.

If the reference to the inner function is lost/removed (f.ex. ``times2``), the
closure is also lost.

^

## Example: HTML Wrappers

```py
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
```

^

## Summary

* Higher order functions let you dynamically create or modify functions.
* Useful to refactor multiple *very* similar pieces of code, which would
  otherwise not be possible to refactor.

Note:

* The ``multiplicator`` and ``wrapper`` example are very simple!
* They can also be solved differently without difficulty.
* The idea to take home is that you can write functions that
  create functions. *Even at runtime!*

^

## Example: Timing Functions

```py
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
```

Note:

* The "timed" function takes another function ``f`` as argument.
* It defines a new function with variadic arguments (remember the earlier
  slides).
* Inside that function, it calls ``f`` by delegating all arguments to it.
* This can be used to do |ell| "stuff" before and/or after calling ``f``.
* |ell| and/or modify arguments.

## But there's a problem

```py
>>> print(timed_hello.__doc__)
>>> help(timed_hello)
```

## Solution

```py
...

from functools import wraps

...

def timed(f):
    @wraps(f)
    def fun(*args, **kwargs):
        ...
    return fun
```

^

## Congratulations

You've written your first *decorator*.

^

## Decorators

* ``@``-syntax introduced in Python 2.4
* Convenient to *add* behaviour to a function or class (caching, logging,
  authentication, ...)

^

With the ``@``-syntax, the previous code can be rewritten as:

```py
@timed
def hello():
    print("Hello World!")
```

Is equivalent to:

```py
def hello():
    print("Hello World!")
hello = timed(hello)
```

^

## Parametrized Decorators

To create a parametrized decorator (a decorator which takes one or more
parameters), you have to write a function (or class) which *returns* a
decorator.

^

```py
def prefix_timed(prefix):
    def decorator(f):
        @wraps(f)
        def fun(*args, **kwargs):
            pass  # Implement the decorator
        return fun
    return decorator
```

^

## Lambda Expressions in Python

* A lambda expression is a function with exactly one statement.
* In other words: Any function that has only one statement can be rewritten as
  lambda expression.
* A lambda expression implicitly/automatically returns the result of that one
  statement.
* A lambda expression has no name.

^

## Lambda Expressions: Example

```py
class Page:
    def __init__(self, title='untitled'):
        self.title = title
data = [Page('b'), Page('c'), Page('a')]

def my_sort_key(a):
    return a.title

print(sorted(data, key=my_sort_key))
```
<!-- .element: class="smallcode" -->

Can be rewritten as:

```py
class Page:
    def __init__(self, title='untitled'):
        self.title = title
data = [Page('b'), Page('c'), Page('a')]

print(sorted(data, key=lambda a: a.title))
```
<!-- .element: class="smallcode" -->

^

## Lambda Expressions: Different Example

```py
def my_sort_key(a):
    return a.title
```

Can be rewritten as:

```py
my_sort_key = lambda a: a.title
```

Note:

This example does not make sense in production code. It is used to
demonstrate lambda expressions and functions as first-class objects.
