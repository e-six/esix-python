#
# POST-RELATED FUNCTIONS
#
def get_recent_posts(limit=75):
    """Fetch the most recent posts from the site.

    :param limit: The number of posts to fetch, up to 100. Default 75.
    :type limit: int
    :returns: A list of the most recent posts.
    :rtype: list
    """
    url = config.BASE_URL + 'post/index.json?limit=' + str(limit)
    return _get_data_obj(_get_page(url))

def search_posts(query,limit=75,verbose=False):
    """Run a search and return a list of the resulting images.

    :param query: The tag search query.
    :type query: str
    :param limit: Number of posts to fetch, 0 for no limit. Default 75.
    :type limit: int
    :param verbose: If True, will print the current page number.
    :type verbose: bool
    :returns: A list of images matching the query.
    :rtype: list
    """
    try: limit = int(limit)
    except: limit = 75
    if not limit >= 0: limit = 75
    result = []
    url = config.BASE_URL + 'post/index.json?tags=' + str(query) +\
        '&limit=' + (str(limit) if limit else '100')
    page = 1
    end = False
    while not end:
        rs = _get_data_obj(_get_page(url+'&page='+str(page)))
        if rs is None or len(rs) == 0 or (limit and len(result) >= limit):
                end = True
                break
        result += rs
        if verbose:
            print(page,end=' ')
            sys.stdout.flush()
        page += 1
    return result

def search_posts2(query,limit=75):
    """Secondary search function utilizing a generator.

    :param query: The tag search query.
    :type query: str
    :param limit: Number of posts to fetch per page. Default 75.
    :type limit: int
    :returns: A list of images matching the query.
    :rtype: list
    """
    result = []
    url = config.BASE_URL + 'post/index.json?tags=' + str(query) +\
        '&limit=' + (str(limit) if limit > 0 else '100')
    page = 1
    end = False
    while not end:
        rs = _get_data_obj(_get_page(url+'&page='+str(page)))
        yield rs
        if rs is None or len(rs) == 0:
            end = True
            break
        page += 1

def get_popular_by_day(year=None,month=None,day=None):
    """Get a list of popular posts for a single day.

    :param year: Optional, the year to search.
    :type year: int
    :param month: Optional, the month to search.
    :type month: int
    :param day: Optional, the day to search.
    :type day: int
    :returns: A list of up to 32 popular posts for the specified day.
    :rtype: list
    """
    url = config.BASE_URL + 'post/popular_by_day.json'
    if day and month and year:
        url += '?day='+str(day)+'&month='+str(month)+'&year='+str(year)
    return _get_data_obj(_get_page(url))

def get_popular_by_week(year=None,month=None,day=None):
    """Get a list of popular posts for a single week.

    :param year: Optional, the year to search.
    :type year: int
    :param month: Optional, the month to search.
    :type month: int
    :param day: Optional, the day of the start of the week.
    :type day: int
    :returns: A list of up to 32 popular posts for the specified week.
    :rtype: list
    """
    url = config.BASE_URL + 'post/popular_by_week.json'
    if day and month and year:
        url += '?day='+str(day)+'&month='+str(month)+'&year='+str(year)
    return _get_data_obj(_get_page(url))

def get_popular_by_month(year=None,month=None):
    """Get a list of popular posts for a single week.

    :param year: Optional, the year to search.
    :type year: int
    :param month: Optional, the month to search.
    :type month: int
    :returns: A list of up to 32 popular posts for the specified month.
    :rtype: list
    """
    url = config.BASE_URL + 'post/popular_by_month.json'
    if month and year:
        url += '?day='+str(day)+'&month='+str(month)+'&year='+str(year)
    return _get_data_obj(_get_page(url))

def get_post(post_id):
    """Fetch a specific post's information.

    :param post_id: The ID number of the post to fetch.
    :type post_id: int
    :returns: An object containing post details, or None on error.
    :rtype: dict or None
    """
    url = config.BASE_URL + 'post/show.json?id=' + str(post_id)
    post_data = _get_data_obj(_get_page(url))
    return post_data

