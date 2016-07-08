Text Parsing
============


Regular Expressions
-------------------

* The :py:mod:`re` module.
* Python RegEx syntax very similar to Perl.
* Syntax for the regexes themselves. *Not* the language syntax (There is no
  ``~=`` operator)!
* Raw strings (``r'...'``) avoids escaping backslashes.
* The :py:data:`re.VERBOSE` flag allows for multiline regexes with comments.
* The :py:data:`re.MULTILINE` flag allows searching across newlines.


Regular Expression Support
--------------------------

Python Regexes Support (apart from the bare basics):

* Non-Greedy qualifiers (``??``, ``+?``, ``*?``, ``{...}?``)
* Non-capturing groups (``(?:...)``)
* Named groups (``(?P<name>...)``)
* Inline comments (``(?#...)``)
* Lookaheads and lookbehinds (``(?=...)`` and ``(?<=...)``)
* Negative lookaheads and lookbehinds (``(?!...)`` and ``(?<!...)``)

.. rst-class:: smaller-slide

Usage
-----

Regular expressions can be used either 

* directly, using functions of the :py:mod:`re` module *or*
* by compiling them and executing methods on the resulting regex object.

Examples:

.. code-block:: python

    import re

    MY_PATTERN = re.compile(r'[a-zA-Z0-9_]+')
    MY_PATTERN.findall(somestring)

    # ... or ...

    re.findall(r'[a-zA-Z0-9_]+', somestring)


Most Useful Functions
---------------------

:py:func:`re.search`
    Find first occurrence of match and return it (or None if not found)

:py:func:`re.match`
    Like ``search`` but don't scan through the string.

:py:func:`re.split`
    Split a string on regex matches.

:py:func:`re.findall`
    Return all matches in a string.

:py:func:`re.sub`
    Return a new string with all regex matches replaced with a new string.


Matches
-------

Many functions return :py:class:`~re.Match` objects. These objects contain
additional metadata of the matched substring. Most notably: If the pattern
contained groups, they can be retrieved here:

* :py:meth:`~re.match.group` to access a single group,
* :py:meth:`~re.match.groups` to access all groups,
* :py:meth:`~re.match.groupdict` to access all named groups



PLY: For Lex and Yacc Veterans
------------------------------

.. sidebar:: GNU

    The GNU counterparts to Lex and Yacc are "Flex" and "Bison"


The third-party module ply_ is a Python implementation of Lex and Yacc.

* Lex, a lexer/tokenizer: transforms a document into a stream of tokens.
* Yacc, a parser: Takes a stream of tokens and detects a syntax tree according
  to a grammar (context free/LALR)
* ``lex.py`` uses ``re.VERBOSE``.


.. _ply: http://www.dabeaz.com/ply/


.. rst-class:: smaller-slide

Token and Grammar Definitions
-----------------------------

**Tokens**

.. code-block:: python
    :class: smaller

    tokens = ('WORD', 'NUMBER')
    t_WORD = r'\w+'
    def t_NUMBER(t):
        r'\d+'
        t.value = int(t)
        return r

**Grammar Rules**

.. code-block:: python
    :class: smaller

    from mylexer import tokens
    def p_myrule(p):
        '''
        myrule : WORD
               | NUMBER
        '''
        p[0] = p[1]


.. rst-class:: smaller-slide


Definitions Summary
-------------------

* Tokens and Productions are defined using docstrings.
* Tokens can also be defined as plain strings.
* Token and grammar definitions can be stored in separate files |ell|
* |ell| and can also be defined as classes.
* Token and Production functions can execute any Python code:

    * **Tokens:** type-conversion for token values, modify lexer state, |ell|
    * **Productions:** construct a syntax tree, trigger code execution, |ell|


Token Rule Precedence
---------------------

Lexer token rules are applied in the following order:

* Token functions (in order they are defined in)
* Simple token strings (in order of decreasing *pattern length*)


Grammar Syntax
--------------

Grammars in Yacc (and by extension ``ply``) are defined using the following
syntax:

.. code-block:: yacc

    statement : assignment
              | addition
              | substraction

    assignment : NAME EQUALS NUMBER

    addition : NUMBER '+' NUMBER

    substraction : NUMBER '-' NUMBER

.. nextslide::
    :increment:

* First rule (production) is the start rule (by default).
* Lower-case identifiers are further productions.
* Upper-case identifiers are tokens from the lexer.
* Literals are enclodes in single-quotes ``'``


Parse Error Recovery: Resynchronisation
---------------------------------------

.. code-block:: python

    def p_statement_print(p):
        'statement : PRINT expr SEMI'
        ...

    def p_statement_print_error(p):
        'statement : PRINT error SEMI'
        print("Syntax error in print statement. Bad expression")

Using the ``error`` production gives the parser an anchor to resynchronize: The
error happened somewhere ``PRINT`` and ``SEMI``.


Parser Error Recovery: Panic Mode
---------------------------------

.. code-block:: python

    def p_error(p):
        print("Whoa. You are seriously hosed.")
        if not p:
            print("End of File!")
            return

        # Read ahead looking for a closing '}'
        while True:
            tok = parser.token()             # Get the next token
            if not tok or tok.type == 'RBRACE':
                break
        parser.restart()

This will discard any tokens until ``RBRACE`` is reached. It will then reset
the parser into the initial state.


Yacc Output Files
-----------------

By default, ``yacc.py`` writes a debug file ``parser.out`` and ``parsetab.py``.
This can be a problem on deployment.

This can be controlled using::

    yacc.yacc(outputdir="/path/to/folder")
    yacc.yacc(write_tables=False)
    yacc.yacc(debug=False)


Offifcial PLY Example
---------------------

See `Official PLY example <http://www.dabeaz.com/ply/example.html>`_.


.. TODO yacc.py ref to packaging
