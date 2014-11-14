#!/usr/bin/env python3
"""
Comment class for the e621 API.
"""

from . import api, config, errors


def login(username, password):
    """Attemt to login to the site, store credentials if successful.

    :param username: Your username.
    :type username: str
    :param password: Your password.
    :type password: str
    :returns: Your user object.
    :rtype: user.User
    :raises: errors.APILoginError
    """
    result = api._get_data_obj(api._post_data(
        {
            'name':str(username),
            'password':str(password)
        },
        config.BASE_URL + 'user/login.json'))
    if 'success' in result and result['success'] in ('failed', False):
        if 'reason' in result:
            raise errors.APILoginError('Login failed: ' + str(result['reason']))
        else:
            raise errors.APILoginError('Login failed, '+\
                                       'incorrect username or password.')
    if not 'password_hash' in result:
        config.USERNAME, config.PASSWORD = ('','')
        raise errors.APILoginError('Login failed, password hash not retrieved.')
    config.USERNAME = result['name']
    config.PASSWORD = result['password_hash']
    return User(result['name'])

def search(user_id):
    """Search for users by ID or username.

    :param user_id: The ID number or username of the user to search for.
    :type user_id: int or str
    :returns: A generator of objects for matching users.
    :rtype: generator object
    """
    try: int(user_id)
    except ValueError: id_type = 'name'
    else: id_type = 'id'
    url = config.BASE_URL + 'user/index.json?' + id_type + '=' + str(user_id)
    for user_data in api._fetch_data(url):
        yield User(user_data=user_data)


class User(object):
    def __init__(self, user_id=None, user_data=None):
        """Create an instance of a user.

        :param user_id: The user's ID number.
        :type uesr_id: int
        :param user_data: Raw data to be loaded directly into the object.
        :type user_data: dict
        :raises: errors.UserNotFoundError
        """
        self._data = {}
        for prop in ['id', 'name', 'level', 'created_at', 'subscriptions']:
            self._data[prop] = None
        if user_id is not None:
            try: int(user_id)
            except ValueError: id_type = 'name'
            else: id_type = 'id'
            url = config.BASE_URL + 'user/index.json?' +\
                id_type + '=' + str(user_id)
            user_list = api._fetch_data(url)
            if len(user_list) == 0:
                raise errors.UserNotFoundError('User ' + str(user_id) +\
                                               ' not found.')
            else:
                data = user_list[0]
                for prop in data: self._data[prop] = data[prop]
        if user_data is not None:
            for prop in user_data: self._data[prop] = user_data[prop]

    @property
    def id(self):
        """Returns the user's ID number."""
        return self._data['id']
    @id.setter
    def id(self, value):
        self._data['id'] = value

    @property
    def name(self):
        """Returns the user's username."""
        return self._data['name']
    @name.setter
    def name(self, value):
        self._data['name'] = value

    @property
    def level(self):
        """Returns the user's site level."""
        return self._data['level']
    @level.setter
    def level(self, value):
        self._data['level'] = value

    @property
    def created_at(self):
        """Returns a formatted string of the user's join date."""
        return self._data['created_at']
    @created_at.setter
    def created_at(self, value):
        self._data['created_at'] = value

    @property
    def blacklisted(self):
        """Returned a list of tag groups the user has blacklisted.
        Now inactive as the API no longer supports this functionality.
        """
        return None

    @property
    def subscriptions(self):
        """Returns a dict of tag subscriptions by the user."""
        return self._data['subscriptions']
    @subscriptions.setter
    def subscriptions(self, value):
        self._data['subscriptions'] = value

    @property
    def url(self):
        """Returns the site URL the user's profile can be found at."""
        return config.BASE_URL + 'user/show/' + str(self.id)

    @property
    def tag_history(self):
        """Returns a generator of tag changes made by the user."""
        url = config.BASE_URL + 'post_tag_history/index.json?' +\
              'user_id=' + str(self.id)
        for tag_change in api._fetch_data(url):
            yield tag_change

    @property
    def flag_history(self):
        """Returns a generator of post flags made by the user."""
        url = config.BASE_URL + 'post_flag_history/index.json?' +\
              'user_id=' + str(self.id)
        for flag in api._fetch_data(url):
            yield flag

    def dump_data(self):
        """Returns a dict of all data stored locally for this object.
        This does not include tag history or flag history.

        :returns: All locally-stored user data.
        :rtype: dict
        """
        return self._data
