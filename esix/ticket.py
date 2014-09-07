#!/usr/bin/env python3
"""
Ticket class for the e621 API.
"""

from . import api, config, errors

def recent(page=1, limit=2):
    """Return a generator of recently created tickets.

    :param page: The page to begin on, assuming 24 tickets per page.
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
        rs = api._fetch_data(url + '&page=' + str(page))
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
                    config.BASE_URL + '/ticket/show.json?id=' + str(ticket_id))
            except (errors.APIGetError, errors.JSONError):
                raise errors.TicketNotFoundError('The requested ticket ' +\
                    'could not be found.')
            else:
                for prop in data: self._data[prop] = data[prop]
        if ticket_data is not None:
            for prop in ticket_data: self._data[prop] = ticket_data[prop]

    @property
    def id(self):
        """Returns the ID number of the ticket."""
        return self._data['id']
    @id.setter
    def id(self, value):
        self._data['id'] = value

    def dump_data(self):
        """Returns a dict of all data stored locally for this object.

        :returns: All locally-stored ticket data.
        :rtype: dict
        """
        return self._data
