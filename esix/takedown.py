#!/usr/bin/env python3
"""
Takedown class for the e621 API.
"""

from . import api, config, errors, user


class Takedown(object):
    def __init__(self, takedown_id=None, takedown_data=None):
        """Create an instance of a takedown request.

        :param takedown_id: The ID number of the tag to fetch online.
        :type takedown_id: int
        :param takedown_data: Raw data to load directly into the object.
        :type takedown_data: dict
        :raises: errors.TakedownNotFoundError
        """
        self._data = {}
        for prop in ['id', 'source', 'posts', 'status', 'email',
                     'created_at', 'updated_at', 'reason',
                     'notes', 'approver', 'vericode',
                     'ip_addr', 'hidereason', 'delposts']:
            self._data[prop] = None
        if takedown_id is not None:
            try:
                data = api._fetch_data(
                    config.BASE_URL + 'takedown/show.json?id=' + \
                    str(takedown_id)
                )
                for prop in data: self._data[prop] = data[prop]
            except errors.JSONError:
                raise errors.TakedownNotFoundError('The requested takedown ' +\
                    'could not be found.')
        if takedown_data is not None:
            for prop in takedown_data: self._data[prop] = takedown_data[prop]

    @property
    def id(self):
        """Returns the ID number of the takedown."""
        return self._data['id']
    @id.setter
    def id(self, value):
        self._data['id'] = value

    @property
    def source(self):
        """Returns the source posted by the user."""
        return self._data['source']
    @source.setter
    def source(self, value):
        self._data['source'] = value

    @property
    def status(self):
        """Return the current status of the takedown."""
        return self._data['status']
    @status.setter
    def status(self, value):
        self._data['status'] = value

    @property
    def email(self):
        """Return the takedown submitter's email."""
        return self._data['email']
    @email.setter
    def email(self, value):
        self._data['email'] = value

    @property
    def created_at(self):
        """Returns a time object for when the takedown was submitted."""
        return self._data['created_at']
    @created_at.setter
    def created_at(self, value):
        self._data['created_at'] = value

    @property
    def updated_at(self):
        """Return a time object for the last edit of the request."""
        return self._data['updated_at']
    @updated_at.setter
    def updated_at(self, value):
        self._data['updated_at'] = value

    @property
    def reason(self):
        """Return the specified reason for the takedown request."""
        return self._data['reason']
    @reason.setter
    def reason(self, value):
        self._data['reason'] = value

    @property
    def notes(self):
        """Return any moderator notes on the request."""
        return self._data['notes']
    @notes.setter
    def notes(self, value):
        self._data['notes'] = value

    @property
    def approver(self):
        """Return the user ID of the request's approver."""
        if not self._data['approver']: return None
        return user.User(self._data['approver'])
    @approver.setter
    def approver(self, value):
        self._data['approver'] = value

    @property
    def vericode(self):
        """Return the unique code to verify the takedown."""
        return self._data['vericode']
    @vericode.setter
    def vericode(self, value):
        self._data['vericode'] = value

    @property
    def ip_addr(self):
        """Return the request submitter's IP address."""
        return self._data['ip_addr']
    @ip_addr.setter
    def ip_addr(self, value):
        self._data['ip_addr'] = value

    @property
    def hidereason(self):
        """Return whether or not the submitter hid the reason."""
        return self._data['hidereason']
    @hidereason.setter
    def hidereason(self, value):
        self._data['hidereason'] = value

    @property
    def delposts(self):
        """Return a list of IDs for deleted posts."""
        if not self._data['delposts']: return []
        return self._data['delposts'].split()
    @delposts.setter
    def delposts(self, value):
        self._data['delposts'] = value

    @property
    def posts(self):
        """Return a list of IDs for posts that were not removed."""
        if not self._data['posts']: return []
        return self._data['posts'].split()
    @posts.setter
    def posts(self, value):
        self._data['posts'] = value

    @property
    def url(self):
        """Returns the site URL the takedown can be found at."""
        return config.BASE_URL + 'takedown/show/' + str(self.id)

    def dump_data(self):
        """Returns a dict of all data stored locally for this object.

        :returns: All locally-stored takedown data.
        :rtype: dict
        """
        return self._data
