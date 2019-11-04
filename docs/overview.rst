
Overview
========

Flask-Continuum is a lightweight Flask extension for providing data provenance and versioning support to Flask applications using SQLAlchemy. It is built on top of the `sqlalchemy-continuum <https://github.com/kvesteri/sqlalchemy-continuum>`_ package, and provides a more Flask-y development experience for app configuration. If you'd like to configure your application with ``sqlalchemy-continuum`` directly, consult the ``sqlalchemy-continuum`` `documentation <https://sqlalchemy-continuum.readthedocs.io/en/latest/>`_.


A Minimal Application
---------------------

Setting up the flask application with extensions:

.. code-block:: python

    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_continuum import Continuum

    app = Flask(__name__)
    db = SQLAlchemy(app)
    continuum = Continuum(app, db)


Or, using via the Flask app factory pattern:

.. code-block:: python

    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_continuum import Continuum

    db = SQLAlchemy()
    continuum = Continuum(db=db)
    app = Flask(__name__)
    db.init_app(app)
    continuum.init_app(app)


The following is a minimal example highlighting how the extension is used. Much of the example was taken from the SQLAlchemy-Continuum documentation to show how this plugin extends that package for a Flask application:

.. code-block:: python

    from flask_continuum import VersioningMixin

    # defining database schema
    class Article(db.Model, VersioningMixin):
        __tablename__ = 'article'

        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        name = db.Column(db.Unicode(255))
        content = db.Column(db.UnicodeText)


    # later in api or request handlers
    article = Article(name='Some article', content='Some content')
    session.add(article)
    session.commit()

    # article has now one version stored in database
    article.versions[0].name
    # 'Some article'

    article.name = 'Updated name'
    session.commit()

    article.versions[1].name
    # 'Updated name'


    # lets revert back to first version
    article.versions[0].revert()

    article.name
    # 'Some article'


For more in-depth discussion on design considerations and how to fully utilize the plugin, see the `User Guide <./usage.html>`_.
