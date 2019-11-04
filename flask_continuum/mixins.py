# -*- coding: utf-8 -*-
#
# Database mixins
#
# ------------------------------------------------


# imports
# -------
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

    # @property
    # def modified(self):
    #     """
    #     Return boolean describing if object has been modified.
    #     """
    #     return is_modified(self)

    @property
    def changeset(self):
        """
        Return SQLAlchemy-Continuum changeset for object.
        """
        return changeset(self)

    @property
    def version_count(self):
        """
        Return number of versions for object.
        """
        return count_versions(self)

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
