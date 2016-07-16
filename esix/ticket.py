#!/usr/bin/env python3
"""
Ticket class for the e621 API.
"""

from . import api, config, errors

def recent(page=1, limit=2):
    """Return a generator of recently created tickets.

    :param page: The page to begin on, assuming 50 tickets per page.
    :type page: int
    :param limit: The maximum pages of tickets to return.
    :type limit: int
    :returns: A generator of tickets matching the query.
    :rtype: generator object
    """
    url = config.BASE_URL + 'ticket/index.json'
    result = 0
    end = False
    while not end:
        rs = api._fetch_data(url + '?page=' + str(page))
        result += len(rs)
        for ticket_data in rs:
            yield Ticket(ticket_data=ticket_data)
        if rs is None or len(rs) == 0 or (limit and result > limit*50):
            end = True
            break
        page += 1


class Ticket(object):
    def __init__(self, ticket_id=None, ticket_data=None):
        """Create an instance of a ticket.

        :param ticket_id: The ID number of the ticket to fetch online.
        :type ticket_id: int
        :param ticket_data: Raw data to load directly into the object.
        :type ticket_data: dict
        :raises: errors.TicketNotFoundError
        """
        self._data = {}
        for prop in ['id', 'type', 'status', 'user', 'username', 'created_at',
                     'updated_at', 'desired_username', 'oldname', 'reason',
                     'reported_comment', 'handled_by', 'handled_by_name',
                     'reported_forum', 'response']:
            self._data[prop] = None
        if ticket_id is not None:
            try:
                data = api._fetch_data(
                    config.BASE_URL + 'ticket/show.json?id=' + str(ticket_id))
            except (errors.APIGetError, errors.JSONError):
                raise errors.TicketNotFoundError('The requested ticket ' +\
                    'could not be found.')
            else:
                for prop in data: self._data[prop] = data[prop]
        if ticket_data is not None:
            for prop in ticket_data: self._data[prop] = ticket_data[prop]

    @property
    def id(self):
        return self._data['id']
    @id.setter
    def id(self, value):
        self._data['id'] = value

    @property
    def type(self):
        return self._data['type']
    @type.setter
    def type(self, value):
        self._data['type'] = value

    @property
    def status(self):
        return self._data['status']
    @status.setter
    def status(self, value):
        self._data['status'] = value

    @property
    def user(self):
        return self._data['user']
    @user.setter
    def user(self, value):
        self._data['user'] = value

    @property
    def username(self):
        return self._data['username']
    @username.setter
    def username(self, value):
        self._data['username'] = value

    @property
    def created_at(self):
        return self._data['created_at']
    @created_at.setter
    def created_at(self, value):
        self._data['created_at'] = value

    @property
    def updated_at(self):
        return self._data['updated_at']
    @updated_at.setter
    def updated_at(self, value):
        self._data['updated_at'] = value

    @property
    def desired_username(self):
        return self._data['desired_username']
    @desired_username.setter
    def desired_username(self, value):
        self._data['desired_username'] = value

    @property
    def oldname(self):
        return self._data['oldname']
    @oldname.setter
    def oldname(self, value):
        self._data['oldname'] = value

    @property
    def reason(self):
        return self._data['reason']
    @reason.setter
    def reason(self, value):
        self._data['reason'] = value

    @property
    def reported_comment(self):
        return self._data['reported_comment']
    @reported_comment.setter
    def reported_comment(self, value):
        self._data['reported_comment'] = value

    @property
    def handled_by(self):
        return self._data['handled_by']
    @handled_by.setter
    def handled_by(self, value):
        self._data['handled_by'] = value

    @property
    def handled_by_name(self):
        return self._data['handled_by_name']
    @handled_by_name.setter
    def handled_by_name(self, value):
        self._data['handled_by_name'] = value

    @property
    def reported_forum(self):
        return self._data['reported_forum']
    @reported_forum.setter
    def reported_forum(self, value):
        self._data['reported_forum'] = value

    @property
    def response(self):
        return self._data['response']
    @response.setter
    def response(self, value):
        self._data['response'] = value

    def dump_data(self):
        """Returns a dict of all data stored locally for this object.

        :returns: All locally-stored ticket data.
        :rtype: dict
        """
        return self._data
