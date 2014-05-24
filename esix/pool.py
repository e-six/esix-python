#!/usr/bin/env python3
"""
Pool class for the e621 API.
"""

from . import api, config, errors, post

def search(title='', limit=5):
    """Search the site's image pools by name.

    :param title: The whole or partial pool name. Omit for all pools.
    :type title: str
    :param limit: The highest number of pages to fetch, 20 results per page.
        Default 5.
    :type limit: int
    :returns: A generator of matching pools.
    :rtype: generator object
    """
    url = config.BASE_URL + 'pool/index.json?query=' + str(title)
    result = 0
    page = 1
    end = False
    while not end:
        rs = api._get_data_obj(api._get_page(url+'&page='+str(page)))
        result += len(rs)
        for pool_data in rs:
            yield Pool(pool_data=pool_data)
        if rs is None or len(rs) == 0 or (limit and result >= limit*20):
            end = True
            break
        result += len(rs)
        page += 1

def recent():
    """Fetch the 20 most recently updated pools on the site.

    :returns: A generator of recently updated pools.
    :rtype: generator object
    """
    url = config.BASE_URL + 'pool/index.json'
    for pool_data in api._get_data_obj(api._get_page(url)):
        yield Pool(pool_data=pool_data)


class Pool(object):
    def __init__(self, pool_id=None, pool_data=None):
        """Create an instance of a pool.

        :param pool_id: The pool's ID number for retrieving from the site.
        :type pool_id: int
        :param pool_data: Raw data to load directly into the object.
        :type pool_data: dict
        """
        self._data = {}
        for prop in ['id', 'name', 'user_id', 'created_at',
                     'updated_at', 'post_count', 'is_public',
                     'is_active', 'description']:
            self._data[prop] = None
        if pool_id is None and pool_data is None: return
        if pool_id is not None:
            url = config.BASE_URL + 'pool/show.json?id=' + str(pool_id)
            pool_data = api._get_data_obj(api._get_page(url+'&page=999'))
            if 'posts' in pool_data: del(pool_data['posts'])
        for prop in pool_data: self._data[prop] = pool_data[prop]

    @property
    def id(self):
        """Returns the pool's ID."""
        return self._data['id']

    @property
    def name(self):
        """Returns the pool's name."""
        return self._data['name']

    @property
    def name_normal(self):
        """Returns a user-friendly formatted version of the pool's name."""
        return self.name.replace('_',' ').title()

    @property
    def user_id(self):
        """Returns the ID of the user who created the pool."""
        return self._data['user_id']

    @property
    def created_at(self):
        """Returns a dict of information on the pool's creation time."""
        return self._data['created_at']

    @property
    def updated_at(self):
        """Returns a dict of information on the pool's last update."""
        return self._data['updated_at']

    @property
    def post_count(self):
        """Returns the number of posts in the pool."""
        return self._data['post_count']

    @property
    def is_public(self):
        """Returns whether or not the pool is marked public."""
        return self._data['is_public']

    @property
    def is_active(self):
        """Returns whether or not the pool is active."""
        return self._data['is_active']

    @property
    def description(self):
        """Returns the pool's description."""
        return self._data['description']

    @property
    def posts(self):
        """Returns a generator of Post objects for the pool."""
        url = url = config.BASE_URL + 'pool/show.json?id=' + str(self.id)
        page = 1
        end = False
        while not end:
            rs = api._get_data_obj(api._get_page(url+'&page='+str(page)))
            for post_data in rs['posts']:
                yield post.Post(post_data=post_data)
            if rs is None or len(rs['posts']) == 0:
                end = True
                break
            page += 1
