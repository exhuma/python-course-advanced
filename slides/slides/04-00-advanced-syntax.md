# Syntax Features & Useful Builtins

^

## List-Comprehensions

List comprehensions are concise 1-line statements to create new collections.

```py
iterable = [1, 2, 3, 4, 5]
new_list = [x for x in iterable]
```

Note:

* Creates a *new* list from elements of the *iterable*.
* If *iterable* is a generator, this will consume the generator.
* Can be used to modify and filter out values from the iterable.
* Don't over-use. Sometimes a ``for`` loop is easier to read.

^

Applying a function to each item:

```py
def modifier(x):
    return x * 2

new_list = [modifier(x) for x in old_list]
```

Using `map()`

```py
new_list = map(modifier, old_list)
```

^

Filtering items from a list:

```py
def is_valid(x):
    return x > 2

new_list = [x for x in old_list if is_valid(x)]
```

Using `filter()`

```py
new_list = filter(is_valid, old_list)
```

^

Filtering & Mapping combined

```py
def modifier(x):
    return x * 2

def is_valid(x):
    return x > 2

new_list = [modifier(x) for x in old_list if is_valid(x)]
```

Using `map()` & `filter()`

```py
new_list = map(modifier, filter(is_valid, old_list))
```

^

## Other Comprehensions

```py
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
```

^

## zipping

[`zip()`](py3_zip) and [`itertools.zip_longest()`](py_zip_longest) are
*very* powerful utility functions. They take iterables and return a new iterable
where each item is a tuple consisting of the next item of each iterable.

```py
>>> zip([1, 2, 3], ["a", "b"])
[(1, "a"), (2, "b")]
```

Note:

* [`zip()`](py3_zip) stops once the first iterable is exhausted.
* [`itertools.zip_longest()`](py_itertools_longest) fills in missing values with
  *fillvalue*

[py3_zip]: https://docs.python.org/3/library/functions.html#zip
[py3_zip_longest]: https://docs.python.org/3/library/itertools.html#itertools.zip_longest

^

## zip Examples

```py
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
```

^

## More than two Iterables

```py
>>> list_a = [1, 2, 3]
>>> list_b = [5, 6, 7]
>>> list_c = ['a', 'b', 'c']
>>> a, b, c = zip(list_a, list_b, list_c)

>>> a, b, c
((1, 5, 'a'), (2, 6, 'b'), (3, 7, 'c'))
```


^

## Using zip to "unzip"

An implicit property of the zip algorithm is that it can also be used to "unzip"
items. Consider the following two lists:

```py
[1, 2, 3]
[5, 6, 7]
```

By zipping them we get these three tuples:

```py
(1, 5)
(2, 6)
(3, 7)
```

^

[`zip`](py_zip) can be used with multiple iterables. So we can use those three
tuples as input again:

```py
zip((1, 5), (2, 6), (3, 7))
```

This will yield the following two **tuples**:

```py
(1, 2, 3)
(5, 6, 7)
```

Note:

In summary, we start with `[1,2,3]` and `[5, 6, 7]`. Zipping this gives us
`[(1, 5), (2, 6), (3, 7)]`.

When we call `zip` with the result values like this:

```py
zip((1, 5), (2, 6), (3, 7))
```

we get the original input back as result.

This can be simplified by using *unpacking*:

```py
zip(*zip(a, b))
```

^

## "Practical" Example

A function ``parse`` which converts a key/value string into a dictionary using
`zip`.

```py
data = "a 10 b 20 c 30"
```
<!-- .element: data-caption="Input Data" -->

```py
{"a": 10, "b": 20, "c": 30}
```
<!-- .element: data-caption="Expected output" -->

Note:

* Remember list "slicing" including "stepping"

```py
>>> data = 'a 10 b 20 c 30'
>>> parse(data)
{'a': '10', 'b': '20', 'c': '30'}
```

## Solution

```py
>>> def parse(line):
...     items = line.split()
...     keys = items[::2]
...     values = items[1::2]
...     return dict(zip(keys, values))
```
