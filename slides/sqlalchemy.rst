Databases & SQLAlchemy
======================

DBAPI-2
-------

* `PEP-0249`_
* Default Database Interface spec.
* Loose spec.
* Raw SQL, few abstractions.

.. note::
    While the spec standardises many concepts, there are still some substantial
    differences between the different implementations. Most prominent is the
    difference between value placeholders (``?``, ``%s``, ``:varname``, |ell|).

.. _PEP-0249: https://www.python.org/dev/peps/pep-0249/


SQLAlchemy
----------

.. image:: _static/sqla_logo.png
    :align: right

* **The** DB Toolkit for Python.
* Abstraction over DBAPI-2
* Separated into:

  * **ORM** *(focus of this introduction)*
  * Expression Language
  * Metadata
  * Core

* Helps DB development at any level.
* Consistent API across DB engines (within limits)

.. note::
    While the *API* is consistent, you still have to decide whether to use DB
    specific concepts. For example, PostgreSQL has many advanced data types
    (Geometric Types, IP-Addresses, Arrays, |ell|). These data types may not be
    available on other databases. It is a tradeoff between being portable, and
    leveraging database features.


ORM Advantages / Disadvantages
------------------------------

* A lot less SQL to write.
* Possibility to build your query step-by-step.
* *Can* be database agnostic.
* Map Python classes to Business objects.
* May generate suboptimal SQL queries:

  * **n+1 problem** (Prevent using `Eager Loading`_).
  * **No Index-Only scans** (Prevent using `Load Only Cols`_).

* New Syntax to learn!


.. _Load Only Cols: http://docs.sqlalchemy.org/en/latest/orm/loading_columns.html#load-only-cols
.. _Eager Loading: http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#eager-loading


Example Mapping
---------------

.. hint::

    To map a table it must be at least 1NF (possible workarounds: the
    PostrgeSQL Array, JSON or hstore type).

.. code-block:: python

    from sqlalchemy import String, Unicode, Column
    from sqlalchemy.ext.declarative import declarative_base

    Base = declarative_base()

    class User(Base):
        __tablename__ = 'user'

        email = Column(String, primary_key=True)
        name = Column(Unicode)
        telephone_number = Column(String)

.. note::
    "Declarative" was implemented as SQLAlchemy *extension*. It has since
    become the de-facto standard for defining domain models together with data
    models. You can still use the "classical" way of mapping classes, in case
    your domain model does not directly map to the data model.

    In classical mapping, definition of tables, and objects is competely
    separate. It can for example be used to map an already existing domain
    model to a DB without touching the existing codebase.

    Both approaches can also be used together without problem.


Usage
-----

.. code-block:: python

    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)

    session = Session()
    user = User(email='user@example.com',
                name='Example User')
    session.add(user)
    session.commit()

See the `engine documentation
<http://docs.sqlalchemy.org/en/latest/core/engines.html>`_ for details on the
engine arguments.


The Session
-----------

See `Session Basics <http://docs.sqlalchemy.org/en/latest/orm/session_basics.html>`_

