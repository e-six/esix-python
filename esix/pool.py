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
        rs = api._fetch_data(url + '&page=' + str(page))
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
    for pool_data in api._fetch_data(url):
        yield Pool(pool_data=pool_data)


class Pool(object):
    def __init__(self, pool_id=None, pool_data=None):
        """Create an instance of a pool.

        :param pool_id: The pool's ID number for retrieving from the site.
        :type pool_id: int
        :param pool_data: Raw data to load directly into the object.
        :type pool_data: dict
        :raises: errors.PoolNotFoundError
        """
        self._data = {}
        for prop in ['id', 'name', 'user_id', 'created_at',
                     'updated_at', 'post_count', 'is_public',
                     'is_active', 'description']:
            self._data[prop] = None
        if pool_id is not None:
            url = config.BASE_URL + 'pool/show.json?id=' + str(pool_id)
            try:
                data = api._fetch_data(url + '&page=999')
                for prop in data: self._data[prop] = data[prop]
            except (errors.APIGetError, errors.JSONError):
                raise errors.PoolNotFoundError('The requested pool could ' +\
                    'not be found.')
            if 'posts' in data: del(data['posts'])
        if pool_data is not None:
            for prop in pool_data: self._data[prop] = pool_data[prop]

    @property
    def id(self):
        """Returns the pool's ID."""
        return self._data['id']
    @id.setter
    def id(self, value):
        self._data['id'] = value
    

    @property
    def name(self):
        """Returns the pool's name."""
        return self._data['name']
    @name.setter
    def name(self, value):
        self._data['name'] = value

    @property
    def name_normal(self):
        """Returns a user-friendly formatted version of the pool's name."""
        return self.name.replace('_',' ').title()

    @property
    def user_id(self):
        """Returns the ID of the user who created the pool."""
        return self._data['user_id']
    @user_id.setter
    def user_id(self, value):
        self._data['user_id'] = value

    @property
    def created_at(self):
        """Returns a dict of information on the pool's creation time."""
        return self._data['created_at']
    @created_at.setter
    def created_at(self, value):
        self._data['created_at'] = value

    @property
    def updated_at(self):
        """Returns a dict of information on the pool's last update."""
        return self._data['updated_at']
    @updated_at.setter
    def updated_at(self, value):
        self._data['updated_at'] = value

    @property
    def post_count(self):
        """Returns the number of posts in the pool."""
        return self._data['post_count']
    @post_count.setter
    def post_count(self, value):
        self._data['post_count'] = value

    @property
    def is_public(self):
        """Returns whether or not the pool is marked public."""
        return self._data['is_public']
    @is_public.setter
    def is_public(self, value):
        self._data['is_public'] = value

    @property
    def is_active(self):
        """Returns whether or not the pool is active."""
        return self._data['is_active']
    @is_active.setter
    def is_active(self, value):
        self._data['is_active'] = value

    @property
    def description(self):
        """Returns the pool's description."""
        return self._data['description']
    @description.setter
    def description(self, value):
        self._data['description'] = value

    @property
    def url(self):
        """Returns the site URL the pool can be found at."""
        return config.BASE_URL + 'pool/show/' + str(self.id)

    @property
    def posts(self):
        """Returns a generator of Post objects for the pool."""
        url = config.BASE_URL + 'pool/show.json?id=' + str(self.id)
        page = 1
        end = False
        while not end:
            try: rs = api._fetch_data(url + '&page=' + str(page))
            except (errors.APIGetError, errors.JSONError):
                yield None
                return
            for post_data in rs['posts']:
                yield post.Post(post_data=post_data)
            if rs is None or len(rs['posts']) == 0:
                end = True
                break
            page += 1

    def dump_data(self):
        """Returns a dict of all data stored locally for this object.
        This does not include the list of posts.

        :returns: All locally-stored pool data.
        :rtype: dict
        """
        return self._data
