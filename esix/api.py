#!/usr/bin/env python3
"""
Standard functions for e621's JSON API.
"""

import json
import requests
import time

from . import config, errors


def RateLimited(max_per_second):
    min_interval = 1.0/float(max_per_second)
    def decorate(func):
        last_called = [0.0]
        def limited_func(*args,**kargs):
            elapsed = time.clock()-last_called[0]
            remaining = min_interval-elapsed
            if remaining > 0:
                time.sleep(remaining)
            ret = func(*args,**kargs)
            last_called[0] = time.clock()
            return ret
        return limited_func
    return decorate

@RateLimited(2)
def _get_page(url):
    """Fetch the content from a given web URL.

    :param url: The URL to fetch.
    :type url: str
    :returns: Response retrieved from URL.
    :rtype: HTTPResponse
    :raises: errors.APIGetError
    """
    try: req = requests.get(url, headers={'User-Agent':config.USER_AGENT})
    except Exception as e: raise errors.APIGetError(str(e))
    return req

@RateLimited(2)
def _post_data(data, url):
    """Post the given data object to the given URL.

    :param data: A dict or tuple of tuples with the data to post.
    :type data: dict or tuple
    :param url: The URL to post to.
    :type url: str
    :returns: Content of the response.
    :rtype: HTTPResponse
    :raises: errors.APIPostError
    """
    err = None
    try:
        req = requests.post(url, data=data, 
            headers={'User-Agent':config.USER_AGENT})
    except Exception as e: raise errors.APIPostError(str(e))
    return req

def _get_data_obj(page):
    """Parse a JSON-structured HTTPResponse into a Python object.

    :param page: The JSON-encoded page content to fetch.
    :type page: HTTPResponse
    :returns: The decoded JSON object.
    :rtype: dict or list
    :raises: errors.JSONError
    """
    try: data = json.loads(page.text)
    except (ValueError, AttributeError):
        if 'This website is under heavy load' in page.text:
            raise errors.SiteLoadError('API call failed. ' +\
                'The site is under heavy load.')
        raise errors.JSONError('The supplied page data is not JSON-decodable.')
    return data

def _fetch_data(url):
    """Fetches a URL's page content, then converts it into a JSON object.

    :param url: The URL of the JSON-encoded page.
    :type url: str
    :returns: The decoded JSON object.
    :rtype: dict
    """
    return _get_data_obj(_get_page(url))