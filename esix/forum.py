#!/usr/bin/env python3
"""
Forum class for the e621 API.
"""

from . import api, config, errors

def recent():
    """Return a generator of the 30 most recent forum threads.

    :returns: A generator of thread objects.
    :rtype: generator object
    """
    url = config.BASE_URL + 'forum/index.json'
    for thread_data in api._fetch_data(url):
        yield Thread(thread_data=thread_data)
    pass


class Post(object):
    def __init__(self, post_id=None, post_data=None):
        """Create an instance of a forum post.

        :param post_id: The ID number of the post to fetch online.
        :type post_id: int
        :param post_data: Raw data to load directly into the object.
        :type post_data: dict
        :raises: errors.ForumPostNotFoundError
        """
        self._data = {}
        for prop in ['id',  'creator',  'creator_id',
                     'parent_id',  'title',    'body']:
            self._data[prop] = None
        if post_id is not None:
            url = config.BASE_URL + 'forum/show.json?id=' + str(post_id)
            try:
                data = api._fetch_data(url)
                for prop in data: self._data[prop] = data[prop]
            except (errors.APIGetError, errors.JSONError):
                raise errors.ForumPostNotFoundError('The requested forum ' +\
                    'post could not be found.')
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
    @parent_id.setter
    def parent_id(self, value):
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

    @property
    def url(self):
        """Returns the site URL the forum post can be found at."""
        return config.BASE_URL + 'forum/show/' + str(self.id)

    def dump_data(self):
        """Returns a dict of all data stored locally for this object.

        :returns: All locally-stored forum post data.
        :rtype: dict
        """
        return self._data


class Thread(object):
    def __init__(self, thread_id=None, thread_data=None):
        """Create an instance of a forum thread.

        :param thread_id: The ID number of the thread to fetch online.
        :type thread_id: int
        :param thread_data: Raw data to load directly into the object.
        :type thread_data: dict
        :raises: errors.ForumPostNotFoundError
        """
        self._op = None
        self._replies = None
        if thread_id is not None:
            # Get OP data
            url = config.BASE_URL + 'forum/show.json?id=' + str(thread_id)
            try: self._op = Post(thread_id)
            except (errors.APIGetError, errors.JSONError):
                raise errors.ForumPostNotFoundError('The requested forum ' +\
                    'thread could not be found.')
            # Get replies data
            self._load_replies()
        if thread_data is not None:
            self._op = Post(post_data=thread_data)
            if 'replies' in thread_data:
                self._replies = []
                for post_data in thread_data['replies']:
                    self._replies.append(Post(post_data=post_data))
                self._replies = list(reversed(self._replies))

    def _load_replies(self):
        """Load all replies to this thread into a list"""
        url = config.BASE_URL + 'forum/index.json?parent_id=' + str(self.id)
        self._replies = []
        page = 1
        end = False
        while not end:
            rs = api._fetch_data(url + '&page=' + str(page))
            for post_data in rs: self._replies.append(Post(post_data=post_data))
            if rs is None or len(rs) == 0:
                end = True
                break
            page += 1
        self._replies = list(reversed(self._replies))

    @property
    def id(self):
        """Return the ID of the thread."""
        return self._op.id
    @id.setter
    def id(self, value):
        self._op.id = value
    
    @property
    def creator(self):
        """Return the thread's original poster."""
        return self._op.creator
    @creator.setter
    def creator(self, value):
        self._op.creator = value
    
    @property
    def creator_id(self):
        """Return the thread's creator's ID."""
        return self._op.creator_id
    @creator_id.setter
    def creator_id(self, value):
        self._op.creator_id = value
    
    @property
    def title(self):
        """Return the original thread title."""
        return self._op.title
    @title.setter
    def title(self, value):
        self._op.title = value
    
    @property
    def body(self):
        """Return the OP's body."""
        return self._op.body
    @body.setter
    def body(self, value):
        self._op.body = value

    @property
    def num_replies(self):
        """Return the number of replies the thread has (excluding the OP)."""
        if self._replies is None: self._load_replies()
        return len(self._replies)

    @property
    def url(self):
        """Returns the site URL the forum thread can be found at."""
        return config.BASE_URL + 'forum/show/' + str(self.id)
    
    @property
    def replies(self):
        """Return a generator of replies in the thread."""
        if self._replies is None:
            yield None
            return
        for r in self._replies:
            yield r

    def get_reply(self, index):
        """Return the given reply by index, None if it does not exist."""
        if index == 0: return self._op
        if self._replies is None: return None
        try: return self._replies[index-1]
        except: return None

    def dump_data(self):
        """Returns a dict of all data stored locally for this object.
        This does not include replies if they have not been loaded.

        :returns: All locally-stored forum thread data.
        :rtype: dict
        """
        return dict(self._op.dump_data(), **{
            'replies':[r.dump_data() for r in self.replies]
        })
