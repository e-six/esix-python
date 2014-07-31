#!/usr/bin/env python3
"""
Comment class for the e621 API.
"""

from . import api, config, errors


def recent():
    """Get a list of the 25 most recent comments made site-wide.

    :returns: A generator of comment objects for the most recent comments.
    :rtype: generator object
    """
    url = config.BASE_URL + 'comment/index.json'
    for comment_data in api._fetch_data(url):
        yield Comment(comment_data=comment_data)

def submit(post_id, body):
    """Create and submit a comment on a post.

    :param post_id: The ID number of the post to comment on.
    :type post_id: int
    :param body: The comment body.
    :type body: str
    :returns: The JSON result of the comment submit request
    :rtype: dict
    """
    comment = Comment(comment_data = {
        'post_id': post_id,
        'body': body
        })
    return comment.submit()


class Comment(object):
    def __init__(self, comment_id=None, comment_data=None):
        """Create an instance of a comment.

        :param comment_id: The comment's ID number, for retrieving online.
        :type comment_id: int
        :param comment_data: Raw comment data, for loading directly into object.
        :type comment_data: dict
        :raises: errors.CommentNotFoundError
        """
        self._data = {}
        for prop in ['creator', 'post_id', 'created_at', 'id',
                     'body', 'score', 'creator_id']:
            self._data[prop] = None
        if comment_id is not None:
            try:
                data = api._get_data_obj(api._post_data({'id':str(comment_id)},
                    config.BASE_URL + 'comment/show.json'))
                for prop in data: self._data[prop] = data[prop]
            except (errors.APIPostError, errors.JSONError):
                raise errors.CommentNotFoundError('The requested comment ' +\
                    'could not be found.')
        if comment_data is not None:
            for prop in comment_data: self._data[prop] = comment_data[prop]

    @property
    def id(self):
        """Returns the comment ID."""
        return self._data['id']
    @id.setter
    def id(self, value):
        self._data['id'] = value

    @property
    def creator_id(self):
        """Returns the user ID of the comment author."""
        return self._data['creator_id']
    @creator_id.setter
    def creator_id(self, value):
        self._data['creator_id'] = value

    @property
    def creator(self):
        """Returns the username of the comment author."""
        return self._data['creator']
    @creator.setter
    def creator(self, value):
        self._data['creator'] = value

    @property
    def post_id(self):
        """Returns the ID of the post the comment was made on."""
        return self._data['post_id']
    @post_id.setter
    def post_id(self, value):
        self._data['post_id'] = value

    @property
    def created_at(self):
        """Returns a formatted string of the comment's post time."""
        return self._data['created_at']
    @created_at.setter
    def created_at(self, value):
        self._data['created_at'] = value

    @property
    def body(self):
        """Returns the comment body as entered by the author."""
        return self._data['body']
    @body.setter
    def body(self, value):
        self._data['body'] = value

    @property
    def score(self):
        """Returns the comment's score."""
        return self._data['score']
    @score.setter
    def score(self, value):
        self._data['score'] = value

    @property
    def url(self):
        """Returns the site URL the comment can be found at."""
        return config.BASE_URL + 'comment/show/' + str(self.id)

    def submit(self):
        """Posts this comment to the site. Must be logged in.

        :returns: Whether the post was successful.
        :rtype: bool
        :raises: errors.APIUnauthorizedError
        """
        if not config.USERNAME and not config.PASSWORD:
            raise errors.APIUnauthorizedError('You must be logged in to ' +\
                'post a comment.')
        data = {
            'comment[post_id]':str(self.post_id),
            'comment[body]':str(self.body),
            'login':str(config.USERNAME),
            'password_hash':str(config.PASSWORD)
        }
        return api._get_data_obj(
            api._post_data(data, config.BASE_URL + 'comment/create.json'))

    def dump_data(self):
        """Returns a dict of all data stored locally for this object.

        :returns: All locally-stored comment data.
        :rtype: dict
        """
        return self._data
