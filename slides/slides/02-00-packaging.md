# Packaging

Packaging allows us to distribute code among other code-bases and developers.

^

## Packages & Distributions

The term "Package" is ambiguous.

Using the term "Distribution" helps to clarify this.

Note:

In Python, a folder containing Python modules (`.py` files) is called a
"package".

This creates an ambiguity on the term "package": "Stuff" that you can download
from https://pypi.org are *also* called "packages".

The first is only a method to split the code of your project into multiple
files.

The latter is a way to distribute code among projects and developers.

In this section we talk about *the latter*.

^

## Metadata

* *Name*
* *Version*
* Dependencies
* Entrypoints
* Documentation
* ...

<!-- .element: class="smaller-text" -->

Note:

A package *must* have at least a name and a version.

Python packages support a large variety of additional meta-data fields. See
[PEP-621](https://peps.python.org/pep-0621/) for the official fields.

Some packaging tools provide additional meta-data. This course only covers the
official meta-data.
<!-- .element: class="admonition note" -->

^

## pyproject.toml

<!-- .element: style="text-transform: none" -->

The `pyproject.toml` file contains the project meta-data. A minimal file looks
like this:

<!-- .element: class="text" -->

```toml
[project]
name = "my-package"
version = "1.0.0rc1"
```

Note:

The `pyproject.toml` file replaces `setup.py` for project meta-data. The TOML
file has several advantages:

* It can be easily read and parsed with external tools
* It decouples the build & packaging process from the local code-base (and the
  Python environment)
* It makes it possible to develop new third-party build systems.

Using `setup.py` is still possible, but new projects should prefer `pyproject.toml`.

<!-- .element: class="admonition note" -->

For valid version-numbers, see [PEP-440](https://peps.python.org/pep-0440/)

<!-- .element: class="admonition tip" -->

^

## Building

```shell
pipx install build
pyproject-build
ls -l dist
```

Note:

The `build` package is the official tool for Python. It honours the
`build-system` of a `pyproject.toml` file (we will cover this later)

If you don't have the permission to install it, you have two options:

* Use [pipx](https://pypa.github.io/pipx/) *(recommended)*
* Install it into a separate virtual environment (covered later)

^

## Installation

*Any* folder with a `pyproject.toml` (or `setup.py`) file can be locally
*installed.

Normally, the distribution file (`.whl`, `.tar.gz`) is installed.

Local folder-installs are useful for development



^

## Dependencies

```toml
[project]
...
dependencies = [
    "requests",
    "pyyaml",
    "example-module-with-lower-bound >= 1.2.0",
    "example-module-with-upper-bound < 2.0",
    "example-module-with-range >=1.2.0, < 2.0",
    "example-module-with-blacklist != 1.2.3",
    "example-pinned-module == 1.2.4",
]
```

Note:

Dependencies are automatically installed when the package is installed using
`pip`. During installation, it ensures that all conditions are met.

By default, packages are downloaded from https://pypi.org (called the "package
index").

It is possible to use a different "index" by specifying the environment variable
`PIP_PACKAGE_INDEX` or setting `index-url` in the pip config file See [the
official configuration
page](https://pip.pypa.io/en/stable/topics/configuration/) for more information

^

## Optional Dependencies

```toml
[project.optional-dependencies]
test = [
    "pytest",
    "pytest-cache",
    "pytest-coverage",
]
dev = [
    "types-PyYAML",
]
```

Note:

Optional dependencies are *not* installed by default. They have to be enabled by
adding the name of the collection (often called the "extra") in square brackets:

```shell
pip install my-package[dev,test]
```

Extras can also be enabled in the `dependencies` section of another application:

```toml
dependencies = [
    "my-package[my-extra]"
]
```

You may have as many optional dependencies as you like. The extra-names are not
limited.

<!-- .element: class="admonition tip" -->

<div class="admonition tip">
<p><strong>Example:</strong> Add an optional web-ui to your application
limited.</p>
<p><pre>web = [
    "flask",
]</pre></p>
</div>

^

## Additional Metadata

* Description
* Readme
* Authors
* URLs

Note:

```toml
[project]
description = "My distributed package"
readme = "README.rst"
authors = [
  {
    name="Michel Albert",
    email="michel.albert@post.lu"
  },
]

[project.urls]
"Documentation" = "the-url"
"Repository" = "another-url"
```

* You may have more than one author
* The "readme" content is extracted from the referenced file and added to the
  project meta-data. Two formats are supported: `.md` (Markdown) and `.rst`
  (reStructuredText)
* You are free to choose the keys for `project.urls`

^

## Console Scripts

```toml
[project.scripts]
my-executable = "my_package.my_module:the_main_function"
another-executable = "my_package.another_module:another_function"

[build-system]
requires = ["setuptools >= 64.0"]
build-backend = "setuptools.build_meta"
```

Note:

Specification on entry-points depends on the build-system. This example uses
`setuptools` which is officially supported by the Python Packaging Authority
(pypa). See https://setuptools.pypa.io/

<!-- .element: class="admonition warning" -->

Defining "scripts" will automatically create executable when the project is
installed. The executables will be created in the binary folder of the
environment where the project is installed.

---

# Virtual Environments

Isolate projects & their dependencies

^

## Creation

```shell
python3 -m venv /path/to/environment
```

Note:

This command creates a new isolated environment for Python. Any package (and its
dependencies) installed in that environment will not interfere with the
operating system or other applications.

## Benefits

* Protect projects from side-effects of other projects
* Install multiple versions of the same library
* Install packages without `root` access
* Don't break the operating-system by installing packages

^

## Usage

Direct Invocation

```shell
/path/to/environment/bin/python
/path/to/environment/bin/pip
```

Via activation:

```shell
source /path/to/environment/bin/activate
...
deactivate
```

Note:

## Direct Invocation

* ✓ Ensures that you are using the correct environment
* ✓ Avoids mistakes
* ✗ Easy to use

## Activation

* ✗ Ensures that you are using the correct environment
* ✗ Avoids mistakes
* ✓ Easy to use

Activating an environment sets the `bin` folder of the environment onto the
`PATH` until deactivated by running the command `deactivate`.

If you forget to deactivate the environment, you risk running commands in that
environment.

^

## Editable Install

```shell
pip install --editable /path/to/package
```

* Default: Copy files to env
* Editable: Link files to env

Note:

When installing a project into an environment, files are *copied* into the
environment subfolder. Any changes to the local files will only take effect when
running installation again.

This is cumbersome during development.

Installing a package in "editable mode" will link the files instead. Any changes
will take immediate effect.

^

## Example

```shell
git clone ssh://git@git.ptech.lu/my-team/my-project.git
cd my-project
python3 -m venv env
./env/bin/pip install -e ".[dev,test]"
```

Note:

The `-e` flag for the install command is the short form of `--editable`.