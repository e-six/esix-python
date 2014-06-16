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
        for prop in ['id',  'creator',  'creator_id',
                     'parent_id',  'title',    'body']:
            self._data[prop] = None
        if post_id is None and post_data is None: return
        if post_id is not None:
            url = config.BASE_URL + 'forum/show.json?id='+str(post_id)
            try: post_data = api._get_data_obj(api._get_page(url))
            except errors.APIGetError:
                raise errors.ForumPostNotFoundError('The requested forum ' +\
                    'post could not be found.')
        for prop in post_data: self._data[prop] = post_data[prop]

    @property
    def id(self):
        """Returns the ID number of the post."""
        return self._data['id']
    @id.setter
    def id(self, value):
        self._data['id'] = value

    @property
    def creator(self):
        """Returns the username of the poster."""
        return self._data['creator']
    @creator.setter
    def creator(self, value):
        self._data['creator'] = value

    @property
    def creator_id(self):
        """Returns the ID number of the poster."""
        return self._data['creator_id']
    @creator_id.setter
    def creator_id(self, value):
        self._data['creator_id'] = value

    @property
    def parent_id(self):
        """Returns the ID of the parent thread."""
        return self._data['parent_id']
    @parent_id.setter(self, value):
        self._data['parent_id'] = value

    @property
    def title(self):
        """Returns the title of the post."""
        return self._data['title']
    @title.setter
    def title(self, value):
        self._data['title'] = value

    @property
    def body(self):
        """Returns the post's body."""
        return self._data['body']
    @body.setter
    def body(self, value):
        self._data['body'] = value

    @property
    def parent(self):
        """Returns an object for the post's parent thread."""
        return Thread(self.parent_id)


class Thread(object):
    def __init__(self, thread_id=None, thread_data=None):
        pass
