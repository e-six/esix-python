#!/usr/bin/env python3
"""
Standard functions for e621's JSON API.
"""

import json
import requests

from . import config, errors


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
    try: data = json.loads(page)
    except (ValueError, AttributeError):
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