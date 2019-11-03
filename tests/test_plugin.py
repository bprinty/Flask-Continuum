# -*- coding: utf-8 -*-
#
# Testing for plugin
#
# ------------------------------------------------


# imports
# -------
from .fixtures import db, Item, ItemFactory


# session
# -------
class TestVersioning(object):

    def test_query_existing(self, client, items):
        response = client.get('/items/{}'.format(items[0].id))
        assert response.status_code == 200
        assert response.json['name'] == items[0].name
        return

    def test_versioning(self, client):
        # create item and update it
        item = ItemFactory.create(name='versioning 1')
        response = client.put('/items/{}'.format(item.id), json=dict(
            name='versioning 2'
        ))
        assert response.status_code == 200
        assert response.json['name'] == 'versioning 2'

        # test versioning properties
        assert item.modified
        assert item.version_count == 2
        print(item.changeset)
        assert item.version_json(0)['name'] == 'versioning 1'
        assert item.version_json(0)['id'] == item.id
        assert item.version_json(0)['name'] == 'versioning 2'
        assert item.version_json(1)['id'] == item.id
        return

    def test_revert(self, client):
        # create item and update it
        item = ItemFactory.create(name='revert 1')
        response = client.put('/items/{}'.format(item.id), json=dict(
            name='revert 2'
        ))
        assert response.status_code == 200
        assert response.json['name'] == 'revert 2'

        # assert data was changed
        response = client.get('/items/{}'.format(item.id))
        assert response.status_code == 200
        assert response.json['name'] == 'revert 2'

        # test that multiple versions exist
        item = db.session.query(Item).filter_by(name='revert 2').one()
        assert item.version_count == 2

        # revert one of the versions
        version = item.versions[0]
        version.revert()
        db.session.commit()
        response = client.get('/items/{}'.format(item.id))
        assert response.status_code == 200
        assert response.json['name'] == 'revert 1'
        return