* implements the `Unit of Work`_ pattern.
* Holds objects in different states (The Entity Lifecycle).
* Not thread-safe (wrap in ``scoped_session`` for this use-case.
* Some actions trigger automatic "flushing" (``session.autoflush``).
* Can be created/closed often (lightweight)


.. _Unit of Work: http://martinfowler.com/eaaCatalog/unitOfWork.html


Querying
--------

.. code-block:: python

    session.query(User) # creates a basic ``SELECT`` query without filters or
                        # orderings (``SELECT * FROM user``).

    # create a new query with an added ``WHERE`` clause.
    query = query.filter(User.name == 'John')

    # This line would add a new filter, "anding" it with the previous filter.
    query = query.filter(or_(User.name == 'John', User.name == 'Jane'))

    # Calls to query methods like filter(), order(), group_by, ...
    # can be chained. They usually do not modify an existing query object:
    query = session.query(User).filter(User.name == 'John').order_by(
        User.name).limit(10)


Selecting and Editing
---------------------

.. code-block:: python

    query = session.query(User).filter_by(email='user@example.com')
    user = query.one()
    user.name = 'Updated name'
    session.commit()

**Common Gotcha**

.. code-block:: python

    user = User(email='user@example.com', name='Another update?')
    session.add(user)
    session.commit()


.. rst-class:: smaller-slide

Entity Lifecycle
----------------

See `Session Management <http://docs.sqlalchemy.org/en/latest/orm/session_state_management.html>`_

*transient*
  The object has been newly created (exists in memory) and is not yet in the
  session.

*pending*
  The object is changed in memory but that has not yet been flushed to the
  database.

*persistent*
  The object exists in memory and changes have been recorded to the database.

*detached*
  The object exists in memory, but is no longer attached to the database.


Updating with transient/detached entities
-----------------------------------------

.. code-block:: python

    user = User(email='user@example.com', name='Another update?')
    new_user = session.merge(user)
    session.commit()


Example Relationships
---------------------

.. code-block:: python
    :class: smaller

    # ... imports ...

    class Port(Base):
        __tablename__ = 'port'

        hostname = Column(String, ForeignKey('device.hostname'),
                          primary_key=True)
        label = Column(String, primary_key=True)


    class Device(Base):
        __tablename__ = 'device'

        hostname = Column(String, primary_key=True)

        ports = relationship('Port')


.. nextslide::
    :increment:

.. code-block:: python

    dev = Device(hostname='MyDevice')
    dev.ports.extend([
        Port(label='1/1'),
        Port(label='1/2'),
        Port(label='1/3')
    ])
    session.add(dev)
    session.commit()

    for port in dev.ports:
        print(port)

    session.delete(dev.ports[1])
    session.commit()

    for port in dev.ports:
        print(port)


Reflection (Introspection)
--------------------------

* Useful if you have an existing database
* Will load only the database items:

  * FKs are imported, SA relationships is still up to you!

Example:

.. code-block:: python

    class User(Base):
        __tablename__ = 'user'
        __table_args__ = {
            'autoload': True
        }

See `table configuration`_

.. _table configuration: http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/table_config.html

.. note::
    Reflection can be extremely useful if you already have an existing DB. The
    downside is however, that your application may break if the Database
    changes. But that may even happen if you *don't* use reflection! So it's
    fairly safe to use.


Example SQL Queries
-------------------

.. code-block:: python
    :class: smaller

    session.execute('SELECT x+10 FROM data')
    session.query(Data.x + 10)

    session.execute('SELECT x, NOW() FROM data')
    session.query(Data.x, func.now())

    session.execute('SELECT blablabla(1, 2, 3) FROM data')
    session.query(func.blablabla(1, 2, 3))

    session.execute('UPDATE data SET x = x * 2 WHERE x > 10')
    session.query(Data.x).filter(Data.x > 10).update({
        'x': Data.x*2
    })

    session.execute('DELETE FROM data WHERE x > 10')
    session.query(Data.x).filter(Data.x > 10).delete()

    # If all else fails...
    query = text('DELETE FROM data WHERE x > :value')
    session.execute(query.bindparams(value=10))


Other Highlights
----------------

**Custom data types**

If SQLAlchemy does not have existing support for a special data type in your
database, you can `build your own`_.

**Call any function**

Using the ``func`` function, you can call any database function and properly
bind values::

    session.query(Data).filter(func.sqrt(25) > Data.x)

.. nextslide::
    :increment:

**Use any operator**

Similarly to ``func``, you can use the ``op`` function to use any DB operator,
even if not foreseen by SQLAlchemy::

    # SELECT * FROM data WHERE (10, 20)::point <@ area
    session.query(Data).filter(Point(10, 20).op('<@')(Data.area))

    # SELECT * FROM data WHERE ip_address << '192.168.0.0/24'::inet
    session.query(Data).filter(Data.ip_address.op('<<')(
        ip_network('192.168.0.0/24')))

|ell| generally:

.. code-block:: text

    <LHS>.op('<operator>')(<RHS>)

.. _build your own: http://docs.sqlalchemy.org/en/latest/core/custom_types.html


Useful Links
------------

* `Official SQLAlchemy Homepage <http://www.sqlalchemy.org/>`_

  * `Official Documentation <http://docs.sqlalchemy.org/en/rel_1_0/>`_

* `Unit Testing with SA <http://docs.sqlalchemy.org/en/latest/orm/tutorial.html?highlight=joinedload#eager-loading>`_
* `Introduction by the creator of SA <https://www.youtube.com/watch?v=P141KRbxVKc>`_ *(over 3 hour video!)*

.. http://www.slideshare.net/mengukagan/an-introduction-to-sqlalchemy
.. TODO -> Read about "leaky abstraction"
.. TODO Add architecture graph, explain the elements.
.. transactions (engine is in autocommit vs UOW)

.. TODO * Reflection Table(autoload=True, autoload_with)
.. TODO   * Inspector
.. TODO * Alembic
.. TODO * SQL
.. TODO   * Bound placeholders
.. TODO     expr = x.c.name == 10
.. TODO     compiled = expr.compile(<dialect>)
.. TODO     compiled.params
.. TODO * Object Identity (identity map)::
.. TODO 
.. TODO   >>> a = User(name='john')
.. TODO   >>> b = session.query(User).first()
.. TODO   >>> a is b
.. TODO   True
.. TODO 
.. TODO 
.. TODO * Session.new
.. TODO * Session.dirty
.. TODO * Flush & Commit
.. TODO * After commit, all objects are expired (can be turned off).
.. TODO * ORM query indexing/slicing
.. TODO * filter (full-blown) vs filter_by (less typing)
.. TODO * all, first, one (multiple, none)
.. TODO * Not opinionated about existing schema. Not enforcing anything.
.. TODO * Custom Base Classes / Mixins
.. TODO * ORM events
.. TODO * ORMs (in general) synchronize primary keys with corresponding foreign keys
.. TODO * Once data is loaded in memory it will not reloaded (unless explicitly specified, or session closed/committed).
.. TODO * Default = Connection Pool, Can be used without one.
.. TODO * Use objects instead of FKs when working with relationships (works both ways, but when editing FKs, the ORM will be unaware). Will get complicated if you cannot commit the TX mid-way.
.. TODO .. My History {{{
.. TODO 
.. TODO My History
.. TODO ----------
.. TODO 
.. TODO Python - SQLObject
.. TODO Java Oracle Toplink
.. TODO Java Eclipselink
.. TODO Java Hibernate
.. TODO Java JPA
.. TODO PHP PDO
.. TODO PHP mDB2
.. TODO PHP Doctrine (-)
.. TODO .NET ADO
.. TODO 
.. TODO .. }}}
.. TODO 
.. TODO Installation
.. TODO ------------
.. TODO 
.. TODO SQLAlchemy installs just like any other third party module in Python::
.. TODO 
.. TODO     pip install sqlalchemy
.. TODO 
.. TODO You do however need the proper DB library installed as well if it is not
.. TODO included in the standard library (for example for PostgreSQL)::
.. TODO 
.. TODO     pip install psycopg2
.. TODO 
.. TODO * No imposed standards (like "id" column).
.. TODO * ORM & Expression Language
.. TODO * Connection Pooling & Lazy Connections
.. TODO * primary key needed in ORM
.. TODO * Creating
.. TODO * Selecting (one/first)
.. TODO * Lazy/Eager Loading (relationships)
.. TODO * Joins
.. TODO * alembic instead of ``create_all``
.. TODO http://docs.sqlalchemy.org/en/rel_1_0/orm/tutorial.html
