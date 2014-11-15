#!/usr/bin/env python3
"""
News class for the e621 API.
"""

from . import api, config, errors, user


class News(object):
    def __init__(self, news_id=None, news_data=None):
        """Create an instance of a news post.

        :param news_id: The ID number of the tag to fetch online.
        :type news_id: int
        :param news_data: Raw data to load directly into the object.
        :type news_data: dict
        :raises: errors.NewsNotFoundError
        """
        self._data = {}
        for prop in ['id', 'user_id', 'created_at', 'updated_at', 'post']:
            self._data[prop] = None
        if news_id is not None:
            try:
                data = api._fetch_data(
                    config.BASE_URL + '/news/show.json?id=' + \
                    str(news_id)
                )
                for prop in data: self._data[prop] = data[prop]
            except errors.JSONError:
                raise errors.NewsNotFoundError('The requested news post ' +\
                    'could not be found.')
        if news_data is not None:
            for prop in news_data: self._data[prop] = news_data[prop]

    @property
    def url(self):
        """Returns the site URL the news post can be found at."""
        return config.BASE_URL + 'news/show/' + str(self.id)

    def dump_data(self):
        """Returns a dict of all data stored locally for this object.

        :returns: All locally-stored news data.
        :rtype: dict
        """
        return self._data
