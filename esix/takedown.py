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
        """
        self._data = {}
        for prop in ['id', 'source', 'posts', 'status', 'email',
                     'created_at', 'updated_at', 'reason',
                     'notes', 'approver', 'vericode',
                     'ip_addr', 'hidereason', 'delposts']:
            self._data[prop] = None
        if takedown_id is None and takedown_data is None: return
        if takedown_id is not None:
            takedown_data = api._get_data_obj(api._get_page(
                config.BASE_URL + '/takedown/show.json?id=' + str(takedown_id)
            ))
        for prop in takedown_data: self._data[prop] = takedown_data[prop]

    @property
    def id(self):
        """Returns the ID number of the takedown."""
        return self._data['id']

    @property
    def source(self):
        """Returns the source posted by the user."""
        return self._data['source']

    @property
    def status(self):
        """Return the current status of the takedown."""
        return self._data['status']

    @property
    def email(self):
        """Return the takedown submitter's email."""
        return self._data['email']

    @property
    def created_at(self):
        """Returns a time object for when the takedown was submitted."""
        return self._data['created_at']

    @property
    def updated_at(self):
        """Return a time object for the last edit of the request."""
        return self._data['updated_at']

    @property
    def reason(self):
        """Return the specified reason for the takedown request."""
        return self._data['reason']

    @property
    def notes(self):
        """Return any moderator notes on the request."""
        return self._data['notes']

    @property
    def approver(self):
        """Return the user ID of the request's approver."""
        if not self._data['approver']: return None
        return user.User(self._data['approver'])

    @property
    def vericode(self):
        """Return the unique code to verify the takedown."""
        return self._data['vericode']

    @property
    def ip_addr(self):
        """Return the request submitter's IP address."""
        return self._data['ip_addr']

    @property
    def hidereason(self):
        """Return whether or not the submitter hid the reason."""
        return self._data['hidereason']

    @property
    def delposts(self):
        """Return a list of IDs for deleted posts."""
        if not self._data['delposts']: return []
        return self._data['delposts'].split()

    @property
    def posts(self):
        """Return a list of IDs for posts that were not removed."""
        if not self._data['posts']: return []
        return self._data['posts'].split()
