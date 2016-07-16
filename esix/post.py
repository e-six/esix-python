#!/usr/bin/env python3
"""
Post class for the e621 API.
"""

import hashlib
import json
import os

from . import api, config, errors, comment, user


def recent(limit=75):
    """Fetch the most recent posts from the site.

    :param limit: The number of posts to fetch, up to 100. Default 75.
    :type limit: int
    :returns: A generator of the most recent posts.
    :rtype: generator object
    """
    url = config.BASE_URL + 'post/index.json?limit=' + str(limit)
    for post_data in api._fetch_data(url):
        yield Post(post_data=post_data)

def search(query, limit=75):
    """Run a search and return a list of the resulting images.

    :param query: The tag search query.
    :type query: str
    :param limit: Number of posts to fetch. Default 75.
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
        rs = api._fetch_data(url + '&page=' + str(page))
        result += len(rs)
        for post_data in rs:
            yield Post(post_data=post_data)
        if rs is None or len(rs) == 0 or (limit and result >= limit):
            end = True
            break
        page += 1

def popular_by_day(year=None, month=None, day=None):
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
        url += '?day=' + str(day) + '&month=' + str(month) +\
            '&year=' + str(year)
    for post_data in api._fetch_data(url):
        yield Post(post_data=post_data)

def popular_by_week(year=None, month=None, day=None):
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
        url += '?day=' + str(day) + '&month=' + str(month) +\
            '&year=' + str(year)
    for post_data in api._fetch_data(url):
        yield Post(post_data=post_data)

def popular_by_month(year=None, month=None):
    """Get a list of popular posts for a single month.

    :param year: Optional, the year to search.
    :type year: int
    :param month: Optional, the month to search.
    :type month: int
    :returns: A generator of up to 32 popular posts for the specified month.
    :rtype: generator object
    """
    url = config.BASE_URL + 'post/popular_by_month.json'
    if month and year:
        url += '?month=' + str(month) + '&year=' + str(year)
    for post_data in api._fetch_data(url):
        yield Post(post_data=post_data)

def from_file(dir, filename):
    """Generate a Post object based on locally-stored information for a file.

    :param dir: The directory the image is stored in.
    :type dir: str
    :param filename: The name of the file to load
    :type filename: str
    :returns: A Post object based on the file.
    :rtype: post.Post object
    :raises: errors.BadPostError
    """
    if dir != "./" and not dir.endswith("/"): dir += "/"
    try:
        with open(dir + filename, 'rb') as f:
            md5 = hashlib.md5(f.read()).hexdigest()
    except:
        raise errors.BadPostError("An error occured loading the " +\
            "specified file's metadata.")
    try: data = json.load(open(dir + '.metadata/' + md5))
    except: raise errors.JSONError("An error occured parsing the JSON data.")
    return Post(post_data=data)


class Post(object):
    def __init__(self, post_id=None, post_data=None):
        """Create an instance of a post.

        :param post_id: The post's ID number, for retrieving from the site.
        :type post_id: int
        :param post_data: Raw post data to be loaded directly into the object.
        :type post_data: dict
        :raises: errors.PostNotFoundError
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
        if post_id is not None:
            try:
                data = api._fetch_data(
                    config.BASE_URL + 'post/show.json?id=' + str(post_id))
                for prop in data: self._data[prop] = data[prop]
            except (errors.APIGetError, errors.JSONError):
                raise errors.PostNotFoundError('The requested post could ' +\
                    'not be found.')
        if post_data is not None:
            for prop in post_data: self._data[prop] = post_data[prop]

    @property
    def id(self):
        """Returns the ID number of the post."""
        return self._data['id']
    @id.setter
    def id(self, value):
        self._data['id'] = value

    @property
    def author(self):
        """Returns the username of the uploader."""
        return self._data['author']
    @author.setter
    def author(self, value):
        self._data['author'] = value

    @property
    def creator_id(self):
        """Returns the user ID of the uploader."""
        return self._data['creator_id']
    @creator_id.setter
    def creator_id(self, value):
        self._data['creator_id'] = value

    @property
    def created_at(self):
        """Returns when the post was uploaded."""
        return self._data['created_at']
    @created_at.setter
    def created_at(self, value):
        self._data['created_at'] = value

    @property
    def status(self):
        """Returns the status of the post: active, flagged, pending, delted."""
        return self._data['status']
    @status.setter
    def status(self, value):
        self._data['status'] = value

    @property
    def source(self):
        """Returns the post's first source."""
        return self._data['source']
    @source.setter
    def source(self, value):
        self._data['source'] = value

    @property
    def sources(self):
        """Returns an array of the post's sources."""
        return self._data['sources']
    @sources.setter
    def sources(self, value):
        self._data['sources'] = value

    @property
    def tags(self):
        """Returns a space-separated string of the post's tags."""
        return self._data['tags']
    @tags.setter
    def tags(self, value):
        self._data['tags'] = value

    @property
    def description(self):
        """Returns the post's description."""
        return self._data['description']
    @description.setter
    def description(self, value):
        self._data['description'] = value

    @property
    def score(self):
        """Returns the post's score."""
        return self._data['score']
    @score.setter
    def score(self, value):
        self._data['score'] = value

    @property
    def rating(self):
        """Returns the post's rating: e, q, s."""
        return self._data['rating']
    @rating.setter
    def rating(self, value):
        self._data['rating'] = value

    @property
    def parent_id(self):
        """Returns the post's parent post ID."""
        return self._data['parent_id']
    @parent_id.setter
    def parent_id(self, value):
        self._data['parent_id'] = value

    @property
    def has_children(self):
        """Returns whether or not the post has children."""
        return self._data['has_children']
    @has_children.setter
    def has_children(self, value):
        self._data['has_children'] = value

    @property
    def children(self):
        """Returns a comma-separated string of the post's children."""
        return self._data['children']
    @children.setter
    def children(self, value):
        self._data['children'] = value

    @property
    def has_notes(self):
        """Returns whether or not the post has any notes."""
        return self._data['has_notes']
    @has_notes.setter
    def has_notes(self, value):
        self._data['has_notes'] = value

    @property
    def has_comments(self):
        """Returns whether or not the post has any comments."""
        return self._data['has_comments']
    @has_comments.setter
    def has_comments(self, value):
        self._data['has_comments'] = value

    @property
    def md5(self):
        """Returns the post's md5 checksum."""
        return self._data['md5']
    @md5.setter
    def md5(self, value):
        self._data['md5'] = value

    @property
    def file_url(self):
        """Returns the URL of the image file."""
        return self._data['file_url']
    @file_url.setter
    def file_url(self, value):
        self._data['file_url'] = value

    @property
    def file_ext(self):
        """Returns the file's extension: jpb, png, gif, swf."""
        return self._data['file_ext']
    @file_ext.setter
    def file_ext(self, value):
        self._data['file_ext'] = value

    @property
    def file_size(self):
        """Returns the size in byetes of the file."""
        return self._data['file_size']
    @file_size.setter
    def file_size(self, value):
        self._data['file_size'] = value

    @property
    def width(self):
        """Returns the width of the image."""
        return self._data['width']
    @width.setter
    def width(self, value):
        self._data['width'] = value

    @property
    def change(self):
        """Returns the timestamp of the post's last change."""
        return self._data['change']
    @change.setter
    def change(self, value):
        self._data['change'] = value

    @property
    def height(self):
        """Returns the height of the image."""
        return self._data['height']
    @height.setter
    def height(self, value):
        self._data['height'] = value

    @property
    def sample_url(self):
        """Returns the URL of the scaled sample image."""
        return self._data['sample_url']
    @sample_url.setter
    def sample_url(self, value):
        self._data['sample_url'] = value

    @property
    def sample_width(self):
        """Returns the width of the sample image."""
        return self._data['sample_width']
    @sample_width.setter
    def sample_width(self, value):
        self._data['sample_width'] = value

    @property
    def sample_height(self):
        """Returns the height of the sample image."""
        return self._data['sample_height']
    @sample_height.setter
    def sample_height(self, value):
        self._data['sample_height'] = value

    @property
    def preview_url(self):
        """Returns the URL of the preview thumbnail."""
        return self._data['preview_url']
    @preview_url.setter
    def preview_url(self, value):
        self._data['preview_url'] = value

    @property
    def preview_width(self):
        """Returns the width of the preview thumbnail."""
        return self._data['preview_width']
    @preview_width.setter
    def preview_width(self, value):
        self._data['preview_width'] = value

    @property
    def preview_height(self):
        """Returns the height of the preview thumbnail."""
        return self._data['preview_height']
    @preview_height.setter
    def preview_height(self, value):
        self._data['preview_height'] = value
    
    @property
    def url(self):
        """Returns the site URL the post can be found at."""
        return config.BASE_URL + 'post/show/' + str(self.id)

    @property
    def favorited_users(self):
        """Returns a generator of users who favorited this post"""
        url = config.BASE_URL + 'favorite/list_users.json?id=' + str(self.id)
        try: data = api._fetch_data(url)
        except (errors.APIGetError, errors.JSONError): return
        for username in data['favorited_users'].split(','):
            yield user.User(username)

    @property
    def tag_history(self):
        """Returns a generator of tag changes for this post."""
        url = config.BASE_URL + 'post_tag_history/index.json?post_id=' +\
              str(self.id)
        try: data = api._fetch_data(url)
        except errors.APIGetError: return
        for tag_change in data:
            yield tag_change

    @property
    def flag_history(self):
        """Returns a generator of flags for this post."""
        url = config.BASE_URL + 'post_flag_history/index.json?post_id=' +\
              str(self.id)
        try: data = api._fetch_data(url)
        except errors.APIGetError: return
        for flag in data: yield flag

    @property
    def comments(self):
        """Returns a generator of comments made on this post."""
        url = config.BASE_URL + 'comment/index.json?post_id=' + str(self.id)
        page = 1
        end = False
        while not end:
            try: rs = api._fetch_data(url + '&page=' + str(page))
            except errors.APIGetError: return
            for comment_data in rs:
                yield comment.Comment(comment_data=comment_data)
            if rs is None or len(rs) == 0:
                end = True
                break
            page += 1

    def vote(self, vote):
        """Upvote or downvote the post.

        :param vote: 1 for an upvote, -1 for a downvote.
        :type vote: int
        :returns: Whether the vote was successful.
        :rtype: bool
        :raises: errors.APIException
        """
        if str(vote) != '1' and str(vote) != '-1': return False
        if not config.USERNAME and not config.PASSWORD:
            raise errors.APIUnauthorizedError('You must be logged in to ' +\
                'vote on posts.')
        data = {
            'id':str(self.id),
            'score':str(vote),
            'login':str(config.USERNAME),
            'password_hash':str(config.PASSWORD)
        }
        send_vote = api._get_data_obj(
            api._post_data(data,config.BASE_URL + 'post/vote.json'))
        return send_vote

    def dump_data(self):
        """Returns a dict of all data stored locally for this object.
        This does not include favorited users, tag history, flag history
        or comments.

        :returns: All locally-stored post data.
        :rtype: dict
        """
        return self._data

    def download_metadata(self, dest, comments=False, pretty=False):
        """Save the post's information locally.

        :param dest: The directory in which metadata will be stored
            (in a .metadata/ subdirectory)
        :type dest: str
        :param comments: Whether or not the post's comments should be stored.
        :type comments: bool
        :param pretty: Whether or not to pretty print the data to the file.
        :type pretty: bool
        :returns: Whether or not the operation was successful.
        :rtype: bool
        """
        if dest != './' and not dest.endswith('/'): dest += '/'
        if not os.path.exists(dest): os.makedirs(dest)
        data = self._data
        data['comments'] = []
        if comments:
            for c in reversed(list(self.comments)): data['comments'].append(c.dump_data())
        try:
            with open(dest + self.md5, 'w') as meta_file:
                if pretty == True:
                    meta_file.write(json.dumps(data, indent=4, sort_keys=True))
                else:
                    meta_file.write(json.dumps(data))
            return True
        except: return False

    def download(self, dest='./', name_format="{md5}.{file_ext}", 
        overwrite=False, write_metadata=False):
        """Downloads the post object as an image.

        :param dest: The directory to download to. Default is script directory.
        :type dest: str
        :param name_format: The format of the filename, post data keywords
            should be surrounded by {}. Default {md5}.{file_ext}
        :type name_format: str
        :param overwrite: If True, will overwrite existing files with the
            same name. Default False.
        :type overwrite: bool
        :returns: Whether or not the download succeeded.
        :rtype: bool
        :raises: errors.BadPostError, errors.FileDownloadError
        """
        name_format = name_format.replace("{","%(").replace("}",")s")
        if dest != './' and not dest.endswith('/'): dest += '/'
        if self.file_url is None:
            raise errors.BadPostError('No file URL found.')
        filename = name_format % self._data
        if not filename.endswith("." + self.file_ext):
            filename += "." + self.file_ext
        file = api._get_page(self.file_url)
        if file and (not os.path.isfile(dest + filename) or overwrite):
            if file.headers['Content-Type'].lower() == 'text/html':
                raise errors.FileDownloadError('An error occured attempting ' +\
                    'to download the image.')
            if not os.path.isdir(dest): os.makedirs(dest)
            with open(dest + filename, 'wb') as out_file:
                for chunk in file.iter_content(chunk_size=1024):
                    if chunk:
                        out_file.write(chunk)
                        out_file.flush()
            if write_metadata: self.download_metadata(dest + '.metadata/')
            return True
        return False
