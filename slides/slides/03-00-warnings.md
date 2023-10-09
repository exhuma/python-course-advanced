# Warnings

^

## Emitting Warnings

```py
from warnings import warn

warn("My warning message")
warn("My warning message", DeprecationWarning)
```

Note:

Warnings provide an alternative messaging channel. The intended audience are
developers.

They are similar to exceptions, but they do not cause the program to crash.

Developers *can* choose to run the application with different warnings modes.
One of them is to convert each warning into exceptions and thereby causing
crashes.

See
[warnings.warn](https://docs.python.org/3/library/warnings.html#warnings.warn)
for details.


^

## Dealing with Warnings

* Console output by default
* Handled externally by `PYTHONWARNINGS` and `-W`
* Handled internally by [warnings.catch_warnings](https://docs.python.org/3/library/warnings.html#warnings.catch_warnings)
* Handled internally by [logging.captureWarnings](https://docs.python.org/3/library/logging.html#logging.captureWarnings)

Note:

Many warning features use "filters" to decide what to do with warnings. The
filter has the following format:

    action:message:category:module:line

A detailed explanation is available at [The Warnings
Filter](https://docs.python.org/3/library/warnings.html?highlight=warnings#the-warnings-filter)
