# -*- coding: utf-8 -*-

__pkg__ = 'Flask-Continuum'
__url__ = 'https://github.com/bprinty/Flask-Continuum'
__info__ = 'Model provenance and versioning via SQLAlchemy-Continuum'
__author__ = 'Blake Printy'
__email__ = 'bprinty@gmail.com'
__version__ = '0.1.4'


from .mixins import VersioningMixin      ## noqa
from .plugin import Continuum            ## noqa
