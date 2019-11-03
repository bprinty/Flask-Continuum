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
    Need to consider implementing a custom plugin for this.
    """
    __versioned__ = {}

    @property
    def modified(self):
        return is_modified(self)

    @property
    def changeset(self):
        return changeset(self)

    @property
    def version_count(self):
        return count_versions(self)

    def version_json(self, idx):
        """
        Return json metadata for specific model version.
        """
        if not hasattr(self, 'json'):
            raise AssertionError('Error: json() method containing json data must be on model to use this method.')
        item = self.versions[idx]
        data = self.json()
        data.update({
            k: getattr(item, k)
            for k in data if k in item.__dict__
        })
        return data
