#!/usr/bin/env python3
"""
Post class for the e621 API.
"""

from . import api, config, errors, comment, user


def recent_posts(limit=75):
    """Fetch the most recent posts from the site.

    :param limit: The number of posts to fetch, up to 100. Default 75.
    :type limit: int
    :returns: A generator of the most recent posts.
    :rtype: generator object
    """
    url = config.BASE_URL + 'post/index.json?limit=' + str(limit)
    for post_data in api._get_data_obj(api._get_page(url)):
        yield Post(post_data=post_data)

def search(query,limit=75):
    """Run a search and return a list of the resulting images.

    :param query: The tag search query.
    :type query: str
    :param limit: Number of posts to fetch per page. Default 75.
    :type limit: int
    :returns: A generator of images matching the query.
    :rtype: generator object
    """
    try: limit = int(limit)
    except: limit = 75
    if not limit >= 0: limit = 75
    url = config.BASE_URL + 'post/index.json?tags=' + str(query) +\
        '&limit=' + (str(limit) if limit > 0 else '100')
    result = 0
    page = 1
    end = False
    while not end:
        rs = api._get_data_obj(api._get_page(url+'&page='+str(page)))
        result += len(rs)
        for post_data in rs:
            yield Post(post_data=post_data)
        if rs is None or len(rs) == 0 or (limit and result >= limit):
            end = True
            break
        page += 1

def popular_by_day(year=None,month=None,day=None):
    """Get a list of popular posts for a single day.

    :param year: Optional, the year to search.
    :type year: int
    :param month: Optional, the month to search.
    :type month: int
    :param day: Optional, the day to search.
    :type day: int
    :returns: A generator of up to 32 popular posts for the specified day.
    :rtype: generator object
    """
    url = config.BASE_URL + 'post/popular_by_day.json'
    if day and month and year:
        url += '?day='+str(day)+'&month='+str(month)+'&year='+str(year)
    for post_data in api._get_data_obj(api._get_page(url)):
        yield Post(post_data=post_data)

def popular_by_week(year=None,month=None,day=None):
    """Get a list of popular posts for a single week.

    :param year: Optional, the year to search.
    :type year: int
    :param month: Optional, the month to search.
    :type month: int
    :param day: Optional, the day of the start of the week.
    :type day: int
    :returns: A generator of up to 32 popular posts for the specified week.
    :rtype: generator object
    """
    url = config.BASE_URL + 'post/popular_by_week.json'
    if day and month and year:
        url += '?day='+str(day)+'&month='+str(month)+'&year='+str(year)
    for post_data in api._get_data_obj(api._get_page(url)):
        yield Post(post_data=post_data)

def popular_by_month(year=None,month=None):
    """Get a list of popular posts for a single week.

    :param year: Optional, the year to search.
    :type year: int
    :param month: Optional, the month to search.
    :type month: int
    :returns: A generator of up to 32 popular posts for the specified month.
    :rtype: generator object
    """
    url = config.BASE_URL + 'post/popular_by_month.json'
    if month and year:
        url += '?day='+str(day)+'&month='+str(month)+'&year='+str(year)
    for post_data in api._get_data_obj(api._get_page(url)):
        yield Post(post_data=post_data)


