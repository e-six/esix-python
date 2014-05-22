#!/usr/bin/env python3
"""
Comment class for the e621 API.
"""

from . import api, config, errors


def login(username,password):
    """Attemt to login to the site, store credentials if successful.

    :param username: Your username.
    :type username: str
    :param password: Your password.
    :type password: str
    :returns: Your user object.
    :rtype: user.User
    """
    result = api._get_data_obj(api._post_data(
        {
            'name':str(username),
            'password':str(password)
        },
        config.BASE_URL + 'user/login.json'))
    if 'success' in result and result['success'] == 'failed':
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
    for user_data in api._get_data_obj(api._get_page(url)):
        yield User(user_data=user_data)


class User(object):
    def __init__(self, user_id=None, user_data=None):
        """Create an instance of a user.

        :param user_id: The user's ID number.
        :type uesr_id: int
        :param user_data: Raw data to be loaded directly into the object.
        :type user_data: dict
        """
        self._data = {}
        for prop in ['id', 'name', 'level', 'created_at',
                     'blacklisted', 'subscriptions']:
            self._data[prop] = None
        if user_id is None and user_data is None: return
        if user_id is not None:
            try: int(user_id)
            except ValueError: id_type = 'name'
            else: id_type = 'id'
            url = config.BASE_URL+'user/index.json?'+id_type+'='+str(user_id)
            user_list = api._get_data_obj(api._get_page(url))
            if len(user_list) == 0:
                raise errors.UserNotFoundError('User '+str(user_id)+\
                                               ' not found.')
            else: user_data = user_list[0]
        for prop in user_data: self._data[prop] = user_data[prop]

    @property
    def id(self):
        """Returns the user's ID number."""
        return self._data['id']

    @property
    def name(self):
        """Returns the user's username."""
        return self._data['name']

    @property
    def level(self):
        """Returns the user's site level."""
        return self._data['level']

    @property
    def created_at(self):
        """Returns a formatted string of the user's join date."""
        return self._data['created_at']

    @property
    def blacklisted(self):
        """Returns a list of tag groups the user has blacklisted."""
        return self._data['blacklisted']

    @property
    def subscriptions(self):
        """Returns a dict of tag subscriptions by the user."""
        return self._data['subscriptions']

    @property
    def tag_history(self):
        """Returns a generator of tag changes made by the user."""
        url = config.BASE_URL + 'post_tag_history/index.json?' +\
              'user_id='+str(self.id)
        for tag_change in api._get_data_obj(api._get_page(url)):
            yield tag_change

    @property
    def flag_history(self):
        """Returns a generator of post flags made by the user."""
        url = config.BASE_URL + 'post_flag_history/index.json?' +\
              'user_id='+str(self.id)
        for flag in api._get_data_obj(api._get_page(url)):
            yield flag
