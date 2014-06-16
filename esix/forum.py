#!/usr/bin/env python3
"""
Forum class for the e621 API.
"""

from . import api, config, errors

def recent():
    """Return a generator of recent forum threads.

    :returns: A generator of thread objects.
    :rtype: generator object
    """
    pass


class Post(object):
    def __init__(self, post_id=None, post_data=None):
        """Create an instance of a forum post.

        :param post_id: The ID number of the tag to fetch online.
        :type post_id: int
        :param post_data: Raw data to load directly into the object.
        :type post_data: dict
        """
        self._data = {}
        for prop in []:
            self._data[prop] = None
        if post_id is None and post_data is None: return
        if post_id is not None:
            url = config.BASE_URL + 'forum/index.json?id='+str(post_id)
            try: post_data = api._get_data_obj(api._get_page(url))
            except errors.APIGetError:
                raise errors.ForumPostNotFoundError('The requested forum ' +\
                    'post could not be found.')
        for prop in post_data: self._data[prop] = post_data[prop]

    @property
    def id(self):
        """Returns the ID number of the tag."""
        return self._data['id']
    @id.setter
    def id(self, value):
        self._data['id'] = value


class Thread(object):
    pass