class Post(object):
    def __init__(self, post_id=None, post_data=None):
        """Create an instance of a post.

        :param post_id: The post's ID number, for retrieving from the site.
        :type post_id: int
        :param post_data: Raw post data to be loaded directly into the object.
        :type post_data: dict
        """
        self._data = {}
        for prop in ['sources', 'file_ext', 'sample_width',
                     'sample_height', 'children', 'preview_url',
                     'status', 'parent_id', 'md5', 'source', 'id',
                     'score', 'preview_height', 'file_url', 'author',
                     'description', 'has_notes', 'has_children',
                     'sample_url', 'tags', 'has_comments', 'file_size',
                     'created_at', 'change', 'height', 'width',
                     'preview_width', 'creator_id', 'rating']:
            self._data[prop] = None
        if post_id is None and post_data is None: return
        if post_id is not None:
            post_data = api._get_data_obj(api._get_page(
                config.BASE_URL + '/post/show.json?id=' + str(post_id)
            ))
        for prop in post_data: self._data[prop] = post_data[prop]

    @property
    def id(self):
        """Returns the ID number of the post."""
        return self._data['id']

    @property
    def author(self):
        """Returns the username of the uploader."""
        return self._data['author']

    @property
    def creator_id(self):
        """Returns the user ID of the uploader."""
        return self._data['creator_id']

    @property
    def created_at(self):
        """Returns when the post was uploaded."""
        return self._data['created_at']

    @property
    def status(self):
        """Returns the status of the post: active, flagged, pending, delted."""
        return self._data['status']

    @property
    def source(self):
        """Returns the post's first source."""
        return self._data['source']

    @property
    def sources(self):
        """Returns an array of the post's sources."""
        return self._data['sources']

    @property
    def tags(self):
        """Returns an array of the post's tags."""
        return self._data['tags'].split()

    @property
    def description(self):
        """Returns the post's description."""
        return self._data['description']

    @property
    def score(self):
        """Returns the post's score."""
        return self._data['score']

    @property
    def rating(self):
        """Returns the post's rating: e, q, s."""
        return self._data['rating']

    @property
    def parent_id(self):
        """Returns the post's parent post ID."""
        return self._data['parent_id']

    @property
    def has_children(self):
        """Returns whether or not the post has children."""
        return self._data['has_children']

    @property
    def children(self):
        """Returns an array of the post's children."""
        return self._data['children'].split(',')

    @property
    def has_notes(self):
        """Returns whether or not the post has any notes."""
        return self._data['has_notes']

    @property
    def has_comments(self):
        """Returns whether or not the post has any comments."""
        return self._data['has_comments']

    @property
    def md5(self):
        """Returns the post's md5 checksum."""
        return self._data['md5']

    @property
    def file_url(self):
        """Returns the URL of the image file."""
        return self._data['file_url']

    @property
    def file_ext(self):
        """Returns the file's extension: jpb, png, gif, swf."""
        return self._data['file_ext']

    @property
    def file_size(self):
        """Returns the size in byetes of the file."""
        return self._data['file_size']

    @property
    def width(self):
        """Returns the width of the image."""
        return self._data['width']

    @property
    def height(self):
        """Returns the height of the image."""
        return self._data['height']

    @property
    def sample_url(self):
        """Returns the URL of the scaled sample image."""
        return self._data['sample_url']

    @property
    def sample_width(self):
        """Returns the width of the sample image."""
        return self._data['sample_width']

    @property
    def sample_height(self):
        """Returns the height of the sample image."""
        return self._data['sample_height']

    @property
    def preview_url(self):
        """Returns the URL of the preview thumbnail."""
        return self._data['preview_url']

    @property
    def preview_width(self):
        """Returns the width of the preview thumbnail."""
        return self._data['preview_width']

    @property
    def preview_height(self):
        """Returns the height of the preview thumbnail."""
        return self._data['preview_height']

    @property
    def favorited_users(self):
        """Returns a generator of users who favorited this post"""
        url = config.BASE_URL + 'favorite/list_users.json?id=' + str(self.id)
        for username in api._get_data_obj(api._get_page(url))\
            ['favorited_users'].split(','):
            yield user.User(username)

    @property
    def tag_history(self):
        """Returns a generator of tag changes for this post."""
        url = config.BASE_URL + 'post_tag_history/index.json?post_id=' +\
              str(self.id)
        for tag_change in api._get_data_obj(api._get_page(url)):
            yield tag_change

    @property
    def flag_history(self):
        """Returns a generator of flags for this post."""
        url = config.BASE_URL + 'post_flag_history/index.json?post_id=' +\
              str(self.id)
        for flag in api._get_data_obj(api._get_page(url)): yield flag

    @property
    def comments(self):
        """Returns a generator of comments made on this post."""
        url = config.BASE_URL + 'comment/index.json?post_id=' + str(self.id)
        for comment_data in list(reversed(
            api._get_data_obj(api._get_page(url)))):
            yield comment.Comment(comment_data=comment_data)

    def vote_post(self,vote):
        """Upvote or downvote the post.

        :param vote: 1 for an upvote, -1 for a downvote.
        :type vote: int
        :returns: Whether the vote was successful.
        :rtype: bool
        """
        raise errors.APIException('Not ready. Unordered Collection error.')
        if str(vote) != '1' and str(vote) != '-1': return False
        data = {
            'id':str(self.id),
            'score':str(vote)
        }
        send_vote = api._get_data_obj(
            api._post_data(data,config.BASE_URL+'post/vote.json'))
        return send_vote
