# -*- coding: utf-8 -*-
#
# Database mixins
#
# ------------------------------------------------


# imports
# -------
from sqlalchemy import inspect
from sqlalchemy_continuum import changeset, count_versions, is_modified


# mixins
# ------
class VersioningMixin(object):
    """
    Database mixin adding versioning support and additional
    helper methods to content models in application. To use
    this mixin in a model, you can configure it like so:

    .. code-block:: python

        class Article(db.Model, VersioningMixin):
            __tablename__ = 'article'

            id = db.Column(db.Integer, primary_key=True, autoincrement=True)
            name = db.Column(db.Unicode(255))
            content = db.Column(db.UnicodeText)
            updated_at = db.Column(db.DateTime, default=datetime.now)
            created_at = db.Column(db.DateTime, onupdate=datetime.now)

    This will implicitly add versioning support to the model.
    """
    __versioned__ = {}

    @property
    def modified(self):
        """
        Return boolean describing if object has been modified.
        """
        return count_versions(self) > 0

    @property
    def changeset(self):
        """
        Return SQLAlchemy-Continuum changeset for object.
        """
        return changeset(self)

    @property
    def records(self):
        """
        Return list of records in versioning history.
        """

        class VersionedInstanceMixin(object):
            __abstract__ = True

            @property
            def previous(self):
                return self.__version__.previous

            @property
            def next(self):
                return self.__version__.next

            @property
            def index(self):
                return self.__version__.index

            def revert(self):
                self.__version__.revert()
                return

        # dynamically create new type with mixin functionality
        VersionedClass = type(
            '{}Record'.format(self.__class__.__name__),
            (VersionedInstanceMixin, self.__class__), {}
        )

        # gather cols
        columns = []
        mapper = inspect(self.__class__)
        for col in mapper.attrs:
            if hasattr(col, 'columns'):
                columns.append(col.columns[0].key)

        # configure versioning
        proxies = []
        for idx in range(count_versions(self)):
            record = self.versions[idx]

            # get column data
            data = {}
            for k in columns:
                if k in record.__dict__:
                    data[k] = getattr(record, k)
                else:
                    data[k] = getattr(self, k)

            # create new abstract object
            item = VersionedClass(**data)
            item.__version__ = record
            proxies.append(item)

        return proxies
