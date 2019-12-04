# -*- coding: utf-8 -*-
#
# Plugin Setup
#
# ------------------------------------------------


# imports
# -------
from flask import Flask
from flask.globals import _app_ctx_stack, _request_ctx_stack
from sqlalchemy_continuum.plugins import FlaskPlugin
from sqlalchemy_continuum import make_versioned
from sqlalchemy.orm import configure_mappers
from sqlalchemy import event


# helpers
# -------
def fetch_current_user_id():
    if _app_ctx_stack.top is None or _request_ctx_stack.top is None:
        return
    try:
        from flask_login import current_user
        return current_user.id
    except (ImportError, AttributeError):
        return


CONFIGURED = False


# plugin
# ------
class Continuum(object):
    """
    Flask extension class for module, which sets up all flask-related
    capabilities provided by the module. This object can be initialized
    directly:

    .. code-block:: python

        from flask import Flask
        from flask_version import Version

        app = Flask(__name__)
        db = SQLAlchemy()
        continuum = Continuum(app, db)

    Or lazily via factory pattern:

    .. code-block:: python

        db = SQLAlchemy()
        continuum = Continuum(db=db)
        app = Flask(__name__)
        continuum.init_app(app)

    To configure SQLAlchemy-Continuum with additional plugins, use the
    ``plugins`` argument to the extension:

    .. code-block:: python

        from sqlalchemy.continuum.plugins import PropertyModTrackerPlugin

        db = SQLAlchemy()
        continuum = Continuum(db=db, plugins=[PropertyModTrackerPlugin()])
        app = Flask(__name__)
        continuum.init_app(app)

    You can also use this plugin with sqlalchemy directly (i.e. not using
    Flask-SQLAlchemy). To do so, simply pass the database engine to this
    plugin upon instantiation:

    .. code-block:: python

        engine = create_engine('postgresql://...')
        continuum = Continuum(engine=engine)
        app = Flask(__name__)
        continuum.init_app(app)

    Finally, to associate all transactions with users from a user table in
    the application database, you can set the `user_cls` parameter to the
    name of the table where users are stored:

    .. code-block:: python

        app = Flask(__name__)
        db = SQLAlchemy(app)
        continuum = Continuum(app, db, user_cls='Users')

    Arguments:
        app (Flask): Flask application to associate with plugin.
        db (SQLAlchemy): SQLAlchemy extension to associate with plugin.
        user_cls (str): Name of user class used in application.
        engine (Engine): SQLAlchemy engine to associate with plugin.
        current_user (callable): Callable object to determine user associated
                                 with request.
        plugins (list): List of other SQLAlchemy-Continuum plugins to install.
            See: `https://sqlalchemy-continuum.readthedocs.io/en/latest/plugins.html`_
            for more information.

    """

    def __init__(self, app=None, db=None, user_cls=None, engine=None, current_user=fetch_current_user_id, plugins=[]):
        self.db = None
        self.app = None
        self.engine = engine
        self.user_cls = user_cls
        self.current_user = current_user

        # arg mismatch
        if app is not None and \
           db is None and \
           not isinstance(app, Flask):
            self.init_db(app)
            app = None

        # proper spec
        if db is not None:
            self.init_db(db)

        # app is specified properly
        if app is not None:
            self.init_app(app)

        # configure versioning support
        make_versioned(
            user_cls=self.user_cls,
            plugins=[
                FlaskPlugin(current_user_id_factory=self.current_user)
            ] + list(plugins)
        )
        return

    def init_app(self, app, db=None):
        """
        Initialize application via lazy factory pattern.

        Args:
            app (Flask): Flask application.
            db (SQAlchemy): Flask SQLAlchemy extension.
        """
        if db is not None:
            self.init_db(db)

        self.app = app

        # configure engine mappers on first connection
        engine = self.engine
        if engine is None:
            db = self.db
            if db is None:
                if 'sqlalchemy' not in app.extensions:
                    raise AssertionError(
                        'Flask-Continuum must be provided database engine '
                        'to configure mappers. Either instantiate Continuum '
                        'plugin with `db` argument (from Flask-SQLAlchemy) or '
                        '`engine` argument (from SQLAlchemy). Consult the documentation '
                        'for more detailed information.')

                db = app.extensions['sqlalchemy']

            # register app on sqlalchemy object (accounting for Flask-SQLAlchemy inconsistencies)
            if db.app is None:
                db.app = app

            engine = db.engine

        @event.listens_for(engine, "connect")
        def do_connect(dbapi_connection, connection_record):
            configure_mappers()
            return
        return

    def init_db(self, db):
        self.db = db
        return
