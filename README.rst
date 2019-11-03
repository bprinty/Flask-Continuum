
.. Uncomment below for banners

.. |Build status| |Code coverage| |Maintenance yes| |GitHub license| |Documentation Status|

.. .. |Build status| image:: https://travis-ci.com/bprinty/Flask-Plugin.png?branch=master
..    :target: https://travis-ci.com/bprinty/Flask-Plugin

.. .. |Code coverage| image:: https://codecov.io/gh/bprinty/Flask-Plugin/branch/master/graph/badge.svg
..    :target: https://codecov.io/gh/bprinty/Flask-Plugin

.. .. |Maintenance yes| image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg
..    :target: https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity

.. .. |GitHub license| image:: https://img.shields.io/github/license/Naereen/StrapDown.js.svg
..    :target: https://github.com/bprinty/Flask-Plugin/blob/master/LICENSE

.. .. |Documentation Status| image:: https://readthedocs.org/projects/flask-plugin/badge/?version=latest
..    :target: http://flask-plugin.readthedocs.io/?badge=latest


============================
Flask-Plugin
============================

Flask-Plugin is a scaffold for Flask extension development. To begin writing a new flask extension, copy this repository and change all refs from ``flask_plugin`` and ``Flask-Plugin`` to whatever your extension is named. Include an overview description of the plugin here.


Installation
============

To install the latest stable release via pip, run:

.. code-block:: bash

    $ pip install Flask-Plugin


Alternatively with easy_install, run:

.. code-block:: bash

    $ easy_install Flask-Plugin


To install the bleeding-edge version of the project (not recommended):

.. code-block:: bash

    $ git clone http://github.com/bprinty/Flask-Plugin.git
    $ cd Flask-Plugin
    $ python setup.py install


Usage
=====

Below is a minimal application configured to take advantage of some of the extension's core features:

.. code-block:: python

    from flask import Flask
    from flask_plugin import Plugin

    app = Flask(__name__)
    app.config.from_object(Config)
    plugin = Plugin(app)


The following is a minimal application highlighting most of the major features provided by the extension:

.. code-block:: python

    INSERT CODE


Documentation
=============

For more detailed documentation, see the `Docs <https://Flask-Plugin.readthedocs.io/en/latest/>`_.


Questions/Feedback
==================

File an issue in the `GitHub issue tracker <https://github.com/bprinty/Flask-Plugin/issues>`_.