def get_post_favs(post_id):
    """Get a list of users who favorited a post.

    :param post_id: The ID number of the post.
    :type post_id: int
    :returns: The list of users with the post in their favorites.
    :rtype: list
    """
    url = config.BASE_URL + 'favorite/list_users.json?id=' + str(post_id)
    return _get_data_obj(_get_page(url))['favorited_users'].split(',')

def vote_post(post_id,vote):
    """Upvote or downvote a specific post.

    :param post_id: The ID number of the post.
    :type post_id: int
    :param vote: 1 for an upvote, -1 for a downvote.
    :type vote: int
    :returns: Whether the vote was successful.
    :rtype: bool
    """
    print('Error: Function not ready. REASON: ' +\
          'Receiving Unordered Collection error.',file=sys.stderr)
    return False
    if str(vote) != '1' and str(vote) != '-1': return False
    data = {
        'id':str(post_id),
        'score':str(vote)
    }
    send_vote = _get_data_obj(_post_data(data,config.BASE_URL+'post/vote.json'))
    return send_vote

def get_post_tag_history(post_id):
    """Get a list of changes to a post's tag list.

    :param post_id: The ID number of the post.
    :type post_id: int
    :returns: A list of the post's tag changes.
    :rtype: list
    """
    url =  config.BASE_URL+'post_tag_history/index.json?post_id=' + str(post_id)
    return _get_data_obj(_get_page(url))

def get_post_flag_history(post_id):
    """Get a list of flags made on a post.

    :param post_id: The ID number of the post.
    :type post_id: int
    :returns: A list of the post's flags.
    :rtype: list
    """
    url = config.BASE_URL+'post_flag_history/index.json?post_id=' + str(post_id)
    return _get_data_obj(_get_page(url))


#
# POOL-RELATED FUNCTIONS
#
def search_pools(query='',limit=5):
    """Search the site's image pools by name.

    :param query: The whole or partial pool name. Omit for all pools.
    :type query: str
    :param limit: The highest number of pages to fetch, 20 results per page.
        Default 5.
    :type limit: int
    :returns: A list of matching pools.
    :rtype: list
    """
    url = config.BASE_URL + 'pool/index.json?query=' + str(query)
    result = []
    page = 1
    end = False
    while not end:
        rs = _get_data_obj(_get_page(url+'&page='+str(page)))
        if rs is None or len(rs) == 0 or \
            len(result) >= (limit*20 if limit > 0 else len(result)+1):
                end = True
                break
        result += rs
        page += 1
    return result

def get_pool(pool_id):
    """Return data on a specific image pool.

    :param pool_id: The ID number of the pool.
    :type pool_id: int
    :returns: An object containing pool data and a list of images.
    :rtype: dict
    """
    url = config.BASE_URL + 'pool/show.json?id=' + str(pool_id)
    pool_info = _get_data_obj(_get_page(url+'&page=999'))
    if not pool_info:
        return None
    pool_info['posts'] = []
    page = 1
    end = False
    while not end:
        rs = _get_data_obj(_get_page(url+'&page='+str(page)))
        if rs is None or len(rs['posts']) == 0:
            end = True
            break
        pool_info['posts'] += rs['posts']
        page += 1
    return pool_info


#
# COMMENT-RELATED FUNCTIONS
#
def get_recent_comments():
    """Get a list of the 25 most recent comments made site-wide.

    :returns: A list of comment objects for the most recent comments.
    :rtype: list
    """
    url = config.BASE_URL + 'comment/index.json'
    return _get_data_obj(_get_page(url))

def get_post_comments(post_id):
    """Get a list of comments on a given post.

    :param post_id: The ID number of the post.
    :type post_id: int
    :returns: A list of comment objects for the post.
    :rtype: list
    """
    url = config.BASE_URL + 'comment/index.json?post_id=' + str(post_id)
    return list(reversed(_get_data_obj(_get_page(url))))
    
