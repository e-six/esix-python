#!/usr/bin/env python3
"""
Tag class for the e621 API.
"""

from . import api, config, errors

def all_tags(page=1, limit=2):
    """Return a generator of all site tags.

    :param page: The page to begin on, assuming 50 tags per page.
    :type page: int
    :param limit: The maximum pages of tags to return.
    :type limit: int
    :returns: A generator of tags matching the query.
    :rtype: generator object
    """
    url = config.BASE_URL + 'tag/index.json?order=name'
    result = 0
    end = False
    while not end:
        rs = api._fetch_data(url + '&page=' + str(page))
        result += len(rs)
        for tag_data in rs:
            yield Tag(tag_data=tag_data)
        if rs is None or len(rs) == 0 or (limit and result > limit*50):
            end = True
            break
        page += 1


class Tag(object):
    def __init__(self, tag_id=None, tag_data=None):
        """Create an instance of a tag.

        :param tag_id: The ID number of the tag to fetch online.
        :type tag_id: int
        :param tag_data: Raw data to load directly into the object.
        :type tag_data: dict
        :raises: errors.TagNotFoundError
        """
        self._data = {}
        for prop in ['id', 'name', 'ambiguous', 'type', 'count']:
            self._data[prop] = None
        if tag_id is not None:
            try: int(tag_id)
            except ValueError: id_type = 'name'
            else: id_type = 'id'
            url = config.BASE_URL + 'tag/index.json?' +\
                id_type + '=' + str(tag_id)
            tag_list = api._fetch_data(url)
            if len(tag_list) == 0:
                raise errors.TagNotFoundError('The requested tag ' +\
                    'could not be found.')
            else:
                data = tag_list[0]
                for prop in data: self._data[prop] = data[prop]
        if tag_data is not None:
            for prop in tag_data: self._data[prop] = tag_data[prop]

    @property
    def id(self):
        """Returns the ID number of the tag."""
        return self._data['id']
    @id.setter
    def id(self, value):
        self._data['id'] = value

    @property
    def name(self):
        """Returns the name of the tag."""
        return self._data['name']
    @name.setter
    def name(self, value):
        self._data['name'] = value

    @property
    def ambiguous(self):
        """Returns whether or not the tag is set as ambiguous."""
        return self._data['ambiguous']
    @ambiguous.setter
    def ambiguous(self, value):
        self._data['ambiguous'] = value

    @property
    def type(self):
        """Returns the integer type of the tag: 0(general), 1(artist),
        3(copyright), 4(character), 5(species)
        """
        return self._data['type']
    @type.setter
    def type(self, value):
        self._data['type'] = value

    @property
    def type_str(self):
        """Returns the tag type: general, artist, copyright,
        character, species
        """
        try:
            return {
                0: 'general',
                1: 'artist',
                3: 'copyright',
                4: 'character',
                5: 'species'
                }[self._data['type']]
        except: return None

    @property
    def count(self):
        """Returns the number of occurrences of this tag."""
        return self._data['count']
    @count.setter
    def count(self, value):
        self._data['count'] = value

    @property
    def related(self):
        """Returns a generator of related tags."""
        url = config.BASE_URL + 'tag/related.json?tags=' + str(self.name)
        for tag in api._fetch_data(url)[self.name][1::]:
            yield Tag(tag[0])

    def dump_data(self):
        """Returns a dict of all data stored locally for this object.
        This does not include the result of type_str or related tags.

        :returns: All locally-stored tag data.
        :rtype: dict
        """
        return self._data
