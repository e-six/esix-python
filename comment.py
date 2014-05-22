#!/usr/bin/env python3
"""
Comment class for the e621 API.
"""

from . import api, config, errors


def recent_comments():
    """Get a list of the 25 most recent comments made site-wide.

    :returns: A generator of comment objects for the most recent comments.
    :rtype: generator object
    """
    url = config.BASE_URL + 'comment/index.json'
    for comment_data in api._get_data_obj(api._get_page(url)):
        yield Comment(comment_data=comment_data)


class Comment(object):
    def __init__(self, comment_id=None, comment_data=None):
        """Create an instance of a comment.

        :param comment_id: The comment's ID number, for retrieving online.
        :type comment_id: int
        :param comment_data: Raw comment data, for loading directly into object.
        :type comment_data: dict
        """
        self._data = {}
        for prop in ['creator', 'post_id', 'created_at', 'id',
                     'body', 'score', 'creator_id']:
            self._data[prop] = None
        if comment_id is None and comment_data is None: return
        if comment_id is not None:
            if not config.USERNAME and not config.PASSWORD:
                raise errors.APIUnauthorizedError('You must be logged in to ' +\
                                                  'find a comment by ID.')
            comment_data = api._get_data_obj(api._post_data(
                {
                    'id':str(comment_id),
                    'login':str(config.USERNAME),
                    'password_hash':str(config.PASSWORD)
                },
                config.BASE_URL + 'comment/show.json')) or self._data
        for prop in comment_data: self._data[prop] = comment_data[prop]

    @property
    def id(self):
        """Returns the comment ID."""
        return self._data['id']

    @property
    def creator_id(self):
        """Returns the user ID of the comment author."""
        return self._data['creator_id']

    @property
    def creator(self):
        """Returns the username of the comment author."""
        return self._data['creator']

    @property
    def post_id(self):
        """Returns the ID of the post the comment was made on."""
        return self._data['post_id']

    @property
    def created_at(self):
        """Returns a formatted string of the comment's post time."""
        return self._data['created_at']

    @property
    def body(self):
        """Returns the comment body as entered by the author."""
        return self._data['body']

    @property
    def score(self):
        """Returns the comment's score."""
        return self._data['score']

    def submit(self):
        """Posts this comment to the site. Must be logged in.

        :returns: Whether the post was successful.
        :rtype: bool
        """
        raise errors.APIException('Function not ready. Need to test.')
        data = {
            'post_id':str(self.id),
            'comment':str(self.body),
            'login':str(config.USERNAME),
            'password_hash':str(config.PASSWORD)
        }
        return api._get_data_obj(
            api._post_data(data,config.BASE_URL+'comment/create.json'))
