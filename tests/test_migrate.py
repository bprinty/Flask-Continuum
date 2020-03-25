# -*- coding: utf-8 -*-
#
# Testing for plugin
#
# ------------------------------------------------


# imports
# -------
import os
import subprocess

from . import SANDBOX, BASE
from .migrate import app, db


# session
# -------
class TestMigrations(object):

    def call(self, cmd):
        return subprocess.call('FLASK_APP=tests/migrate.py:app {} 1>/dev/null'.format(cmd), cwd=BASE, shell=True)

    def test_create_migration(self, application):
        path = os.path.join(SANDBOX, 'migrations')

        # create initial scheme in app context
        self.call('flask create')

        # initialize migrations directory (outside of app context)
        self.call('flask db init -d {}'.format(path))
        assert len(os.listdir(os.path.join(SANDBOX, 'migrations'))) != 0

        # create initial migration (outside of app context)
        self.call('flask db migrate -d {}'.format(path))
        assert len(os.listdir(os.path.join(SANDBOX, 'migrations', 'versions'))) != 0
        return
