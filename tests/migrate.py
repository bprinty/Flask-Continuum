from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_continuum import Continuum, VersioningMixin
from flask_migrate import Migrate
# from sqlalchemy import orm

from . import SANDBOX

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/migrate.db'.format(SANDBOX)\

db = SQLAlchemy(app)
migrate = Migrate(app, db)
continuum = Continuum(app, db, migrate)

class User(VersioningMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(123))


@app.cli.command('create')
def create():
    db.create_all();
    return
