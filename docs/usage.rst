
Usage
=====

The sections below detail how to fully use this module, along with context for design decisions made during development of the plugin.


Setup
-----

Obviously, this plugin requires the use of SQLAlchemy for model definitions. However, there are two common patterns for how SQLAlchemy models are configured for a Flask application:

1. Using the `Flask-SQLAlchemy <https://flask-sqlalchemy.palletsprojects.com/en/2.x/>`_ plugin for simplifying boilerplate associated with configuring a SQLAlchemy-backed Flask application (recommended).

2. Using SQLAlchemy directly with the `declarative <https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/basic_use.html>`_ system for defining models in your application.


If you're using the ``Flask-SQLAlchemy`` plugin, you can configure this plugin by passing the ``db`` parameter into the extension:

.. code-block:: python

    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_continuum import Continuum

    db = SQLAlchemy()
    continuum = Continuum(db=db)
    app = Flask(__name__)
    db.init_app(app)
    continuum.init_app(app)


If you're using SQLAlchemy directly, you need to pass the SQLAlchemy ``engine`` to the plugin. See the SQLAlchemy `documentation <https://docs.sqlalchemy.org/en/13/core/engines.html>`_ for more context on setting up the ``engine``:

.. code-block:: python

    from flask import Flask
    from sqlalchemy import create_engine
    from flask_continuum import Continuum

    engine = create_engine('postgresql://admin:password@localhost:5432/my-database')
    continuum = Continuum(engine=engine)
    app = Flask(__name__)
    continuum.init_app(app)


Aside from the plugin configuration detailed above, there is no additional steps required for configuring mappers or setting up ``sqlalchemy-continuum``. SQLAlchemy mappers for versioning tables will be set up when the first connection to the application database is made. For more information on additional configuration options, see the `Other Customizations`_ section below.


Mixins
------

In order to add versioning support to models in your application, you can either:

1. Use the ``VersioningMixin`` from this package to add versioning support and additional helper methods (recommended).
2. Add a ``__versioned__ = {}`` property to model classes.


With the ``VersioningMixin``, you can add versioning to a model via:

.. code-block:: python

    class Article(db.Model, VersioningMixin):
        __tablename__ = 'article'

        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        name = db.Column(db.Unicode(255))
        content = db.Column(db.UnicodeText)
        updated_at = db.Column(db.DateTime, default=datetime.now)
        created_at = db.Column(db.DateTime, onupdate=datetime.now)


.. The mixin also provides additional methods that can be useful when tracking revisions. Below are some examples of those methods. For more information, see the `API <./api.html>`_ section of the documentation.

.. .. code-block:: python

..     # code
..     # finish after tests


Additionally, if you only want to track specific fields in the database (for more efficient changeset processing), you can use the following syntax:

.. code-block:: python

    class Article(db.Model, VersioningMixin):
        __versioned__ = {
            'include': ['name', 'content']
        }
        __tablename__ = 'article'

        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        name = db.Column(db.Unicode(255))
        content = db.Column(db.UnicodeText)
        updated_at = db.Column(db.DateTime, default=datetime.now)
        created_at = db.Column(db.DateTime, onupdate=datetime.now)


For more details on what the ``__versioned__`` property can encode, see the ``SQLAlchemy-Continuum`` documentation. If you have no need for the ``VersioningMixin``, you can take route (2) like so:

.. code-block:: python

    class Article(db.Model):
        __versioned__ = {}
        __tablename__ = 'article'

        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        name = db.Column(db.Unicode(255))
        content = db.Column(db.UnicodeText)



Configuration
-------------

The following configuration values exist for Flask-Continuum.
Flask-Continuum loads these values from your main Flask config which can
be populated in various ways. Note that some of those cannot be modified
after the database engine was created so make sure to configure as early as
possible and to not modify them at runtime.

Configuration Keys
++++++++++++++++++

A list of configuration keys currently understood by the extension:

.. tabularcolumns:: |p{6.5cm}|p{10cm}|

================================== =========================================
``CONTINUUM_RECORD_REQUEST_INFO``  Whether or not the plugin should record
                                   request information in the versioning
                                   tables. By default, this is set to ``True``,
                                   and additional data stored for provenance
                                   are the user associated with the request
                                   and the remote address of the request.
================================== =========================================


Other Customizations
++++++++++++++++++++

As detailed in the `Overview <./overview.html>`_ section of the documentation,
the plugin can be customized with specific triggers. The following detail
what can be customized:

* ``user_cls`` - The name of the user table to associate with content changes.
* ``current_user`` - A function for returning the current user issuing a request. By default, this is determined from the ``Flask-Login`` plugin, but can be overwritten.
* ``engine`` - A SQLAlchemy engine to connect to the database. This parameter can be used if the application doesn't require the use of ``Flask-SQLAlchemy``.

The code below details how you can override all of these configuration options:

.. code-block:: python

    from flask import Flask
    from flask_continuum import Continuum
    from sqlalchemy import create_engine

    app = Flask(__name__)
    engine = create_engine('postgresql://...')
    continuum = Continuum(
        engine=engine,
        user_cls='Users',
        current_user=lambda: g.user
    )
    continuum.init_app(app)


For even more in-depth information on the module and the tools it provides, see the `API <./api.html>`_ section of the documentation.
