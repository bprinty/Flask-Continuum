
Usage
=====

The sections below detail how to fully use this module, along with context for design decisions made during development of the plugin.


Configuration
-------------

Talk about configuring with Flask-SQLAlchemy or engine= directly.


Mixins
------

Talk about VersioningMixin

.. code-block:: python

    article = db.session.query(Article).one()

    # show properties provided by mixin


Versioning Specific Fields
--------------------------

Talk about how to configure version tracking for specific fields.


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
                                   tables. By default, this is set to True,
                                   and additional data stored for provenance
                                   are the user associated with the request
                                   and the remote address of the request.
================================== =========================================


Other Customizations
++++++++++++++++++++

As detailed in the `Overview <./overview.html>`_ section of the documentation,
the plugin can be customized with specific triggers. The following detail
what can be customized:

* ``user_cls`` - An option for the plugin.
* ``current_user`` - An option for the plugin.
* ``engine`` - An option for the plugin.

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