def get_comment(comment_id):
    """Retrieves a single comment. Must call login() first.

    :param comment_id: The ID number of the comment.
    :type comment_id: int
    :returns:
    :rtype:
    """
    data = {
        'id':str(comment_id),
        'login':str(config.USERNAME),
        'password_hash':str(config.PASSWORD)
    }
    return _get_data_obj(_post_data(data,config.BASE_URL + 'comment/show.json'))

def create_comment(post_id,comment):
    """Make a comment on a given post.

    :param post_id: The ID number of the post.
    :type post_id: int
    :param comment: The comment body.
    :type comment: str
    :returns: The result of
    """
    print('Error: Function not ready. REASON: Need to test.',file=sys.stderr)
    return False
    data = {
        'post_id':str(post_id),
        'comment':str(comment),
        'login':str(config.USERNAME),
        'password_hash':str(config.PASSWORD)
    }
    return _get_data_obj(_post_data(data,config.BASE_URL+'comment/create.json'))


#
# TAG-RELATED FUNCTIONS
#
def list_tags(page=1,limit=2):
    url = config.BASE_URL + 'tag/index.json?order=name'
    result = []
    end = False
    while not end:
        rs = _get_data_obj(_get_page(url+'&page='+str(page)))
        if rs is None or len(rs) == 0 or \
            len(result) >= (limit*50 if limit > 0 else len(result)+1):
                end = True
                break
        result += rs
        page += 1
    return result

def get_related_tags(tags):
    """Get a collection of tags related to the query.

    :param tags: A list of tags to search, space separated.
    :type tags: str
    :returns: A dict of lists, each list relating to one search tag.
    :rtype: dict
    """
    url = config.BASE_URL + 'tag/related.json?tags=' + str(tags)
    return _get_data_obj(_get_page(url))


#
# USER-RELATED FUNCTIONS
#
def login(username,password):
    """Attemt to login to the site, store credentials if successful.

    :param username: Your username.
    :type username: str
    :param password: Your password.
    :type password: str
    :returns: Whether the login attempt was successful or not.
    :rtype: bool
    """
    data = {
        'name':str(username),
        'password':str(password)
    }
    result = _get_data_obj(_post_data(data,config.BASE_URL + 'user/login.json'))
    print(result)
    if not 'password_hash' in result:
        config.USERNAME, config.PASSWORD = ('','')
        return False
    config.USERNAME = result['name']
    config.PASSWORD = result['password_hash']
    return True

def search_users(user_id):
    """Search for users by ID or username.

    :param user_id: The ID number or username of the user to search for.
    :type user_id: int or str
    :returns: An list of objects for matching users.
    :rtype: list
    """
    try: int(user_id)
    except ValueError: id_type = 'name'
    else: id_type = 'id'
    url = config.BASE_URL + 'user/index.json?' + id_type + '=' + str(user_id)
    user_list = _get_data_obj(_get_page(url))
    return user_list

def get_user(user_id):
    """Get information on a specific user.

    :param user_id: The ID number or username of the user.
    :type user_id: int or str
    :returns: An object containing profile info for the user.
    :rtype: dict
    """
    user_list = search_users(user_id)
    if len(user_list) == 0:
        raise UserNotFoundError('User '+str(user_id)+' not found.')
    return user_list[0]

def get_user_tag_history(user_id):
    """Get a list of tag changes made by a user.

    :param user_id: The ID number or username of the user.
    :type post_id: int or str
    :returns: A list of the user's tag changes.
    :rtype: list
    """
    try: int(user_id)
    except ValueError: id_type = 'user_name'
    else: id_type = 'user_id'
    url = config.BASE_URL + 'post_tag_history/index.json?' +\
          id_type+'='+str(user_id)
    return _get_data_obj(_get_page(url))

def get_user_flag_history(user_id):
    """Get a list of post flags made by a user.

    :param user_id: The ID number or username of the user.
    :type post_id: int or str
    :returns: A list of the user's created flags.
    :rtype: list
    """
    try: int(user_id)
    except ValueError: id_type = 'user_name'
    else: id_type = 'user_id'
    url =  config.BASE_URL + 'post_flag_history/index.json?' +\
          id_type+'='+str(user_id)
    return _get_data_obj(_get_page(url))

