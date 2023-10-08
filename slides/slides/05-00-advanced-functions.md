# Advanced Functions

---

## Default Arguments

* Functions may define default values
* And argument with a default can be omitted on call

```py
def default_arg(name="<unknown>"):
    print(f"Hello {name}")
```

Note:

## Danger Zone

Using mutable objects as default value is very dangerous and must be avoided.

<!-- .element: class="admonition warning" -->

```py
def unexpected_output(my_argument=[]):
    my_argument.append(1)
    print(my_argument)
```

---

## Variadic Functions

* Functions accept any number of arguments
* Either positional, keyword or both

```py
def variadic_args(*args, **kwargs):
    for i, arg in enumerate(args):
        print(f"Positional argument #{i}: {arg}")
    print(f"Argument with name 'foo': {kwargs['foo']}")
```

Notes:

<div class="admonition tip">
The `args` and `kwargs` are only conventional names. Sometimes (but rarely)
it may be useful to use other names.
</div>

---

## Call Delegation

```py
import logging

def anonymise_log(message, *args, **kwargs):
    message = remove_ips(message)
    logging.log(message, *args, **kwargs)


anonymise_log('Hello World')
anonymise_log('Hello World', level=logging.DEBUG)
anonymise_log('Hello World', exc_info=True)
```
<!-- .element: data-caption="Using variadic arguments to delegate calls to another function" -->

Note:

This functions shows how to define a function that passes all arguments down to
another function. By using variadic arguments, this function will always accept
the arguments of the "downstream" function. Even when it changes.

This is not without downsides though. Our "wrapper" function does not know
anything about the downstream function. And code editors will not be able to
"look into" the downstream function either. As a result, code-completion in
editors loses its usefulness.

---


## Enforced Keyword Arguments

It is possible to *require* some arguments to be passed as keyword arguments.
This is done by separating normal arguments from keyword arguments with a
single ``*``:


```py
import sys

def say_hello(name, *, stream=sys.stdout):
    print(f'Hello {name}', file=stream)

say_hello('John')
say_hello('Jane', stream=sys.stderr)
say_hello('Jane', sys.stderr)  # This will cause an error
```

---

## Functions as Objects

Functions are objects. They can be assigned to variables. For example as values
in a dictionary:

```py
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
```

---

## functools

[`functools`](py3_functools) contains a couple of very interesting helpers to work with
functions:

* `functools.partial`
* `functools.lru_cache`
* `functools.singledispatch`

Note:

* `functools.partial` -- Returns a new function which "freezes" some
  arguments of the original function (similar to "currying")
* `functools.lru_cache` -- Implementation of a "Least Recently Used" cache
* `functools.singledispatch` -- Helper to dispatch calls to other functions
  depending on type.

[py3_functools]: https://docs.python.org/3/library/functools.html

^

## functools.partial

```py
from functools import partial

def say_hello(greeting, name):
    print(f'{greeting} {name}')

hello = partial(say_hello, greeting='Hello')

hello('John')
```
<!-- .element: data-caption="Implementation" -->

```
Hello John
```
<!-- .element: data-caption="Output" -->


^

## functools.lru_cache

```py
from datetime import datetime
from functools import lru_cache
from time import sleep

@lru_cache(10)
def slow_function(n):
    sleep(5)
    return n * 2

print(datetime.now(), 'start')
print(datetime.now(), slow_function(1))
print(datetime.now(), slow_function(1))
print(datetime.now(), slow_function(2))
print(datetime.now(), 'end')
```
<!-- .element: data-caption="Implementation" -->

```
2018-04-18 07:47:20.506880 start
2018-04-18 07:47:20.506907 2
2018-04-18 07:47:25.512025 2
2018-04-18 07:47:25.512044 4
2018-04-18 07:47:30.515630 end
```
<!-- .element: data-caption="Output" -->

^

## functools.singledispatch

```py
from functools import singledispatch

@singledispatch
def process(value):
    print('<unknown>', value)

@process.register(int)
def process_numeric(value):
    print('Calling with numeric value', value * 2)

@process.register(str)
def process_string(value):
    print('Calling with text', value * 2)

process(1)
process('This is some Text')
process(1.1)
```
<!-- .element: data-caption="Implementation" class="smallcode" -->


```text
Calling with numeric value 2
Calling with text This is some TextThis is some Text
<unknown> 1.1
```
<!-- .element: data-caption="Output" -->

---

# Type Hints

^

## Simple Type Hints

For details see [PEP-484](https://peps.python.org/pep-0484/)

```py
def format_hello(name: str) -> str:
    return f'Hello {name}'
```

^

## Benefits

* Detection of errors before runtime ([mypy](http://mypy-lang.org))
* Better documentation ([Sphinx](http://sphinx-doc.org))
* Better tooling support (Code Editors)

^

## Challenges

* Python is dynamic
* Runtime types

Note:

Very advanced Python code may create types during runtime. These types often
depend on user input or config-files. It is impossible for static checkers to
deal with those situations. There is helpful support in Python for such cases
(for example "Protocols"). But getting this right is difficult.

^

## The typing module

The `typing` module contains generic types to use with type hints. Example:


```py
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
```
<!-- .element: class="smallcode" -->


^

## Checking Type Hints

* Optional
* Code runs even with broken types
* Static checkers

Note:

Checking types is *optional* in Python. It is **not enforced** by the Python
runtime. Instead, separate tools may use these hints for useful information.

PyCharm already supports type hints for quite some time and uses them for more
helpful auto-completions.

Additionally, the tool [mypy](http://mypy-lang.org) can be used to check a
project for type correctness:

```shell
$ mypy checked.py
checked.py:21: error: "int" has no attribute "upper"

$ # Recursively checks files in <package>.
$ mypy -p package
$ # Checks <module> and everything imported in it.
$ mypy -m module
```

^

## Type Checking Legacy Code

* Stub files (`.pyi`)
* No need to edit old code

Note:

mypy has support for "stub" files (``.pyi``). These files a *very* similar to a
C header file. They only contain function signatures without body.

* mypy first looks for stub files.
* If found they are used for type hints instead of the ``.py`` file.
* Can be used to add type-checks to third-party modules without type hints.
* [typeshed](https://github.com/python/typeshed) contains some stub files for
  popular projects and is bundled with ``mypy``.

^

## mypy difficulties

* mypy has its own search path to find Python source files (non-trivial with
  virtual environments).
* Dependencies to Python source which has no type-annotations
* Following imports not found on the mypy search path
