
Uncomment below for banners

|Build status| |Code coverage| |Maintenance yes| |GitHub license| |Documentation Status|

.. |Build status| image:: https://travis-ci.com/bprinty/Flask-Continuum.png?branch=master
   :target: https://travis-ci.com/bprinty/Flask-Continuum

.. |Code coverage| image:: https://codecov.io/gh/bprinty/Flask-Continuum/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/bprinty/Flask-Continuum

.. |Maintenance yes| image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg
   :target: https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity

.. |GitHub license| image:: https://img.shields.io/github/license/Naereen/StrapDown.js.svg
   :target: https://github.com/bprinty/Flask-Continuum/blob/master/LICENSE

.. |Documentation Status| image:: https://readthedocs.org/projects/flask-continuum/badge/?version=latest
   :target: http://flask-continuum.readthedocs.io/?badge=latest


============================
Flask-Continuum
============================

Flask-Continuum is a lightweight Flask extension for providing data provenance and versioning support to Flask applications using SQLAlchemy. It is built on top of the `sqlalchemy-continuum <https://github.com/kvesteri/sqlalchemy-continuum>`_ package, and provides a more Flask-y development experience for app configuration. If you'd like to configure your application with ``sqlalchemy-continuum`` directly, consult the ``sqlalchemy-continuum`` `documentation <https://sqlalchemy-continuum.readthedocs.io/en/latest/>`_.


Installation
============

To install the latest stable release via pip, run:

.. code-block:: bash

    $ pip install Flask-Continuum


Alternatively with easy_install, run:

.. code-block:: bash

    $ easy_install Flask-Continuum


To install the bleeding-edge version of the project (not recommended):

.. code-block:: bash

    $ git clone http://github.com/bprinty/Flask-Continuum.git
    $ cd Flask-Continuum
    $ python setup.py install


Usage
=====

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


Documentation
=============

For more detailed documentation, see the `Docs <https://Flask-Continuum.readthedocs.io/en/latest/>`_.


Questions/Feedback
==================

File an issue in the `GitHub issue tracker <https://github.com/bprinty/Flask-Continuum/issues>`_.
