
Overview
========

Provide overview snippet of what the plugin does.


A Minimal Application
---------------------


Setting up the flask application with extensions:


.. code-block:: python

    from flask import Flask
    from flask_continuum import Continuum

    app = Flask(__name__)
    app.config.from_object(Config)
    continuum = Continuum(app)


Here is how you use the plugin:

.. code-block:: python

    # insert code here ...


For more in-depth discussion on design considerations and how to fully utilize the plugin, see the `User Guide <./usage.html>`_.
