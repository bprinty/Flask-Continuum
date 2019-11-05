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

    # def version_json(self, idx):
    #     """
    #     Return json metadata for specific model version.

    #     Arguments:
    #         idx (int): Index of versioned object to return JSON for.
    #     """
    #     if not hasattr(self, 'json'):
    #         raise AssertionError('Error: json() method containing json data must be on model to use this method.')
    #     item = self.versions[idx]
    #     data = self.json()
    #     data.update({
    #         k: getattr(item, k)
    #         for k in data if k in item.__dict__
    #     })
    #     return data

    @property
    def history(self):

        class VersionedInstance(self.__class__):

            def __init__(self, **kwargs):
                self.__version_obj__ = kwargs.pop('__version_obj__')
                for key in kwargs:
                    setattr(self, key, kwargs[key])
                return

            @property
            def previous(self):
                return self.__version_obj__.previous

            @property
            def next(self):
                return self.__version_obj__.next

            @property
            def index(self):
                return self.__version_obj__.index

            def revert(self):
                return self.__version_obj__.revert()

        VersionedInstance.__name__ = 'Versioned{}'.format(self.__class__.__name__)

        # gather cols
        columns = []
        mapper = inspect(self.__class__)
        for col in mapper.attrs:
            if hasattr(col, 'columns'):
                columns.append(col.columns[0].key)

        # configure versioning
        proxies = []
        for idx in range(count_versions(self)):
            item = self.versions[idx]
            data = {
                k: getattr(item, k)
                if k in item.__dict__ else getattr(self, k)
                for k in columns
            }
            print(data)
            data['__version_obj__'] = item
            proxies.append(VersionedInstance(**data))

        print(proxies)

        return proxies
